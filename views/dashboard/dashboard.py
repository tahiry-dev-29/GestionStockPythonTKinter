import tkinter as tk
from styles.colors import *
from views.managers.users.users_view import UsersView


class DashboardWindow:
    def __init__(self, root, show_login_callback, logged_in_user):
        self.root = root
        self.show_login_callback = show_login_callback
        self.logged_in_user = logged_in_user

        self.frame = tk.Frame(self.root, bg=BG_COLOR)
        self.frame.pack(fill="both", expand=True)

        self.content_frame = None
        self.current_view = None

        self.setup_ui()
        self.show_default_view()

    def setup_ui(self):
        self.create_sidebar()
        self.create_content_area()

    def create_sidebar(self):
        self.sidebar = tk.Frame(self.frame, bg=PRIMARY_COLOR, width=250)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.create_logo()
        self.create_menu_items()
        self.create_logout_button()

    def create_logo(self):
        logo_frame = tk.Frame(self.sidebar, bg=PRIMARY_COLOR)
        logo_frame.pack(fill="x", pady=20)

        tk.Label(
            logo_frame,
            text="Stock Manager",
            font=TITLE_FONT,
            bg=PRIMARY_COLOR,
            fg="white",
        ).pack(pady=10)

    def create_menu_items(self):
        menu_items = [
            ("📊 Dashboard", self.show_default_view),
            ("👥 User Management", self.show_user_manager),
            ("📦 Stock Management", self.show_stock_manager),
            ("🏷️ Categories", self.show_categories),
            ("📈 Reports", self.show_reports),
        ]

        for text, command in menu_items:
            self.create_menu_item(text, command)

    def create_menu_item(self, text, command):
        btn = tk.Button(
            self.sidebar,
            text=text,
            command=command,
            bg=PRIMARY_COLOR,
            fg="white",
            font=NORMAL_FONT,
            bd=0,
            relief="flat",
            anchor="w",
            padx=20,
            pady=10,
            width=25,
            cursor="hand2",
        )
        btn.pack(fill="x", pady=2)

        btn.bind("<Enter>", lambda e: btn.configure(bg=HOVER_COLOR))
        btn.bind("<Leave>", lambda e: btn.configure(bg=PRIMARY_COLOR))

    def create_logout_button(self):
        tk.Button(
            self.sidebar, text="Logout", command=self.logout, **BUTTON_STYLE
        ).pack(side="bottom", pady=20, padx=20, fill="x")

    def create_content_area(self):
        self.content_frame = tk.Frame(self.frame, bg=BG_COLOR)
        self.content_frame.pack(side="right", fill="both", expand=True)

    def clear_content(self):
        if hasattr(self, "current_view") and self.current_view:
            self.current_view.destroy()

        if hasattr(self, "content_frame") and self.content_frame:
            for widget in self.content_frame.winfo_children():
                widget.destroy()

    def show_user_manager(self):
        self.clear_content()
        self.current_view = UsersView(self.content_frame)

    def show_default_view(self):
        self.clear_content()
        if self.logged_in_user:
            welcome_text = f"Welcome, {self.logged_in_user['username']} ({self.logged_in_user['role']})"
        else:
            welcome_text = "Welcome to Dashboard (User not found)"

        tk.Label(
            self.content_frame,
            text=welcome_text,
            font=TITLE_FONT,
            bg=BG_COLOR,
            fg=TEXT_COLOR,
        ).pack(pady=20)

    def show_products(self):
        pass

    def show_categories(self):
        self.clear_content()
        from views.managers.categories.categories_view import CategoriesView

        self.current_view = CategoriesView(self.content_frame)

    def show_reports(self):
        pass

    def show_stock_manager(self):
        self.clear_content()
        from views.managers.stocks.stock import StockWindow

        self.current_view = StockWindow(self.content_frame)

    def logout(self):
        self.frame.destroy()
        self.show_login_callback()

    def destroy(self):
        self.frame.destroy()
