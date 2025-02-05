import tkinter as tk
from tkinter import messagebox
from database.db_manager import DBManager
from styles.colors import *

class RegisterWindow:
    def __init__(self, root, show_login_callback):
        self.root = root
        self.show_login_callback = show_login_callback
        self.db_manager = DBManager()
        
        self.frame = tk.Frame(self.root, bg=BG_COLOR)
        self.frame.pack(fill='both', expand=True)
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Register - Stock Management System")
        
        # Main container with card effect
        container = tk.Frame(self.frame, bg='white', padx=40, pady=30)
        container.place(relx=0.5, rely=0.5, anchor='center')
        
        # Card border
        card_border = tk.Frame(container, bg=PRIMARY_COLOR)
        card_border.place(x=-2, y=-2, width=404, height=604)
        
        # Main card
        card = tk.Frame(container, bg='white', padx=40, pady=30)
        card.pack()

        # Logo and Title
        tk.Label(card, text="📝", font=("Helvetica", 48), bg='white', fg=PRIMARY_COLOR).pack(pady=(0, 10))
        tk.Label(card, text="Create Account", font=TITLE_FONT, bg='white', fg=TEXT_COLOR).pack(pady=(0, 20))

        # Username field
        tk.Label(card, text="Username*", **LABEL_STYLE).pack(anchor='w')
        self.entry_username = tk.Entry(card, **ENTRY_STYLE)
        self.entry_username.pack(fill='x', pady=(5, 15), ipady=8)

        # Email field
        tk.Label(card, text="Email*", **LABEL_STYLE).pack(anchor='w')
        self.entry_email = tk.Entry(card, **ENTRY_STYLE)
        self.entry_email.pack(fill='x', pady=(5, 15), ipady=8)

        # Password field
        tk.Label(card, text="Password*", **LABEL_STYLE).pack(anchor='w')
        self.entry_password = tk.Entry(card, **ENTRY_STYLE, show="•")
        self.entry_password.pack(fill='x', pady=(5, 15), ipady=8)

        # Confirm Password field
        tk.Label(card, text="Confirm Password*", **LABEL_STYLE).pack(anchor='w')
        self.entry_confirm_password = tk.Entry(card, **ENTRY_STYLE, show="•")
        self.entry_confirm_password.pack(fill='x', pady=(5, 25), ipady=8)

        # Register button
        register_btn = tk.Button(card, text="Register", command=self.register_user, **BUTTON_STYLE)
        register_btn.pack(fill='x', ipady=10, pady=(0, 20))

        # Login link
        tk.Label(card, text="Already have an account?", bg='white', fg="#666666").pack()
        login_link = tk.Label(
            card, text="Login here", fg=PRIMARY_COLOR,
            cursor="hand2", bg='white', font=("Helvetica", 12, "bold")
        )
        login_link.pack(pady=(5, 0))
        login_link.bind('<Button-1>', lambda e: self.navigate_to_login())

    def register_user(self):
        username = self.entry_username.get()
        email = self.entry_email.get()
        password = self.entry_password.get()
        confirm_password = self.entry_confirm_password.get()

        if not all([username, email, password, confirm_password]):
            messagebox.showerror("Error", "All fields are required")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        try:
            self.db_manager.create_user(username, email, password)
            messagebox.showinfo("Success", "Registration successful!")
            self.navigate_to_login()
        except Exception as e:
            messagebox.showerror("Error", f"Registration failed: {str(e)}")

    def navigate_to_login(self):
        self.frame.destroy()
        self.show_login_callback()

    def destroy(self):
        self.frame.destroy()
