from database.db_config import DbConnection

class UserManager:
    def __init__(self):
        self.db = DbConnection()

    def get_all_users(self):
        query = "SELECT id, username, email, role, created_at FROM users"
        return self.db.fetch_all(query)

    def create_user(self, username, email, password, role="user"):
        query = """INSERT INTO users (username, email, password, role) 
                  VALUES (%s, %s, %s, %s)"""
        return self.db.execute(query, (username, email, password, role))

    def update_user(self, user_id, data):
        query = """UPDATE users SET username=%s, email=%s, role=%s 
                  WHERE id=%s"""
        return self.db.execute(query, (data['username'], data['email'], 
                                     data['role'], user_id))

    def delete_user(self, user_id):
        query = "DELETE FROM users WHERE id=%s"
        return self.db.execute(query, (user_id,))

    def get_user_by_id(self, user_id):
        query = "SELECT * FROM users WHERE id=%s"
        return self.db.fetch_one(query, (user_id,))
