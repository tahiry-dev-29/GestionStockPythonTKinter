import mysql.connector
from mysql.connector import Error
from hashlib import sha256
import logging
from .db_config import DB_CONFIG

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class DBManager:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.connect()
        self.create_tables_if_not_exist()

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
            self.cursor.execute(
                f"""
                SELECT COUNT(*)
                FROM information_schema.tables 
                WHERE table_schema = '{DB_CONFIG['database']}'
                AND table_name = '{table_name}'
                """
            )
            return self.cursor.fetchone()["COUNT(*)"] > 0
        except Error as e:
            logging.error(f"❌ Error checking table existence: {e}")
            return False

    def create_tables_if_not_exist(self):
        try:
            # IMPORTANT : Créer d'abord les tables référencées (categories) pour éviter les problèmes de clés étrangères.
            if not self.table_exists("categories"):
                self.cursor.execute(
                    """
                    CREATE TABLE categories (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100) NOT NULL UNIQUE,
                        description TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                    """
                )
                logging.info("✅ Categories table created successfully")

            if not self.table_exists("users"):
                self.cursor.execute(
                    """
                    CREATE TABLE users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        username VARCHAR(50) UNIQUE NOT NULL,
                        email VARCHAR(100) UNIQUE NOT NULL,
                        password VARCHAR(255) NOT NULL,
                        role VARCHAR(20) DEFAULT 'user',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                    """
                )
                logging.info("✅ Users table created successfully")

            if not self.table_exists("products"):
                self.cursor.execute(
                    """
                    CREATE TABLE products (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        price DECIMAL(10,2) NOT NULL,
                        quantity INT NOT NULL,
                        photo TEXT,
                        category_id INT,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (category_id) REFERENCES categories(id)
                    )
                    """
                )
                logging.info("✅ Products table created successfully")

            if not self.table_exists("stock_movements"):
                self.cursor.execute(
                    """
                    CREATE TABLE stock_movements (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        product_id INT NOT NULL,
                        quantity INT NOT NULL,
                        movement_type ENUM('IN', 'OUT') NOT NULL,
                        movement_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (product_id) REFERENCES products(id)
                    )
                    """
                )
                logging.info("✅ Stock movements table created successfully")

            self.connection.commit()

        except Error as e:
            logging.error(f"❌ Error creating tables: {e}")
            self.connection.rollback()
            raise

    def hash_password(self, password):
        return sha256(password.encode()).hexdigest()

    def insert_user(self, username, password, email):
        try:
            hashed_password = self.hash_password(password)
            self.cursor.execute(
                """
                INSERT INTO users (username, email, password)
                VALUES (%s, %s, %s)
                """,
                (username, email, hashed_password),
            )
            self.connection.commit()
            logging.info(f"✅ Nouvel utilisateur créé: {username}")
        except Error as e:
            logging.error(f"❌ Erreur lors de l'insertion de l'utilisateur: {e}")
            raise

    def get_users(self):
        try:
            # Ajout de la colonne created_at pour afficher la date de création
            self.cursor.execute("SELECT id, username, email, created_at FROM users")
            return self.cursor.fetchall()
        except Error as e:
            logging.error(f"❌ Erreur lors de la récupération des utilisateurs: {e}")
            raise

    def update_user(self, user_id, username, password):
        try:
            hashed_password = self.hash_password(password)
            self.cursor.execute(
                """
                UPDATE users 
                SET username = %s, password = %s 
                WHERE id = %s
                """,
                (username, hashed_password, user_id),
            )
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
            self.cursor.execute(
                """
                INSERT INTO products (name, price, quantity, photo, category_id)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    product.name,
                    product.price,
                    product.quantity,
                    product.photo,
                    product.category_id,
                ),
            )
            self.connection.commit()
            logging.info(f"✅ Nouveau produit ajouté: {product.name}")
        except Error as e:
            logging.error(f"❌ Erreur lors de l'insertion du produit: {e}")
            raise

    def get_products(self):
        try:
            query = """
                SELECT p.*, c.name as category_name
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.id
            """
            self.cursor.execute(query)
            return self.cursor.fetchall()  # returns a list of dict
        except Error as e:
            logging.error(f"❌ Erreur lors de la récupération des produits: {e}")
            raise

    def get_product_by_id(self, product_id):
        try:
            self.cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
            return self.cursor.fetchone()
        except Error as e:
            logging.error(f"❌ Erreur lors de la récupération du produit: {e}")
            raise

    def update_product(self, product_id, name, price, quantity, photo, category_id):
        try:
            self.cursor.execute(
                """
                UPDATE products 
                SET name = %s, price = %s, quantity = %s, photo = %s, category_id = %s 
                WHERE id = %s
                """,
                (name, price, quantity, photo, category_id, product_id),
            )
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
            # Hachage du mot de passe avant vérification
            hashed_password = self.hash_password(password)
            query = """SELECT * FROM users 
                       WHERE username = %s AND password = %s"""
            self.cursor.execute(query, (username, hashed_password))
            user = self.cursor.fetchone()
            return user is not None
        except Error as e:
            logging.error(f"❌ Error verifying user: {e}")
            return False

    def verify_user_by_email(self, email, password):
        try:
            self.connect()  # Ensure connection is active
            hashed_password = self.hash_password(password)
            query = "SELECT * FROM users WHERE email = %s AND password = %s"
            self.cursor.execute(query, (email, hashed_password))
            return self.cursor.fetchone() is not None
        except Error as e:
            logging.error(f"❌ Error verifying user: {e}")
            return False

    def create_user(self, username, email, password, role="user"):
        try:
            self.connect()  # Ensure connection is active
            hashed_password = self.hash_password(password)
            query = """INSERT INTO users (username, email, password, role) 
                       VALUES (%s, %s, %s, %s)"""
            self.cursor.execute(query, (username, email, hashed_password, role))
            self.connection.commit()
            return True
        except Error as e:
            logging.error(f"❌ Error creating user: {e}")
            self.connection.rollback()
            return False

    # Méthodes de gestion des catégories
    def create_category(self, name, description=""):
        try:
            self.cursor.execute(
                """
                INSERT INTO categories (name, description)
                VALUES (%s, %s)
                """,
                (name, description),
            )
            self.connection.commit()
            logging.info(f"✅ New category created: {name}")
            return True
        except Error as e:
            logging.error(f"❌ Error creating category: {e}")
            self.connection.rollback()
            return False

    def get_all_categories(self):
        try:
            self.cursor.execute("SELECT * FROM categories")
            return self.cursor.fetchall()
        except Error as e:
            logging.error(f"❌ Error fetching categories: {e}")
            return []

    def get_category_by_id(self, category_id):
        try:
            self.cursor.execute(
                "SELECT * FROM categories WHERE id = %s", (category_id,)
            )
            return self.cursor.fetchone()
        except Error as e:
            logging.error(f"❌ Error fetching category: {e}")
            return None

    def update_category(self, category_id, name, description):
        try:
            self.cursor.execute(
                """
                UPDATE categories 
                SET name = %s, description = %s 
                WHERE id = %s
                """,
                (name, description, category_id),
            )
            self.connection.commit()
            logging.info(f"✅ Category updated: {name}")
            return True
        except Error as e:
            logging.error(f"❌ Error updating category: {e}")
            self.connection.rollback()
            return False

    def delete_category(self, category_id):
        try:
            self.cursor.execute("DELETE FROM categories WHERE id = %s", (category_id,))
            self.connection.commit()
            logging.info(f"✅ Category deleted: ID {category_id}")
            return True
        except Error as e:
            logging.error(f"❌ Error deleting category: {e}")
            self.connection.rollback()
            return False

    def __del__(self):
        try:
            if hasattr(self, "cursor") and self.cursor:
                self.cursor.close()
            if (
                hasattr(self, "connection")
                and self.connection
                and self.connection.is_connected()
            ):
                self.connection.close()
        except Exception as e:
            logging.error(f"Error closing connection: {e}")
