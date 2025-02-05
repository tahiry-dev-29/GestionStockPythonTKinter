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
        
        # Container principal avec effet de carte
        container = tk.Frame(self.frame, bg='white', padx=40, pady=30)
        container.place(relx=0.5, rely=0.5, anchor='center')
        
        # Ajouter une bordure à la carte
        card_border = tk.Frame(container, bg=PRIMARY_COLOR)
        card_border.place(x=-2, y=-2, width=404, height=504)
        
        # Carte principale
        card = tk.Frame(container, bg='white', padx=40, pady=30)
        card.pack()

        # Logo ou icône (à remplacer par votre logo)
        logo_label = tk.Label(card, text="🏪", font=("Helvetica", 48), bg='white', fg=PRIMARY_COLOR)
        logo_label.pack(pady=(0, 10))

        # Titre
        tk.Label(
            card,
            text="Welcome Back!",
            font=TITLE_FONT,
            bg='white',
            fg=TEXT_COLOR
        ).pack(pady=(0, 5))

        tk.Label(
            card,
            text="Please login to your account",
            font=NORMAL_FONT,
            bg='white',
            fg="#666666"
        ).pack(pady=(0, 20))

        # Username
        tk.Label(
            card,
            text="Username",
            font=NORMAL_FONT,
            bg='white',
            fg=TEXT_COLOR
        ).pack(anchor='w')
        
        self.entry_username = tk.Entry(
            card,
            font=NORMAL_FONT,
            bg='#F8F9FA',
            fg=TEXT_COLOR,
            relief='flat',
            width=30
        )
        self.entry_username.pack(pady=(5, 15), ipady=8)

        # Password
        tk.Label(
            card,
            text="Password",
            font=NORMAL_FONT,
            bg='white',
            fg=TEXT_COLOR
        ).pack(anchor='w')
        
        self.entry_password = tk.Entry(
            card,
            font=NORMAL_FONT,
            bg='#F8F9FA',
            fg=TEXT_COLOR,
            relief='flat',
            width=30,
            show="•"
        )
        self.entry_password.pack(pady=(5, 25), ipady=8)

        # Login button with hover effect
        login_btn = tk.Button(
            card,
            text="Login",
            command=self.login_user,
            font=BUTTON_FONT,
            bg=PRIMARY_COLOR,
            fg='white',
            relief='flat',
            width=25,
            cursor='hand2'
        )
        login_btn.pack(pady=(0, 20), ipady=10)
        
        # Bind hover effects
        login_btn.bind('<Enter>', lambda e: login_btn.configure(bg='#1976D2'))
        login_btn.bind('<Leave>', lambda e: login_btn.configure(bg=PRIMARY_COLOR))

        # Register link
        register_frame = tk.Frame(card, bg='white')
        register_frame.pack(pady=(10, 0))
        
        tk.Label(
            register_frame,
            text="Don't have an account? ",
            font=NORMAL_FONT,
            bg='white',
            fg="#666666"
        ).pack(side='left')
        
        register_link = tk.Label(
            register_frame,
            text="Register",
            font=("Helvetica", 12, "bold"),
            bg='white',
            fg=PRIMARY_COLOR,
            cursor='hand2'
        )
        register_link.pack(side='left')
        
        # Modifier le binding du register link
        register_link.bind('<Button-1>', lambda e: self.navigate_to_register())
        register_link.bind('<Enter>', lambda e: register_link.configure(fg='#1976D2'))
        register_link.bind('<Leave>', lambda e: register_link.configure(fg=PRIMARY_COLOR))

    def navigate_to_register(self):
        from views import RegisterWindow
        self.frame.destroy()
        RegisterWindow(self.root, lambda: LoginWindow(self.root, self.show_dashboard_callback))

    def login_user(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        try:
            if self.db_manager.verify_user(username, password):
                messagebox.showinfo("Success", "Login Successful")
                self.frame.pack_forget()  # Cacher le frame de login
                self.frame.destroy()  # Détruire proprement le frame
                self.root.update()  # Forcer la mise à jour de l'interface
                self.show_dashboard_callback()  # Afficher le dashboard
            else:
                messagebox.showerror("Error", "Invalid Credentials")
        except Exception as e:
            messagebox.showerror("Error", f"Login error: {str(e)}")

    def destroy(self):
        self.frame.destroy()
