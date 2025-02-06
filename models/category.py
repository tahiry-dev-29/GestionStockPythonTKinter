import sqlite3

class Category:
    def __init__(self, id=None, name="", description="", created_at=None):
        self.id = id
        self.name = name
        self.description = description
        self.created_at = created_at

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at
        }

    @staticmethod
    def from_db_row(row):
        if row is None:
            return None
        return Category(
            id=row[0],
            name=row[1],
            description=row[2],
            created_at=row[3]
        )

    @staticmethod
    def create_table():
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def save(self):
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO categories (name, description, created_at) VALUES (?, ?, ?)', (self.name, self.description, self.created_at))
            conn.commit()

    @staticmethod
    def all():
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM categories')
            return cursor.fetchall()
