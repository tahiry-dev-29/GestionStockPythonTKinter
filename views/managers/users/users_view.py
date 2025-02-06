import tkinter as tk
from tkinter import ttk, messagebox
from controllers.user_controller import UserController
from .dialogs.update_dialog import UpdateUserDialog
from styles.theme import Theme
from styles.colors import *

class UsersView:
    def __init__(self, parent):
        self.parent = parent
        self.controller = UserController()
        self.theme = Theme()
        
        self.frame = tk.Frame(self.parent, bg=BG_COLOR)
        self.frame.pack(fill='both', expand=True, padx=30, pady=20)
        
        self.setup_ui()
        self.setup_treeview_style()
        self.load_users()

    def setup_ui(self):
        header = tk.Frame(self.frame, bg=BG_COLOR)
        header.pack(fill='x', pady=(0, 25))

        title_frame = tk.Frame(header, bg=BG_COLOR)
        title_frame.pack(fill='x')

        tk.Label(
            title_frame,
            text="Users Management",
            font=("Helvetica", 24, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack(side='left')

        tk.Label(
            self.frame,
            text="Double-click on a user to edit",
            font=("Helvetica", 12),
            bg=BG_COLOR,
            fg="#666666"
        ).pack(pady=(0, 15))

        self.table_container = tk.Frame(self.frame, bg=BG_COLOR)
        self.table_container.pack(fill='both', expand=True)

        self.setup_table()

    def setup_treeview_style(self):
        style = ttk.Style()
        treeview_style = self.theme.setup_treeview_style()
        
        style.configure(
            treeview_style["style_name"],
            **treeview_style["settings"]
        )
        
        heading_style = treeview_style["heading_style"].copy()
        heading_style.update({
            'font': ("Helvetica", 11, "bold"),
            'padding': 10
        })
        style.configure(
            f"{treeview_style['style_name']}.Heading",
            **heading_style
        )
        
        style.configure(
            f"{treeview_style['style_name']}.Treeview",
            rowheight=35,
            borderwidth=0
        )
        
        style.map(
            f"{treeview_style['style_name']}.Treeview",
            background=[('selected', '#2196F3')],
            foreground=[('selected', 'white')]
        )

    def setup_table(self):
        columns = Theme.get_table_columns()
        
        table_frame = tk.Frame(self.table_container, bg="white", bd=1, relief="solid")
        table_frame.pack(fill='both', expand=True)
        
        self.tree = ttk.Treeview(
            table_frame,
            columns=tuple(columns.keys()),
            show="headings",
            style="Custom.Treeview",
            height=15
        )

        y_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=y_scrollbar.set)

        self.tree.pack(side='left', fill='both', expand=True)
        y_scrollbar.pack(side='right', fill='y')

        for col, props in columns.items():
            self.tree.heading(col, text=col)
            self.tree.column(col, **props)

        self.tree.bind("<Double-1>", self.on_item_double_click)
        self.tree.bind("<Motion>", self.on_hover)
        self.tree.tag_configure("hover", background="#E3F2FD")

    def on_item_double_click(self, event):
        selected_item = self.tree.focus()
        if not selected_item:
            return
        user_data = self.get_user_data_from_item(selected_item)
        self.show_update_dialog(user_data)

    def get_user_data_from_item(self, item):
        values = self.tree.item(item)['values']
        return {
            'id': values[0],
            'username': values[1],
            'email': values[2],
            'role': values[3]
        }

    def load_users(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        users = self.controller.get_all_users()
        for user in users:
            self.tree.insert("", "end", values=(
                user['id'],
                user['username'],
                user['email'],
                user['role'],
            ))

    def delete_user(self, user_id, username):
        try:
            if self.controller.delete_user(user_id, username):
                self.load_users()
                messagebox.showinfo("Success", f"User {username} has been deleted successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete user: {str(e)}")

    def handle_update(self, data):
        try:
            if self.controller.update_user(data):
                self.load_users()
                messagebox.showinfo("Success", f"User {data['username']} has been updated successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update user: {str(e)}")

    def show_update_dialog(self, user_data):
        dialog = UpdateUserDialog(
            self.frame,
            user_data,
            on_update=self.handle_update,
            on_delete=lambda: self.delete_user(user_data['id'], user_data['username'])
        )

    def refresh_data(self):
        self.load_users()
        messagebox.showinfo("Success", "Data refreshed successfully!")

    def handle_add(self, data):
        try:
            if self.controller.create_user(data):
                self.load_users()
                messagebox.showinfo("Success", f"User {data['username']} has been added successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add user: {str(e)}")

    def on_hover(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            for row in self.tree.get_children():
                self.tree.item(row, tags=())
            self.tree.item(item, tags=("hover",))

    def destroy(self):
        self.frame.destroy()
