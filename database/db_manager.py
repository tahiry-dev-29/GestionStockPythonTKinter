# Gestion des requêtes SQL génériques

import sqlite3

class DBManager:
    def __init__(self):
        self.conn = sqlite3.connect('stock_management.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT,
                quantity INTEGER,
                price REAL
            )
        """)
        self.conn.commit()

    def insert_product(self, product):
        self.cursor.execute("""
            INSERT INTO products (name, quantity, price)
            VALUES (?, ?, ?)
        """, (product.name, product.quantity, product.price))
        self.conn.commit()
