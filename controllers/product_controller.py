# Logique métier pour les produits
from models.product_manager import ProductManager

class ProductController:
    def __init__(self):
        self.product_manager = ProductManager()

    def get_all_products(self):
        return self.product_manager.get_all_products()

    def create_product(self, data):
        return self.product_manager.create_product(data)

    def update_product(self, product_id, data):
        return self.product_manager.update_product(product_id, data)

    def delete_product(self, product_id):
        return self.product_manager.delete_product(product_id)