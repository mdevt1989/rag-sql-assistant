from typing import Dict, List, Any
import psycopg2
from psycopg2.extras import RealDictCursor
import logging
from config.config import DatabaseConfig

class DatabaseManager:
    def __init__(self):
        self.config = DatabaseConfig()
        self.logger = logging.getLogger(__name__)
        
    def get_connection(self):
        try:
            return psycopg2.connect(
                dbname=self.config.DB_NAME,
                user=self.config.DB_USER,
                password=self.config.DB_PASSWORD,
                host=self.config.DB_HOST,
                port=self.config.DB_PORT
            )
        except Exception as e:
            self.logger.error(f"Database connection error: {str(e)}")
            raise

    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        try:
            with self.get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute(query)
                    return cur.fetchall()
        except Exception as e:
            self.logger.error(f"Query execution error: {str(e)}")
            raise 