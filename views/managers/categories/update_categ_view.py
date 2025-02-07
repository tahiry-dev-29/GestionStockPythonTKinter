import tkinter as tk
from tkinter import messagebox
from styles.colors import *
from styles.theme import *

class UpdateCategoryDialog(tk.Toplevel):
    def __init__(self, parent, category_id, name, description, controller, on_update):
        super().__init__(parent)
        self.category_id = category_id
        self.controller = controller
        self.on_update = on_update
        self.current_dialog = None
        
        self.configure(**DIALOG_STYLE)
        self.title("Edit Category")
        self.geometry("400x300")
        
        # Make dialog modal
        self.transient(parent)
        
        # Wait for dialog to be ready before grab_set
        self.after(100, lambda: self.grab_set())
        
        # Handle dialog close
        self.protocol("WM_DELETE_WINDOW", self.on_dialog_close)
        
        # Center the dialog
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
        # Create main frame
        main_frame = tk.Frame(self, bg=BG_COLOR, padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Name field
        name_label = tk.Label(main_frame, text="Name:", font=SUBTITLE_FONT, bg=BG_COLOR, fg=TEXT_PRIMARY)
        name_label.pack(anchor='w', pady=(0, 5))
        
        self.name_entry = tk.Entry(main_frame, **ENTRY_STYLE)
        self.name_entry.insert(0, name)
        self.name_entry.pack(fill='x', pady=(0, 15))
        
        # Description field
        desc_label = tk.Label(main_frame, text="Description:", font=SUBTITLE_FONT, bg=BG_COLOR, fg=TEXT_PRIMARY)
        desc_label.pack(anchor='w', pady=(0, 5))
        
        self.desc_entry = tk.Text(main_frame, height=5, **ENTRY_STYLE)
        self.desc_entry.insert("1.0", description)
        self.desc_entry.pack(fill='both', expand=True, pady=(0, 20))
        
        # Buttons frame
        button_frame = tk.Frame(main_frame, bg=BG_COLOR)
        button_frame.pack(fill='x', pady=(10, 0))
        
        cancel_button = tk.Button(
            button_frame,
            text="Cancel",
            command=self.destroy,
            **BUTTON_STYLE
        )
        cancel_button.pack(side='left', padx=(0, 10))
        
        save_button = tk.Button(
            button_frame,
            text="Save",
            command=self.save,
            **BUTTON_STYLE
        )
        save_button.pack(side='right')

    def on_dialog_close(self):
        self.current_dialog = None
        self.destroy()

    def save(self):
        new_name = self.name_entry.get().strip()
        new_description = self.desc_entry.get("1.0", tk.END).strip()
        
        if not new_name:
            messagebox.showwarning("Warning", "Name is required!", parent=self)
            return
            
        if self.controller.update_category(self.category_id, new_name, new_description):
            self.on_update()
            self.current_dialog = None
            self.destroy()
            messagebox.showinfo("Success", "Category updated successfully!")
        else:
            messagebox.showerror("Error", "Failed to update category", parent=self)
