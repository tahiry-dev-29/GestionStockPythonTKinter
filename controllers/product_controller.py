# Logique métier pour les produits
from database.db_manager import DBManager
from models.product import Product

class ProductController:
    def __init__(self):
        self.db_manager = DBManager()

    def create_product(self, product):
        try:
            self.db_manager.insert_product(product)
            return True
        except Exception as e:
            print(f"Error creating product: {e}")
            return False

    def get_all_products(self):
        products_data = self.db_manager.get_products()
        return [Product(
            id=prod['id'],
            name=prod['name'],
            price=prod['price'],
            quantity=prod['quantity'],
            photo=prod['photo'],
            category_id=prod['category_id']
        ) for prod in products_data]

    def get_product_by_id(self, product_id):
        product_data = self.db_manager.get_product_by_id(product_id)
        if product_data:
            return Product(
                id=product_data['id'],
                name=product_data['name'],
                price=product_data['price'],
                quantity=product_data['quantity'],
                photo=product_data['photo'],
                category_id=product_data['category_id']
            )
        return None

    def update_product(self, product_id, name, price, quantity, photo, category_id):
        return self.db_manager.update_product(product_id, name, price, quantity, photo, category_id)

    def delete_product(self, product_id):
        return self.db_manager.delete_product(product_id)