from database.db_manager import DBManager
from models.category import Category

class CategoryController:
    def __init__(self):
        self.db_manager = DBManager()

    def create_category(self, name, description=""):
        return self.db_manager.create_category(name, description)

    def get_all_categories(self):
        categories_data = self.db_manager.get_all_categories()
        return [Category(
            id=cat['id'],
            name=cat['name'],
            description=cat['description'],
            created_at=cat['created_at']
        ) for cat in categories_data]

    def get_category_by_id(self, category_id):
        category_data = self.db_manager.get_category_by_id(category_id)
        if category_data:
            return Category(
                id=category_data['id'],
                name=category_data['name'],
                description=category_data['description'],
                created_at=category_data['created_at']
            )
        return None

    def update_category(self, category_id, name, description):
        return self.db_manager.update_category(category_id, name, description)

    def delete_category(self, category_id):
        return self.db_manager.delete_category(category_id)
