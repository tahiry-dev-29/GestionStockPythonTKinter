import sqlite3
from database.db_config import DbConnection


class Product:
    def __init__(
        self,
        id=None,
        name="",
        price=0.0,
        quantity=0,
        photo="",
        category_id=None,
        created_at=None,
    ):
        self.id = id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.photo = photo
        self.category_id = category_id
        self.created_at = created_at  # Date de création du produit
        self.db = DbConnection()

    def __str__(self):
        # Affichage du nom, de la quantité, du prix et de la date de création
        return f"{self.name} (Qté: {self.quantity}, Prix: {self.price}€, Créé le: {self.created_at})"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "photo": self.photo,
            "category_id": self.category_id,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_db_row(row):
        if row is None:
            return None
        # On s'attend à ce que row contienne 7 colonnes : id, name, price, quantity, photo, category_id, created_at
        return Product(
            id=row[0],
            name=row[1],
            price=row[2],
            quantity=row[3],
            photo=row[4],
            category_id=row[5],
            created_at=row[6],  # Date de création récupérée depuis la BDD
        )

    @staticmethod
    def create_table():
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    price REAL NOT NULL,
                    quantity INTEGER NOT NULL,
                    photo TEXT,
                    category_id INTEGER,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES categories(id)
                )
            """
            )
            conn.commit()

    def save(self):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO products (name, price, quantity, photo, category_id)
                VALUES (?, ?, ?, ?, ?)
            """,
                (self.name, self.price, self.quantity, self.photo, self.category_id),
            )
            conn.commit()

    @staticmethod
    def all():
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products")
            return cursor.fetchall()
