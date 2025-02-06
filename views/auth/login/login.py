import tkinter as tk
from tkinter import messagebox
from database.db_manager import DBManager
from styles.colors import *

class LoginWindow:
    def __init__(self, root, show_dashboard_callback):
        self.root = root
        self.show_dashboard_callback = show_dashboard_callback
        self.db_manager = DBManager()
        
        self.frame = tk.Frame(self.root, bg=BG_COLOR)
        self.frame.pack(fill='both', expand=True)
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Login - Stock Management System")
        
        # Main container with card effect
        container = tk.Frame(self.frame, bg='white', padx=40, pady=30)
        container.place(relx=0.5, rely=0.5, anchor='center')
        
        # Card border
        card_border = tk.Frame(container, bg=PRIMARY_COLOR)
        card_border.place(x=-2, y=-2, width=404, height=504)
        
        # Main card
        card = tk.Frame(container, bg='white', padx=40, pady=30)
        card.pack()

        # Logo
        logo_label = tk.Label(card, text="🔐", font=("Helvetica", 28), bg='white', fg=PRIMARY_COLOR)
        logo_label.pack(pady=(0, 10))

        # Title
        tk.Label(card, text="Welcome Back!", font=TITLE_FONT, bg='white', fg=TEXT_COLOR).pack(pady=(0, 5))
        tk.Label(card, text="Login to your account", font=NORMAL_FONT, bg='white', fg="#666666").pack(pady=(0, 20))

        # Email field
        tk.Label(card, text="Email*", **LABEL_STYLE).pack(anchor='w')
        self.entry_email = tk.Entry(card, **ENTRY_STYLE)
        self.entry_email.pack(fill='x', pady=(5, 15), ipady=8)

        # Password field
        tk.Label(card, text="Password*", **LABEL_STYLE).pack(anchor='w')
        self.entry_password = tk.Entry(card, **ENTRY_STYLE, show="•")
        self.entry_password.pack(fill='x', pady=(5, 25), ipady=8)

        # Login button
        login_btn = tk.Button(card, text="Login", command=self.login_user, **BUTTON_STYLE)
        login_btn.pack(fill='x', ipady=10, pady=(0, 20))

        # Register link
        tk.Label(card, text="Don't have an account?", bg='white', fg="#666666").pack()
        register_link = tk.Label(
            card, text="Register here", fg=PRIMARY_COLOR,
            cursor="hand2", bg='white', font=("Helvetica", 12, "bold")
        )
        register_link.pack(pady=(5, 0))
        register_link.bind('<Button-1>', lambda e: self.navigate_to_register())

    def navigate_to_register(self):
        self.frame.destroy()
        # Utiliser le callback pour naviguer vers register depuis main.py
        self.show_dashboard_callback(register=True)

    def login_user(self):
        email = self.entry_email.get()
        password = self.entry_password.get()
        
        try:
            if self.db_manager.verify_user_by_email(email, password):
                messagebox.showinfo("Success", "Login Successful")
                self.frame.destroy()  # Clean up the login frame
                self.show_dashboard_callback()
            else:
                messagebox.showerror("Error", "Invalid Email or Password")
        except Exception as e:
            messagebox.showerror("Error", f"Login error: {str(e)}")

    def destroy(self):
        self.frame.destroy()
