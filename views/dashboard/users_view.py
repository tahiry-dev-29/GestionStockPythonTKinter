import tkinter as tk
from tkinter import ttk, messagebox
from styles.colors import *
from database import DBManager

class UsersView:
    def __init__(self, parent):
        self.parent = parent
        self.db = DBManager()
        self.setup_ui()
        self.load_users()

    def setup_ui(self):
        # Frame principal
        self.frame = tk.Frame(self.parent, bg=BG_COLOR, padx=20, pady=20)
        self.frame.pack(fill='both', expand=True)

        # Titre
        tk.Label(
            self.frame,
            text="Users Management",
            font=TITLE_FONT,
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=(0, 20))

        # Zone des formulaires
        form_frame = tk.Frame(self.frame, bg=BG_COLOR)
        form_frame.pack(fill='x', pady=10)

        # Champs du formulaire
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        tk.Label(form_frame, text="Username:", bg=BG_COLOR).pack(side='left', padx=5)
        tk.Entry(form_frame, textvariable=self.username_var, **ENTRY_STYLE).pack(side='left', padx=5)
        
        tk.Label(form_frame, text="Password:", bg=BG_COLOR).pack(side='left', padx=5)
        tk.Entry(form_frame, textvariable=self.password_var, show="•", **ENTRY_STYLE).pack(side='left', padx=5)

        # Boutons CRUD
        buttons_frame = tk.Frame(form_frame, bg=BG_COLOR)
        buttons_frame.pack(side='left', padx=5)

        tk.Button(buttons_frame, text="Add", command=self.add_user, **BUTTON_STYLE).pack(side='left', padx=2)
        tk.Button(buttons_frame, text="Update", command=self.update_user, **BUTTON_STYLE).pack(side='left', padx=2)
        tk.Button(buttons_frame, text="Delete", command=self.delete_user, **BUTTON_STYLE).pack(side='left', padx=2)

        # Table
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Username"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Username", text="Username")
        self.tree.pack(fill='both', expand=True, pady=10)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

    def load_users(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Load users from database
        users = self.db.get_users()
        for user in users:
            self.tree.insert("", "end", values=user)

    def add_user(self):
        username = self.username_var.get()
        password = self.password_var.get()
        
        if username and password:
            try:
                self.db.insert_user(username, password)
                self.load_users()
                self.clear_form()
                messagebox.showinfo("Success", "User added successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Please fill all fields")

    def update_user(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a user to update")
            return
            
        user_id = self.tree.item(selection[0])['values'][0]
        username = self.username_var.get()
        password = self.password_var.get()
        
        if username and password:
            try:
                self.db.update_user(user_id, username, password)
                self.load_users()
                self.clear_form()
                messagebox.showinfo("Success", "User updated successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def delete_user(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a user to delete")
            return
            
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this user?"):
            user_id = self.tree.item(selection[0])['values'][0]
            try:
                self.db.delete_user(user_id)
                self.load_users()
                self.clear_form()
                messagebox.showinfo("Success", "User deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def on_select(self, event):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            username = item['values'][1]
            self.username_var.set(username)
            self.password_var.set("")  # Clear password for security

    def clear_form(self):
        self.username_var.set("")
        self.password_var.set("")

    def destroy(self):
        self.frame.destroy()
