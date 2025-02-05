import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from models.user_manager import UserManager
from styles.colors import *

class UserManagerView:
    def __init__(self, parent):
        self.parent = parent
        self.user_manager = UserManager()
        
        self.setup_ui()
        self.load_users()

    def setup_ui(self):
        # Header
        header = tk.Frame(self.parent, bg=BG_COLOR)
        header.pack(fill='x', padx=20, pady=10)
        
        tk.Label(
            header,
            text="User Management",
            font=HEADER_FONT,
            bg=BG_COLOR
        ).pack(side='left')
        
        tk.Button(
            header,
            text="Add New User",
            command=self.show_add_user_dialog,
            **BUTTON_STYLE
        ).pack(side='right')

        # Table
        self.create_table()

    def create_table(self):
        columns = ('ID', 'Username', 'Email', 'Role', 'Created At', 'Actions')
        
        self.tree = ttk.Treeview(self.parent, columns=columns, show='headings')
        
        # Configure columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.parent, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack elements
        self.tree.pack(padx=20, pady=10, fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Bind double-click event for editing
        self.tree.bind('<Double-1>', self.edit_user)

    def load_users(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Load users from database
        users = self.user_manager.get_all_users()
        for user in users:
            self.tree.insert('', 'end', values=user)

    def show_add_user_dialog(self):
        # Create dialog for adding new user
        dialog = tk.Toplevel(self.parent)
        dialog.title("Add New User")
        dialog.geometry("400x300")
        dialog.transient(self.parent)
        
        # Add form fields
        # ... form implementation ...

    def edit_user(self, event):
        # Get selected item
        item = self.tree.selection()[0]
        user_data = self.tree.item(item)
        # Show edit dialog
        # ... dialog implementation ...

    def destroy(self):
        self.parent.destroy()
