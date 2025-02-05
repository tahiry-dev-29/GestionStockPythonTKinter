from database.db_config import DbConnection

class Product:
    def __init__(self, name, quantity, price, id=None):
        self.id = id
        self.name = name
        self.quantity = quantity
        self.price = price
        self.db = DbConnection()

    def __str__(self):
        return f"{self.name} (Qté: {self.quantity}, Prix: {self.price}€)"
    
    def get_all_products(self):
        # ...existing code...
        pass
    
    def add_product(self, data):
        # ...existing code...
        pass
