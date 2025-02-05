import tkinter as tk
from tkinter import ttk
from styles.colors import *

class DashboardWindow:
    def __init__(self, root, show_login_callback):
        self.root = root
        self.show_login_callback = show_login_callback
        
        self.frame = tk.Frame(self.root, bg=BG_COLOR)
        self.frame.pack(fill='both', expand=True)
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Dashboard")
        
        # Frame principal avec style
        main_frame = tk.Frame(self.frame, bg=BG_COLOR, padx=40, pady=20)
        main_frame.place(relx=0.5, rely=0.5, anchor='center')

        tk.Label(
            main_frame, 
            text="Welcome to Dashboard", 
            font=TITLE_FONT,
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=20)
        
        # Boutons d'action
        buttons_frame = tk.Frame(main_frame, bg=BG_COLOR)
        buttons_frame.pack(pady=10)
        
        tk.Button(
            buttons_frame, 
            text="Manage Products", 
            command=self.manage_products,
            **BUTTON_STYLE
        ).pack(pady=5)
        
        tk.Button(
            buttons_frame, 
            text="Logout",
            command=self.show_login_callback,
            **BUTTON_STYLE
        ).pack(pady=5)

    def manage_products(self):
        # À implémenter : gestion des produits
        pass

    def destroy(self):
        self.frame.destroy()
