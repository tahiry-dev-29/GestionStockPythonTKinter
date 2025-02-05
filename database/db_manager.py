import mysql.connector
from hashlib import sha256
import logging
from .db_config import DB_CONFIG

logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

class DBManager:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(**DB_CONFIG)
            self.cursor = self.conn.cursor()
            logging.info("✅ Connexion à MySQL réussie")
            self.create_tables()
        except mysql.connector.Error as e:
            logging.error(f"❌ Erreur de connexion à MySQL: {e}")
            raise

    def create_tables(self):
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255) UNIQUE,
                    password VARCHAR(255)
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    quantity INT,
                    price DECIMAL(10, 2)
                )
            """)
            self.conn.commit()
            logging.info("✅ Tables créées avec succès")
        except mysql.connector.Error as e:
            logging.error(f"❌ Erreur lors de la création des tables: {e}")
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
            self.conn.commit()
            logging.info(f"✅ Nouvel utilisateur créé: {username}")
        except mysql.connector.Error as e:
            logging.error(f"❌ Erreur lors de l'insertion de l'utilisateur: {e}")
            raise

    def get_users(self):
        try:
            self.cursor.execute("SELECT id, username FROM users")
            return self.cursor.fetchall()
        except mysql.connector.Error as e:
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
            self.conn.commit()
            logging.info(f"✅ Utilisateur mis à jour: {username}")
        except mysql.connector.Error as e:
            logging.error(f"❌ Erreur lors de la mise à jour de l'utilisateur: {e}")
            raise

    def delete_user(self, user_id):
        try:
            self.cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            self.conn.commit()
            logging.info(f"✅ Utilisateur supprimé: ID {user_id}")
        except mysql.connector.Error as e:
            logging.error(f"❌ Erreur lors de la suppression de l'utilisateur: {e}")
            raise

    def insert_product(self, product):
        try:
            self.cursor.execute("""
                INSERT INTO products (name, quantity, price)
                VALUES (%s, %s, %s)
            """, (product.name, product.quantity, product.price))
            self.conn.commit()
            logging.info(f"✅ Nouveau produit ajouté: {product.name}")
        except mysql.connector.Error as e:
            logging.error(f"❌ Erreur lors de l'insertion du produit: {e}")
            raise

    def get_products(self):
        try:
            self.cursor.execute("SELECT id, name, quantity, price FROM products")
            return self.cursor.fetchall()
        except mysql.connector.Error as e:
            logging.error(f"❌ Erreur lors de la récupération des produits: {e}")
            raise

    def update_product(self, product_id, name, quantity, price):
        try:
            self.cursor.execute("""
                UPDATE products 
                SET name = %s, quantity = %s, price = %s 
                WHERE id = %s
            """, (name, quantity, price, product_id))
            self.conn.commit()
            logging.info(f"✅ Produit mis à jour: {name}")
        except mysql.connector.Error as e:
            logging.error(f"❌ Erreur lors de la mise à jour du produit: {e}")
            raise

    def delete_product(self, product_id):
        try:
            self.cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
            self.conn.commit()
            logging.info(f"✅ Produit supprimé: ID {product_id}")
        except mysql.connector.Error as e:
            logging.error(f"❌ Erreur lors de la suppression du produit: {e}")
            raise

    def verify_user(self, username, password):
        try:
            self.cursor.execute("""
                SELECT password FROM users 
                WHERE username = %s
            """, (username,))
            result = self.cursor.fetchone()
            return result and result[0] == self.hash_password(password)
        except mysql.connector.Error as e:
            logging.error(f"❌ Erreur lors de la vérification de l'utilisateur: {e}")
            raise
