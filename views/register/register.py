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
        
        # Container principal avec effet de carte
        container = tk.Frame(self.frame, bg='white', padx=40, pady=30)
        container.place(relx=0.5, rely=0.5, anchor='center')
        
        # Bordure de la carte
        card_border = tk.Frame(container, bg=PRIMARY_COLOR)
        card_border.place(x=-2, y=-2, width=404, height=504)
        
        # Carte principale
        card = tk.Frame(container, bg='white', padx=40, pady=30)
        card.pack()

        # Logo ou icône
        logo_label = tk.Label(card, text="📝", font=("Helvetica", 48), bg='white', fg=PRIMARY_COLOR)
        logo_label.pack(pady=(0, 10))

        # Titre
        tk.Label(card, text="Create Account", font=TITLE_FONT, bg='white', fg=TEXT_COLOR).pack(pady=(0, 5))
        tk.Label(card, text="Please fill in the form below", font=NORMAL_FONT, bg='white', fg="#666666").pack(pady=(0, 20))

        # Username
        tk.Label(card, text="Username", font=NORMAL_FONT, bg='white', fg=TEXT_COLOR).pack(anchor='w')
        self.entry_username = tk.Entry(card, font=NORMAL_FONT, bg=INPUT_BG, fg=TEXT_COLOR, relief='flat', width=30)
        self.entry_username.pack(pady=(5, 15), ipady=8)

        # Password
        tk.Label(card, text="Password", font=NORMAL_FONT, bg='white', fg=TEXT_COLOR).pack(anchor='w')
        self.entry_password = tk.Entry(card, font=NORMAL_FONT, bg=INPUT_BG, fg=TEXT_COLOR, relief='flat', width=30, show="•")
        self.entry_password.pack(pady=(5, 25), ipady=8)

        # Register button with hover effect
        register_btn = tk.Button(
            card, text="Register", command=self.register_user,
            font=BUTTON_FONT, bg=PRIMARY_COLOR, fg='white',
            relief='flat', width=25, cursor='hand2'
        )
        register_btn.pack(pady=(0, 20), ipady=10)
        
        # Hover effects
        register_btn.bind('<Enter>', lambda e: register_btn.configure(bg=HOVER_COLOR))
        register_btn.bind('<Leave>', lambda e: register_btn.configure(bg=PRIMARY_COLOR))

        # Login link
        login_frame = tk.Frame(card, bg='white')
        login_frame.pack(pady=(10, 0))
        tk.Label(login_frame, text="Already have an account? ", font=NORMAL_FONT, bg='white', fg="#666666").pack(side='left')
        login_link = tk.Label(login_frame, text="Login", font=("Helvetica", 12, "bold"), bg='white', fg=PRIMARY_COLOR, cursor='hand2')
        login_link.pack(side='left')
        login_link.bind('<Button-1>', lambda e: self.navigate_to_login())
        login_link.bind('<Enter>', lambda e: login_link.configure(fg=HOVER_COLOR))
        login_link.bind('<Leave>', lambda e: login_link.configure(fg=PRIMARY_COLOR))

    def navigate_to_login(self):
        from views import LoginWindow
        self.frame.destroy()
        LoginWindow(self.root, self.show_login_callback)

    def register_user(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        if username and password:
            try:
                self.db_manager.insert_user(username, password)
                messagebox.showinfo("Success", "Registration Successful")
                self.navigate_to_login()
            except Exception as e:
                messagebox.showerror("Error", f"Registration error: {str(e)}")
        else:
            messagebox.showerror("Error", "Please fill out all fields")

    def destroy(self):
        self.frame.destroy()
