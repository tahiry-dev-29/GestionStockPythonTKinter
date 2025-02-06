from models.user_manager import UserManager
from tkinter import messagebox

class UserController:
    def __init__(self):
        self.user_manager = UserManager()

    def get_all_users(self):
        try:
            return self.user_manager.get_all_users()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch users: {str(e)}")
            return []

    def create_user(self, data):
        try:
            return self.user_manager.create_user(
                data['username'],
                data['email'],
                data['password'],
                data['role']
            )
        except Exception as e:
            raise Exception(f"Failed to create user: {str(e)}")

    def update_user(self, data):
        try:
            self.user_manager.update_user(data['id'], data)
            return True
        except Exception as e:
            raise Exception(f"Failed to update user: {str(e)}")

    def delete_user(self, user_id, username):
        try:
            self.user_manager.delete_user(user_id)
            return True
        except Exception as e:
            raise Exception(f"Failed to delete user: {str(e)}")