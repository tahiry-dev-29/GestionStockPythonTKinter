from database.database import Database
from models.category import Category

class CategoryController:
    def __init__(self):
        self.db = Database()

    def create_category(self, name, description=""):
        try:
            self.db.cursor.execute(
                "INSERT INTO categories (name, description) VALUES (?, ?)",
                (name, description)
            )
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Error creating category: {e}")
            return False

    def get_all_categories(self):
        try:
            self.db.cursor.execute("SELECT * FROM categories")
            rows = self.db.cursor.fetchall()
            return [Category.from_db_row(row) for row in rows]
        except Exception as e:
            print(f"Error fetching categories: {e}")
            return []

    def get_category_by_id(self, category_id):
        try:
            self.db.cursor.execute(
                "SELECT * FROM categories WHERE id = ?",
                (category_id,)
            )
            row = self.db.cursor.fetchone()
            return Category.from_db_row(row)
        except Exception as e:
            print(f"Error fetching category: {e}")
            return None

    def update_category(self, category_id, name, description):
        try:
            self.db.cursor.execute(
                "UPDATE categories SET name = ?, description = ? WHERE id = ?",
                (name, description, category_id)
            )
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Error updating category: {e}")
            return False

    def delete_category(self, category_id):
        try:
            self.db.cursor.execute(
                "DELETE FROM categories WHERE id = ?",
                (category_id,)
            )
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting category: {e}")
            return False

    def __del__(self):
        self.db.close()
