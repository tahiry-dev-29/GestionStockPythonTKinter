import mysql.connector
from mysql.connector import Error
from hashlib import sha256
import logging
from .db_config import DB_CONFIG

logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

class DBManager:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            if not self.connection or not self.connection.is_connected():
                self.connection = mysql.connector.connect(**DB_CONFIG)
                self.cursor = self.connection.cursor(dictionary=True)
                logging.info("✅ Database manager initialized successfully")
        except Error as e:
            logging.error(f"❌ Error connecting to MySQL: {e}")
            raise

    def table_exists(self, table_name):
        try:
            self.cursor.execute(f"""
                SELECT COUNT(*)
                FROM information_schema.tables 
                WHERE table_schema = '{DB_CONFIG['database']}'
                AND table_name = '{table_name}'
            """)
            return self.cursor.fetchone()['COUNT(*)'] > 0
        except Error as e:
            logging.error(f"❌ Error checking table existence: {e}")
            return False

    def create_tables_if_not_exist(self):
        try:
            # Create tables only if they don't exist
            if not self.table_exists('users'):
                self.cursor.execute("""
                    CREATE TABLE users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        username VARCHAR(50) UNIQUE NOT NULL,
                        email VARCHAR(100) UNIQUE NOT NULL,
                        password VARCHAR(255) NOT NULL,
                        role VARCHAR(20) DEFAULT 'user',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                logging.info("✅ Users table created successfully")

            # Products table
            if not self.table_exists('products'):
                self.cursor.execute("""
                    CREATE TABLE products (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        quantity INT DEFAULT 0,
                        price DECIMAL(10,2) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                logging.info("✅ Products table created successfully")

            # Stock movements table
            if not self.table_exists('stock_movements'):
                self.cursor.execute("""
                    CREATE TABLE stock_movements (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        product_id INT NOT NULL,
                        quantity INT NOT NULL,
                        movement_type ENUM('IN', 'OUT') NOT NULL,
                        movement_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (product_id) REFERENCES products(id)
                    )
                """)
                logging.info("✅ Stock movements table created successfully")

            self.connection.commit()

        except Error as e:
            logging.error(f"❌ Error creating tables: {e}")
            self.connection.rollback()
            raise

    def hash_password(self, password):
        return sha256(password.encode()).hexdigest()

    def insert_user(self, username, password):
        try:
            hashed_password = self.hash_password(password)
            self.cursor.execute("""
                INSERT INTO users (username, password)
                VALUES (%s, %s)
            """, (username, hashed_password))
            self.connection.commit()
            logging.info(f"✅ Nouvel utilisateur créé: {username}")
        except Error as e:
            logging.error(f"❌ Erreur lors de l'insertion de l'utilisateur: {e}")
            raise

    def get_users(self):
        try:
            self.cursor.execute("SELECT id, username FROM users")
            return self.cursor.fetchall()
        except Error as e:
            logging.error(f"❌ Erreur lors de la récupération des utilisateurs: {e}")
            raise

    def update_user(self, user_id, username, password):
        try:
            hashed_password = self.hash_password(password)
            self.cursor.execute("""
                UPDATE users 
                SET username = %s, password = %s 
                WHERE id = %s
            """, (username, hashed_password, user_id))
            self.connection.commit()
            logging.info(f"✅ Utilisateur mis à jour: {username}")
        except Error as e:
            logging.error(f"❌ Erreur lors de la mise à jour de l'utilisateur: {e}")
            raise

    def delete_user(self, user_id):
        try:
            self.cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            self.connection.commit()
            logging.info(f"✅ Utilisateur supprimé: ID {user_id}")
        except Error as e:
            logging.error(f"❌ Erreur lors de la suppression de l'utilisateur: {e}")
            raise

    def insert_product(self, product):
        try:
            self.cursor.execute("""
                INSERT INTO products (name, quantity, price)
                VALUES (%s, %s, %s)
            """, (product.name, product.quantity, product.price))
            self.connection.commit()
            logging.info(f"✅ Nouveau produit ajouté: {product.name}")
        except Error as e:
            logging.error(f"❌ Erreur lors de l'insertion du produit: {e}")
            raise

    def get_products(self):
        try:
            self.cursor.execute("SELECT id, name, quantity, price FROM products")
            return self.cursor.fetchall()
        except Error as e:
            logging.error(f"❌ Erreur lors de la récupération des produits: {e}")
            raise

    def update_product(self, product_id, name, quantity, price):
        try:
            self.cursor.execute("""
                UPDATE products 
                SET name = %s, quantity = %s, price = %s 
                WHERE id = %s
            """, (name, quantity, price, product_id))
            self.connection.commit()
            logging.info(f"✅ Produit mis à jour: {name}")
        except Error as e:
            logging.error(f"❌ Erreur lors de la mise à jour du produit: {e}")
            raise

    def delete_product(self, product_id):
        try:
            self.cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
            self.connection.commit()
            logging.info(f"✅ Produit supprimé: ID {product_id}")
        except Error as e:
            logging.error(f"❌ Erreur lors de la suppression du produit: {e}")
            raise

    def verify_user(self, username, password):
        try:
            query = """SELECT * FROM users 
                      WHERE username = %s AND password = %s"""
            self.cursor.execute(query, (username, password))
            user = self.cursor.fetchone()
            return user is not None
        except Error as e:
            logging.error(f"❌ Error verifying user: {e}")
            return False

    def verify_user_by_email(self, email, password):
        try:
            self.connect()  # Ensure connection is active
            query = "SELECT * FROM users WHERE email = %s AND password = %s"
            self.cursor.execute(query, (email, password))
            return self.cursor.fetchone() is not None
        except Error as e:
            logging.error(f"❌ Error verifying user: {e}")
            return False

    def create_user(self, username, email, password, role="user"):
        try:
            self.connect()  # Ensure connection is active
            query = """INSERT INTO users (username, email, password, role) 
                      VALUES (%s, %s, %s, %s)"""
            self.cursor.execute(query, (username, email, password, role))
            self.connection.commit()
            return True
        except Error as e:
            logging.error(f"❌ Error creating user: {e}")
            self.connection.rollback()
            return False

    def __del__(self):
        try:
            if hasattr(self, 'cursor') and self.cursor:
                self.cursor.close()
            if hasattr(self, 'connection') and self.connection and self.connection.is_connected():
                self.connection.close()
        except Exception as e:
            logging.error(f"Error closing connection: {e}")
