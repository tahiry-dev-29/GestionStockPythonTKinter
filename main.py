from tkinter import *
from views import DashboardWindow, LoginWindow, RegisterWindow
from database.db_manager import DBManager
from styles.colors import BG_COLOR


class StockManagementApp:
    def __init__(self):
        self.root = Tk()
        self.setup_main_window()
        self.current_window = None
        self.db_manager = DBManager()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.show_login()

    def setup_main_window(self):
        self.root.title("Stock Management System")
        self.root.configure(bg=BG_COLOR)
        self.center_window(1300, 650)
        self.root.update_idletasks()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def show_register(self):
        if self.current_window:
            self.current_window.destroy()
        self.current_window = RegisterWindow(self.root, self.show_login)

    def show_login(self):
        if self.current_window:
            self.current_window.destroy()
        self.current_window = LoginWindow(self.root, self.show_dashboard)

    def show_dashboard(self, register=False):
        if register:
            self.show_register()
        else:
            if self.current_window:
                self.current_window.destroy()
            self.current_window = DashboardWindow(self.root, self.show_login)

    def on_closing(self):
        self.root.destroy()

    def run(self):
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.root.destroy()


if __name__ == "__main__":
    app = StockManagementApp()
    app.run()
