import tkinter as tk
from tkinter import ttk, messagebox
from styles.colors import *
from styles.theme import Theme

class UpdateUserDialog:
    def __init__(self, parent, user_data, on_update, on_delete):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Update User")
        self.theme = Theme.get_dialog_style()
        
        self.dialog.geometry("500x450")
        self.dialog.resizable(False, False)
        self.dialog.configure(bg='#f5f5f5')
        self.dialog.transient(parent)
        self.dialog.update_idletasks()
        self.dialog.grab_set()
        
        self.user_data = user_data
        self.on_update = on_update
        self.on_delete = on_delete
        self.setup_ui()

    def setup_ui(self):
        container = tk.Frame(self.dialog, bg='#f5f5f5')
        container.pack(fill='both', expand=True, padx=30, pady=30)

        tk.Label(
            container,
            text="Update User Information",
            font=('Helvetica', 18, 'bold'),
            bg='#f5f5f5',
            fg='#333333'
        ).pack(pady=(0, 30))

        self.create_form(container)

    def create_form(self, parent):
        self.username_var = tk.StringVar(value=self.user_data['username'])
        self.email_var = tk.StringVar(value=self.user_data['email'])
        self.role_var = tk.StringVar(value=self.user_data['role'])

        form = tk.Frame(parent, bg='#f5f5f5')
        form.pack(fill='x', pady=10)

        self.create_field(form, "Username:", self.username_var, 0)
        self.create_field(form, "Email:", self.email_var, 1)
        self.create_role_field(form, 2)
        self.create_buttons(form)

    def create_field(self, parent, label, variable, row):
        frame = tk.Frame(parent, bg='#f5f5f5')
        frame.pack(fill='x', pady=10)
        
        tk.Label(
            frame, 
            text=label,
            font=('Helvetica', 12),
            bg='#f5f5f5',
            fg='#333333'
        ).pack(anchor='w', pady=(0, 5))
        
        entry = tk.Entry(
            frame,
            textvariable=variable,
            font=('Helvetica', 11),
            bg='white',
            relief='solid',
            bd=1
        )
        entry.pack(fill='x', ipady=8)
        
    def create_role_field(self, parent, row):
        frame = tk.Frame(parent, bg='#f5f5f5')
        frame.pack(fill='x', pady=10)
        
        tk.Label(
            frame,
            text="Role:",
            font=('Helvetica', 12),
            bg='#f5f5f5',
            fg='#333333'
        ).pack(anchor='w', pady=(0, 5))
        
        roles = ttk.Combobox(
            frame,
            textvariable=self.role_var,
            values=["user", "admin"],
            state="readonly",
            font=('Helvetica', 11)
        )
        roles.pack(fill='x', ipady=4)

    def create_buttons(self, parent):
        button_frame = tk.Frame(parent, bg='#f5f5f5')
        button_frame.pack(fill='x', pady=(30, 0))

        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=self.dialog.destroy,
            font=('Helvetica', 11),
            bg='#e0e0e0',
            fg='#333333',
            padx=20,
            pady=10,
            relief='flat'
        )
        cancel_btn.pack(side='right', padx=5)

        delete_btn = tk.Button(
            button_frame,
            text="Delete",
            command=self.delete_user,
            font=('Helvetica', 11),
            bg='#ff4444',
            fg='white',
            padx=20,
            pady=10,
            relief='flat'
        )
        delete_btn.pack(side='right', padx=5)

        update_btn = tk.Button(
            button_frame,
            text="Update",
            command=self.update_user,
            font=('Helvetica', 11),
            bg='#4CAF50',
            fg='white',
            padx=20,
            pady=10,
            relief='flat'
        )
        update_btn.pack(side='right', padx=5)

        for btn in (cancel_btn, delete_btn, update_btn):
            btn.bind('<Enter>', lambda e, b=btn: self.on_hover(b, True))
            btn.bind('<Leave>', lambda e, b=btn: self.on_hover(b, False))

    def on_hover(self, button, hovering):
        if button['text'] == 'Cancel':
            button['bg'] = '#d0d0d0' if hovering else '#e0e0e0'
        elif button['text'] == 'Delete':
            button['bg'] = '#ff3333' if hovering else '#ff4444'
        else:  # Update button
            button['bg'] = '#45a049' if hovering else '#4CAF50'

    def update_user(self):
        if not self.validate_form():
            return
            
        updated_data = {
            'id': self.user_data['id'],
            'username': self.username_var.get().strip(),
            'email': self.email_var.get().strip(),
            'role': self.role_var.get()
        }
        self.on_update(updated_data)
        self.dialog.destroy()

    def delete_user(self):
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete user {self.user_data['username']}?"):
            self.on_delete()
            self.dialog.destroy()

    def validate_form(self):
        if not self.username_var.get().strip():
            messagebox.showerror("Error", "Username is required")
            return False
        if not self.email_var.get().strip():
            messagebox.showerror("Error", "Email is required")
            return False
        if not self.role_var.get():
            messagebox.showerror("Error", "Role is required")
            return False
        return True
