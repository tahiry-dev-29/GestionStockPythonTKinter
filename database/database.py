import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('stock.db')
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Création de la table users
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )''')

        # Création de la table products
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL
        )''')
        
        self.conn.commit()
