import tkinter as tk
from views.login.login import LoginWindow
from views.dashboard.dashboard import DashboardWindow
from database.db_manager import DBManager
from styles.colors import BG_COLOR
from controllers.auth_controller import AuthController

class StockManagementApp:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_main_window()
        self.current_window = None
        self.auth_controller = AuthController()
        self.show_login()

    def setup_main_window(self):
        self.root.title("Stock Management System")
        self.root.configure(bg=BG_COLOR)
        self.center_window(1200, 700)  # Augmenter la taille de la fenêtre
        self.root.update_idletasks()  # Forcer la mise à jour de la géométrie

    def center_window(self, width, height):
        # Centrer la fenêtre sur l'écran
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def show_register(self):
        if self.current_window:
            self.current_window.destroy()
        self.current_window = None  # Important: reset current_window
        self.current_window = RegisterWindow(self.root, self.show_login)

    def show_login(self):
        if self.current_window:
            self.current_window.destroy()
        self.current_window = None  # Important: reset current_window
        self.current_window = LoginWindow(self.root, self.show_dashboard)

    def show_dashboard(self):
        if self.current_window:
            self.current_window.destroy()
        self.current_window = None
        self.current_window = DashboardWindow(self.root, self.show_login)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = StockManagementApp()
    app.run()
