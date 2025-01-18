import unittest
from src.database.db_manager import DatabaseManager

class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        self.db_manager = DatabaseManager()

    def test_connection(self):
        conn = self.db_manager.get_connection()
        self.assertIsNotNone(conn)
        conn.close()

    def test_execute_query(self):
        query = "SELECT 1 as test"
        result = self.db_manager.execute_query(query)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["test"], 1)

if __name__ == '__main__':
    unittest.main() 