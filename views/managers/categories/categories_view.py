import tkinter as tk
from tkinter import ttk, messagebox
from styles.colors import *
from controllers.category_controller import CategoryController
from styles.theme import *

class CategoriesView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, **FRAME_STYLE)
        self.pack(fill='both', expand=True)
        self.controller = CategoryController()
        self.current_dialog = None  # Track active dialog
        
        # Header
        self.header_frame = tk.Frame(self, bg=BG_COLOR)
        self.header_frame.pack(fill='x', pady=20, padx=20)
        
        tk.Label(
            self.header_frame,
            text="Categories Management",
            font=TITLE_FONT,
            bg=BG_COLOR
        ).pack(side='left')
        
        # Add Category Button
        tk.Button(
            self.header_frame,
            text="+ Add Category",
            command=self.show_add_category_dialog,
            **BUTTON_STYLE
        ).pack(side='right')
        
        # Categories Table
        self.create_categories_table()
        
        # Load categories
        self.setup_tree_events()
        self.load_categories()

    def create_categories_table(self):
        # Table Frame
        table_frame = tk.Frame(self, **FRAME_STYLE)
        table_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Create Treeview
        columns = ('id', 'name', 'description', 'edit', 'delete')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        
        # Define column headings
        self.tree.heading('id', text='ID')
        self.tree.heading('name', text='Name')
        self.tree.heading('description', text='Description')
        self.tree.heading('edit', text='Edit')
        self.tree.heading('delete', text='Delete')
        
        # Column widths
        self.tree.column('id', width=50)
        self.tree.column('name', width=150)
        self.tree.column('description', width=300)
        self.tree.column('edit', width=50)
        self.tree.column('delete', width=50)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack the treeview and scrollbar
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Style the tree
        style = ttk.Style()
        style.configure(
            "Treeview",
            background=SURFACE_COLOR,
            fieldbackground=SURFACE_COLOR,
            foreground=TEXT_PRIMARY,
            rowheight=40,
            font=TEXT_FONT
        )
        style.configure(
            "Treeview.Heading",
            background=PRIMARY_COLOR,
            foreground="white",
            font=SUBTITLE_FONT,
            relief="flat"
        )
        style.map(
            "Treeview",
            background=[("selected", SECONDARY_COLOR)],
            foreground=[("selected", "white")]
        )

    def load_categories(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load categories from database
        categories = self.controller.get_all_categories()
        for category in categories:
            self.tree.insert('', 'end', values=(
                category.id,
                category.name,
                category.description,
                "📝 Edit",  # Edit symbol
                "🗑️ Delete"   # Delete symbol
            ))

    def show_add_category_dialog(self):
        self.show_dialog_safely(self._create_add_dialog)

    def setup_tree_events(self):
        self.tree.bind('<ButtonRelease-1>', self.on_tree_click)

    def on_tree_click(self, event):
        region = self.tree.identify_region(event.x, event.y)
        if region != "cell":
            return

        item = self.tree.identify_row(event.y)
        if not item:
            return

        column = self.tree.identify_column(event.x)
        values = self.tree.item(item)['values']

        if column == '#4':  # Edit column
            self.show_edit_dialog(values[0], values[1], values[2])
        elif column == '#5':  # Delete column
            self.confirm_delete(values[0])

    def show_dialog_safely(self, dialog_func, *args):
        if self.current_dialog is not None:
            self.current_dialog.destroy()
        
        dialog = tk.Toplevel(self)
        self.current_dialog = dialog
        
        # Configure dialog
        dialog.transient(self)
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        
        def on_dialog_close():
            self.current_dialog = None
            dialog.destroy()
            
        dialog.protocol("WM_DELETE_WINDOW", on_dialog_close)
        
        # Center dialog
        self.center_dialog(dialog)
        
        # Make modal
        dialog.grab_set()
        dialog.focus_set()
        
        # Create dialog content
        dialog_func(dialog, *args)
        
        return dialog

    def center_dialog(self, dialog):
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y}')

    def show_edit_dialog(self, category_id, name, description):
        self.show_dialog_safely(self._create_edit_dialog, category_id, name, description)

    def confirm_delete(self, category_id):
        self.show_dialog_safely(self._create_delete_dialog, category_id)

    def _create_add_dialog(self, dialog):
        dialog.configure(**DIALOG_STYLE)
        dialog.title("Add Category")
        
        # Form fields with styled entries
        name_label = tk.Label(dialog, text="Name:", font=SUBTITLE_FONT, bg=BG_COLOR)
        name_label.pack(pady=(0, 5), anchor="w")
        
        name_entry = tk.Entry(dialog, **ENTRY_STYLE)
        name_entry.pack(fill="x", pady=(0, 15))
        
        desc_label = tk.Label(dialog, text="Description:", font=SUBTITLE_FONT, bg=BG_COLOR)
        desc_label.pack(pady=(0, 5), anchor="w")
        
        desc_entry = tk.Text(dialog, height=5, **ENTRY_STYLE)
        desc_entry.pack(fill="both", expand=True, pady=(0, 20))
        
        # Button area
        button_frame = tk.Frame(dialog, bg=BG_COLOR)
        button_frame.pack(fill="x", pady=(20, 0))
        
        save_button = tk.Button(
            button_frame,
            text="Save",
            command=lambda: self.save_category(dialog, name_entry, desc_entry),
            **BUTTON_STYLE
        )
        save_button.pack(side="right")

    def _create_edit_dialog(self, dialog, category_id, name, description):
        dialog.configure(**DIALOG_STYLE)
        dialog.title("Edit Category")
        dialog.geometry("400x300")
        
        # Make dialog modal
        dialog.transient(self)
        
        # Wait for dialog to be ready before grab_set
        self.after(100, lambda: dialog.grab_set())
        
        # Handle dialog close
        def on_dialog_close():
            self.current_dialog = None
            dialog.destroy()
            
        dialog.protocol("WM_DELETE_WINDOW", on_dialog_close)
        
        # Center the dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y}')
        
        # Create main frame
        main_frame = tk.Frame(dialog, padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Name field
        name_frame = tk.Frame(main_frame)
        name_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(name_frame, text="Name:", anchor='w').pack(fill='x')
        name_entry = tk.Entry(name_frame)
        name_entry.insert(0, name)
        name_entry.pack(fill='x', pady=(5, 0))
        
        # Description field
        desc_frame = tk.Frame(main_frame)
        desc_frame.pack(fill='both', expand=True)
        
        tk.Label(desc_frame, text="Description:", anchor='w').pack(fill='x')
        desc_entry = tk.Text(desc_frame, height=5)
        desc_entry.insert("1.0", description)
        desc_entry.pack(fill='both', expand=True, pady=(5, 0))
        
        # Buttons frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill='x', pady=(20, 0))
        
        def cancel():
            dialog.destroy()
            
        def save():
            new_name = name_entry.get().strip()
            new_description = desc_entry.get("1.0", tk.END).strip()
            
            if not new_name:
                messagebox.showwarning("Warning", "Name is required!", parent=dialog)
                return
                
            if self.controller.update_category(category_id, new_name, new_description):
                self.load_categories()
                self.current_dialog = None
                dialog.destroy()
                messagebox.showinfo("Success", "Category updated successfully!")
            else:
                messagebox.showerror("Error", "Failed to update category", parent=dialog)

        # Cancel button
        tk.Button(
            button_frame,
            text="Cancel",
            command=cancel,
            width=15
        ).pack(side='left', padx=(0, 10))
        
        # Save button
        tk.Button(
            button_frame,
            text="Save",
            command=save,
            width=15,
            **BUTTON_STYLE
        ).pack(side='right')

    def _create_delete_dialog(self, dialog, category_id):
        # Configuration de base du dialogue
        dialog.configure(bg=BG_COLOR)
        dialog.title("Confirmer la suppression")
        dialog.geometry("350x200")
        
        # Container principal
        container = tk.Frame(dialog, bg=BG_COLOR, padx=20, pady=10)
        container.pack(fill='both', expand=True)
        
        # Icône d'avertissement
        icon_label = tk.Label(
            container,
            text="⚠️",
            font=(FONT_FAMILY, 48),
            bg=BG_COLOR,
            fg=WARNING_COLOR
        )
        icon_label.pack(pady=(0, 10))
        
        # Message d'avertissement
        message = tk.Label(
            container,
            text="Êtes-vous sûr de vouloir supprimer\ncette catégorie ?",
            font=SUBTITLE_FONT,
            bg=BG_COLOR,
            fg=TEXT_PRIMARY,
            justify='center'
        )
        message.pack(pady=(0, 20))
        
        # Conteneur pour les boutons
        button_container = tk.Frame(container, bg=BG_COLOR)
        button_container.pack(fill='x', pady=(0, 10))
        
        # Fonction de suppression
        def confirm_delete():
            if self.controller.delete_category(category_id):
                self.load_categories()
                dialog.destroy()
                messagebox.showinfo("Succès", "Catégorie supprimée avec succès")
            else:
                messagebox.showerror("Erreur", "Impossible de supprimer la catégorie", parent=dialog)
        
        # Boutons
        cancel_btn = tk.Button(
            button_container,
            text="Annuler",
            command=dialog.destroy,
            bg=SURFACE_COLOR,
            fg=TEXT_PRIMARY,
            font=BUTTON_FONT,
            padx=20,
            pady=5,
            relief="flat",
            cursor="hand2"
        )
        cancel_btn.pack(side='left', padx=5, expand=True)
        
        confirm_btn = tk.Button(
            button_container,
            text="Supprimer",
            command=confirm_delete,
            bg=DANGER_COLOR,
            fg="white",
            font=BUTTON_FONT,
            padx=20,
            pady=5,
            relief="flat",
            cursor="hand2"
        )
        confirm_btn.pack(side='right', padx=5, expand=True)
        
        # Centrer le dialogue
        self.center_dialog(dialog)

    def _handle_delete(self, dialog, category_id):
        if self.controller.delete_category(category_id):
            self.load_categories()
            dialog.destroy()
            self.current_dialog = None
            messagebox.showinfo("Success", "Category deleted successfully!")
        else:
            messagebox.showerror("Error", "Failed to delete category", parent=dialog)

    def save_category(self, dialog, name_entry, desc_entry):
        name = name_entry.get().strip()
        description = desc_entry.get("1.0", tk.END).strip()
        
        if not name:
            messagebox.showwarning("Warning", "Name is required!", parent=dialog)
            return
            
        if self.controller.create_category(name, description):
            self.load_categories()
            self.current_dialog = None
            dialog.destroy()
            messagebox.showinfo("Success", "Category added successfully!")
        else:
            messagebox.showerror("Error", "Failed to add category", parent=dialog)

    # Remove unused methods
    def set_dialog_modal(self, dialog):
        pass
        
    def close_dialog(self, dialog):
        if dialog == self.current_dialog:
            self.current_dialog = None
        dialog.destroy()
