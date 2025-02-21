from tkinter import *
from views import (
    DashboardWindow,
    LoginWindow,
    RegisterWindow,
)
from database.db_manager import DBManager
from styles.colors import BG_COLOR
from models.user_manager import UserManager
import os
from PIL import Image, ImageTk
from tkinter import TclError


class StockManagementApp:
    def __init__(self):
        self.root = Tk()
        self.setup_main_window()
        self.current_window = None
        self.db_manager = DBManager()
        self.user_manager = UserManager()
        self.logged_in_user = None

        icon_path = os.path.abspath("./assets/favicon.ico")
        self.imgicon = ImageTk.PhotoImage(Image.open(icon_path))
        self.root.tk.call("wm", "iconphoto", self.root._w, self.imgicon)

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
        self.current_window = LoginWindow(self.root, self.show_dashboard_after_login)

    def show_dashboard_after_login(self, email=None, register=False):
        if register:
            self.show_register()
        else:
            self.show_dashboard(email=email)

    def show_dashboard(self, email=None):
        if self.current_window:
            self.current_window.destroy()

        if email:
            user = self.user_manager.get_user_by_email(email)
            if user:
                self.logged_in_user = user
                self.current_window = DashboardWindow(
                    self.root, self.show_login, self.logged_in_user
                )
            else:
                self.show_login()
        else:
            self.show_login()

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
