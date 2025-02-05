import tkinter as tk
from tkinter import ttk
from styles.colors import *
from views.managers.users.user_manager import UserManagerView

class DashboardWindow:
    def __init__(self, root, show_login_callback):
        self.root = root
        self.show_login_callback = show_login_callback
        self.current_view = None  # Initialisation de current_view
        
        self.frame = tk.Frame(self.root, bg=BG_COLOR)
        self.frame.pack(fill='both', expand=True)
        
        # Create main layout
        self.create_layout()
        self.show_default_view()

    def create_layout(self):
        # Create sidebar
        self.sidebar = tk.Frame(self.frame, bg=PRIMARY_COLOR, width=250)
        self.sidebar.pack(side='left', fill='y')
        self.sidebar.pack_propagate(False)
        
        # Logo area
        logo_frame = tk.Frame(self.sidebar, bg=PRIMARY_COLOR)
        logo_frame.pack(fill='x', pady=20)
        
        tk.Label(
            logo_frame,
            text="Stock Manager",
            font=TITLE_FONT,
            bg=PRIMARY_COLOR,
            fg="white"
        ).pack(pady=10)

        # Menu items
        self.create_menu_item("Dashboard", self.show_default_view)
        self.create_menu_item("User Management", self.show_user_manager)
        self.create_menu_item("Products", self.show_products)
        self.create_menu_item("Categories", self.show_categories)
        self.create_menu_item("Reports", self.show_reports)
        
        # Logout button at bottom of sidebar
        tk.Button(
            self.sidebar,
            text="Logout",
            command=self.logout,
            **BUTTON_STYLE
        ).pack(side='bottom', pady=20, padx=20, fill='x')

        # Main content area
        self.content_frame = tk.Frame(self.frame, bg=BG_COLOR)
        self.content_frame.pack(side='right', fill='both', expand=True)

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
            cursor="hand2"
        )
        btn.pack(fill='x', pady=2)
        
        # Hover effects
        btn.bind('<Enter>', lambda e: btn.configure(bg=HOVER_COLOR))
        btn.bind('<Leave>', lambda e: btn.configure(bg=PRIMARY_COLOR))

    def clear_content(self):
        if self.current_view:
            self.current_view.destroy()
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_user_manager(self):
        self.clear_content()
        from views.managers.users.users_view import UsersView  # Import local pour éviter les imports circulaires
        self.current_view = UsersView(self.content_frame)

    def show_default_view(self):
        self.clear_content()
        # Add default dashboard content here
        tk.Label(
            self.content_frame,
            text="Welcome to Dashboard",
            font=TITLE_FONT,
            bg=BG_COLOR
        ).pack(pady=20)

    # ... other view methods (show_products, show_categories, etc.) ...

    def logout(self):
        self.frame.destroy()
        self.show_login_callback()
