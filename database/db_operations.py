# database/db_operations.py

import logging
from typing import List, Dict, Any
import psycopg2
from psycopg2.extras import RealDictCursor
from config import DATABASE_CONFIG

logger = logging.getLogger(__name__)

class DatabaseOperations:
    def __init__(self):
        self.connection = self._connect_to_database()

    def _connect_to_database(self):
        try:
            conn = psycopg2.connect(**DATABASE_CONFIG, cursor_factory=RealDictCursor)
            return conn
        except Exception as e:
            logger.error(f"Error connecting to database: {e}")
            raise

    def execute_query(self, sql_query: str) -> List[Dict[str, Any]]:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql_query)
                return cursor.fetchall()
        except Exception as e:
            logger.error(f"Error executing SQL query: {e}")
            raise

    def close_connection(self):
        if self.connection:
            self.connection.close()