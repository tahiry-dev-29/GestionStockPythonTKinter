from database.db_manager import DBManager

class AuthController:
    def __init__(self):
        self.db_manager = DBManager()

    def login(self, username, password):
        try:
            return self.db_manager.verify_user(username, password)
        except Exception as e:
            print(f"Erreur d'authentification: {e}")
            return False

    def register(self, username, password):
        try:
            self.db_manager.insert_user(username, password)
            return True
        except Exception as e:
            print(f"Erreur d'enregistrement: {e}")
            return False
