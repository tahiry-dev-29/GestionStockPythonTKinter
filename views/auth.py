import tkinter as tk
from tkinter import messagebox
from database import Database

class AuthWindow:
    def __init__(self):
        self.db = Database()
        self.window = tk.Tk()
        self.window.title("Authentication")
        self.window.geometry("300x250")

        # Login Frame
        self.login_frame = tk.Frame(self.window)
        tk.Label(self.login_frame, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.pack(pady=5)
        
        tk.Label(self.login_frame, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.pack(pady=5)
        
        tk.Button(self.login_frame, text="Login", command=self.login).pack(pady=10)
        tk.Button(self.login_frame, text="Switch to Signup", 
                 command=lambda: self.switch_frame(self.signup_frame)).pack()
        self.login_frame.pack()

        # Signup Frame
        self.signup_frame = tk.Frame(self.window)
        tk.Label(self.signup_frame, text="New Username:").pack(pady=5)
        self.new_username_entry = tk.Entry(self.signup_frame)
        self.new_username_entry.pack(pady=5)
        
        tk.Label(self.signup_frame, text="New Password:").pack(pady=5)
        self.new_password_entry = tk.Entry(self.signup_frame, show="*")
        self.new_password_entry.pack(pady=5)
        
        tk.Button(self.signup_frame, text="Signup", command=self.signup).pack(pady=10)
        tk.Button(self.signup_frame, text="Switch to Login", 
                 command=lambda: self.switch_frame(self.login_frame)).pack()

    def switch_frame(self, frame):
        self.login_frame.pack_forget()
        self.signup_frame.pack_forget()
        frame.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", 
                      (username, password))
        if cursor.fetchone():
            self.window.destroy()
            from views.stock.stock import StockWindow
            StockWindow()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def signup(self):
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()
        cursor = self.db.conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                         (username, password))
            self.db.conn.commit()
            messagebox.showinfo("Success", "Account created successfully!")
            self.switch_frame(self.login_frame)
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")

    def run(self):
        self.window.mainloop()
