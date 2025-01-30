 # Logique métier pour les mouvements de stock

from models.product import Product
from database.db_manager import DBManager

class StockController:
    def __init__(self, view):
        self.view = view
        self.db_manager = DBManager()

    def add_product(self, product_name, quantity):
        new_product = Product(None, product_name, quantity, 0)  # Assuming price is 0 for now
        self.db_manager.insert_product(new_product)
        self.view.display_message("Product added successfully")