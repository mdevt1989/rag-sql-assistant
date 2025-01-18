from typing import Dict, Any
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import logging
from .query_generator import QueryGenerator
from config.config import DatabaseConfig

class LLMHandler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.query_generator = QueryGenerator(DatabaseConfig.get_db_config())

    def generate_sql_query(self, question: str) -> str:
        try:
            sql_query = self.query_generator.generate_sql_query(question)
            self.logger.info(f"Generated SQL query: {sql_query}")
            return sql_query.strip()
        except Exception as e:
            self.logger.error(f"Error generating SQL query: {str(e)}")
            raise