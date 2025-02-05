import mysql.connector
from mysql.connector import Error
import logging

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'tahiry4534',  # Replace with your actual MySQL password
    'database': 'gestion_stock_py',
    'raise_on_warnings': True
}

class DbConnection:
    def __init__(self):
        self.connection = None
        try:
            self.connect()
            logging.info("✅ Successfully connected to MySQL database")
        except Exception as e:
            logging.error(f"❌ Error connecting to MySQL: {str(e)}")
            raise

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=DB_CONFIG['host'],
                database=DB_CONFIG['database'],
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password']
            )
        except Error as e:
            print(f"Error connecting to MySQL Database: {e}")

    def execute(self, query, params=None):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params or ())
            self.connection.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Error executing query: {e}")
            return None
        finally:
            cursor.close()

    def fetch_one(self, query, params=None):
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            return cursor.fetchone()
        except Error as e:
            print(f"Error fetching data: {e}")
            return None
        finally:
            cursor.close()

    def fetch_all(self, query, params=None):
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            return cursor.fetchall()
        except Error as e:
            print(f"Error fetching data: {e}")
            return []
        finally:
            cursor.close()

    def __del__(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()