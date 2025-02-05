import mysql.connector
import logging
from config.database_config import DB_CONFIG

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.connection = None
            cls._instance.setup_logging()
        return cls._instance

    def setup_logging(self):
        logging.basicConfig(
            filename='database.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def connect(self):
        try:
            if not self.connection or not self.connection.is_connected():
                self.connection = mysql.connector.connect(**DB_CONFIG)
                self.logger.info("Successfully connected to the database")
            return self.connection
        except mysql.connector.Error as err:
            self.logger.error(f"Error connecting to database: {err}")
            raise

    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.logger.info("Database connection closed")

    def execute_query(self, query, params=None):
        try:
            connection = self.connect()
            cursor = connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchall()
            connection.commit()
            self.logger.info(f"Query executed successfully: {query}")
            return result
        except mysql.connector.Error as err:
            self.logger.error(f"Error executing query: {err}")
            connection.rollback()
            raise
        finally:
            cursor.close()
