from tkinter import *
from views import DashboardWindow, LoginWindow, RegisterWindow
from database import DBManager
from styles.colors import BG_COLOR

class StockManagementApp:
    def __init__(self):
        self.root = Tk()
        self.setup_main_window()
        self.current_window = None
        self.db_manager = DBManager()
        self.show_login()

    def setup_main_window(self):
        self.root.title("Stock Management System")
        self.root.configure(bg=BG_COLOR)
        self.center_window(1100, 600)  # Augmenter la taille de la fenêtre
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
        self.current_window = None 
        self.current_window = RegisterWindow(self.root, self.show_login)

    def show_login(self):
        if self.current_window:
            self.current_window.destroy()
        self.current_window = None
        self.current_window = LoginWindow(self.root, self.show_dashboard)

    def show_dashboard(self):
        if self.current_window:
            self.current_window.destroy()
        self.current_window = DashboardWindow(self.root, self.show_login)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = StockManagementApp()
    app.run()
