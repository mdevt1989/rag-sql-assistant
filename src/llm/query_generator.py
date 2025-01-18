# llm/query_generator.py

from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import chromadb
from config.config import LLMConfig
import psycopg2
import logging

class QueryGenerator:
    def __init__(self, db_config):
        self.llm = OllamaLLM(model=LLMConfig.MODEL_NAME)
        self.embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-small-en-v1.5",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': False}
        )
        self.vector_store = self._initialize_vector_store()
        self.db_config = db_config
        
    def _initialize_vector_store(self):
        client = chromadb.Client()
        return Chroma(
            embedding_function=self.embeddings, 
            client=client, 
            collection_name="sales_data_store"
        )

    def get_table_info(self) -> str:
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Enhanced query to get table information including foreign keys
            schema_query = """
                WITH fk_info AS (
                    SELECT
                        tc.table_name,
                        kcu.column_name,
                        ccu.table_name AS foreign_table_name,
                        ccu.column_name AS foreign_column_name
                    FROM information_schema.table_constraints tc
                    JOIN information_schema.key_column_usage kcu
                        ON tc.constraint_name = kcu.constraint_name
                    JOIN information_schema.constraint_column_usage ccu
                        ON ccu.constraint_name = tc.constraint_name
                    WHERE tc.constraint_type = 'FOREIGN KEY'
                )
                SELECT 
                    t.table_name,
                    array_agg(
                        c.column_name || ' ' || c.data_type || 
                        CASE 
                            WHEN c.is_nullable = 'NO' THEN ' NOT NULL'
                            ELSE ''
                        END ||
                        COALESCE(
                            ' (FK -> ' || fk.foreign_table_name || '.' || fk.foreign_column_name || ')',
                            ''
                        )
                    ) as columns
                FROM information_schema.tables t
                JOIN information_schema.columns c 
                    ON c.table_name = t.table_name
                LEFT JOIN fk_info fk
                    ON fk.table_name = t.table_name
                    AND fk.column_name = c.column_name
                WHERE t.table_schema = 'public'
                GROUP BY t.table_name;
            """
            
            cursor.execute(schema_query)
            tables_info = cursor.fetchall()
            
            # Format the schema information with more details
            schema_text = "Database Schema:\n"
            for table_name, columns in tables_info:
                schema_text += f"\nTable: {table_name}\nColumns:\n"
                for col in columns:
                    schema_text += f"  - {col}\n"
            
            return schema_text
            
        except Exception as e:
            logging.error(f"Error fetching schema information: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def generate_sql_query(self, user_query: str) -> str:
        try:
            schema_info = self.get_table_info()
            logging.info(f"Retrieved schema information:\n{schema_info}")
            
            prompt = PromptTemplate(
                input_variables=["schema", "query"],
                template="""
                Given the following database schema:
                {schema}
                
                Task: Convert the following natural language query to a valid SQL query.
                
                Requirements:
                1. Use only the tables and columns that exist in the schema above
                2. Use proper table aliases and column references
                3. For aggregations, make sure to include proper GROUP BY clauses
                4. Always qualify column names with table aliases
                5. For temporal queries (involving dates/months/years):
                   - Use DATE_TRUNC('month', timestamp_column) for monthly aggregation
                   - Use EXTRACT(YEAR FROM timestamp_column) for yearly aggregation
                   - Use TO_CHAR(timestamp_column, 'YYYY-MM') for month-year formatting
                6. For sales/revenue queries:
                   - Use total_amt_usd or total columns depending on context
                   - Always specify the aggregation function (SUM, AVG, etc.)
                7. If the query cannot be answered with the available schema, explain why and respond with:
                   "Unable to generate query with available schema because: [reason]"
                
                User Query: {query}
                
                Analysis Steps:
                1. Identify required tables and their relationships
                2. Identify relevant columns for:
                   - Measures (amounts, quantities)
                   - Dimensions (dates, categories, regions)
                   - Join conditions
                3. Determine appropriate aggregations and groupings
                4. Consider date/time handling if temporal analysis is needed
                
                If you can generate a valid query, format it as:
                SQL_QUERY_START
                [your SQL query here]
                SQL_QUERY_END
                
                If you cannot generate a query, format as:
                ERROR_START
                Unable to generate query with available schema because: [detailed explanation]
                ERROR_END
                """
            )
            
            chain = prompt | self.llm
            response = chain.invoke({"schema": schema_info, "query": user_query})
            logging.info(f"LLM Response: {response}")
            
            # Extract SQL query using more reliable method
            if "SQL_QUERY_START" in response and "SQL_QUERY_END" in response:
                # Get everything between SQL_QUERY_START and SQL_QUERY_END
                sql_parts = response.split("SQL_QUERY_START")[1].split("SQL_QUERY_END")[0].strip()
                
                # Extract only the SQL query part (ignore analysis)
                sql_lines = []
                capture = False
                for line in sql_parts.split('\n'):
                    if line.strip().upper().startswith('SELECT'):
                        capture = True
                    if capture and line.strip():
                        sql_lines.append(line.strip())
                
                if sql_lines:
                    return '\n'.join(sql_lines)
                
            elif "ERROR_START" in response and "ERROR_END" in response:
                error_msg = response.split("ERROR_START")[1].split("ERROR_END")[0].strip()
                return f"Unable to generate query: {error_msg}"
                
            # Fallback: try to extract SQL directly
            if "SELECT" in response and "FROM" in response:
                sql_lines = []
                capture = False
                for line in response.split('\n'):
                    line = line.strip()
                    if line.upper().startswith('SELECT'):
                        capture = True
                    if capture and any(keyword in line.upper() for keyword in 
                        ['SELECT', 'FROM', 'WHERE', 'GROUP BY', 'ORDER BY', 'HAVING']):
                        sql_lines.append(line)
                if sql_lines:
                    return '\n'.join(sql_lines)
                
            return "Unable to generate a valid SQL query from the response"
            
        except Exception as e:
            logging.error(f"Error generating SQL query: {str(e)}")
            return f"Error generating SQL query: {str(e)}"