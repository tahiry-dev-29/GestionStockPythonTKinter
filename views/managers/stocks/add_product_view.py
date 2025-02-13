import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from styles.colors import *
from styles.theme import Theme
import os
from controllers.category_controller import CategoryController
from models.product import Product


class AddProductDialog(tk.Toplevel):
    def __init__(self, parent, controller, on_add):
        super().__init__(parent)
        self.controller = controller
        self.on_add = on_add
        self.current_dialog = None
        self.theme = Theme.get_dialog_style()

        self.configure(bg="#f5f5f5")
        self.title("Add Product")
        self.geometry("500x550")
        self.resizable(False, False)

        self.transient(parent)
        self.after(100, lambda: self.grab_set())
        self.protocol("WM_DELETE_WINDOW", self.on_dialog_close)

        self.setup_ui()  # Ajout d'une fonction setup_ui pour organiser le code

    def setup_ui(self):  # Fonction pour organiser l'interface utilisateur
        container = tk.Frame(self, bg="#f5f5f5", padx=30, pady=30)
        container.pack(fill="both", expand=True)

        self.create_title_label(container)  # Fonction pour le titre
        self.create_form(container)  # Fonction pour le formulaire
        self.create_buttons(container)  # Fonction pour les boutons

    def create_title_label(self, parent):
        tk.Label(
            parent,
            text="Add New Product",
            font=("Helvetica", 18, "bold"),
            bg="#f5f5f5",
            fg="#333333",
        ).pack(pady=(0, 20))

    def create_form(self, parent):
        form_frame = tk.Frame(parent, bg="#f5f5f5")
        form_frame.pack(fill="x", pady=10)

        self.create_form_fields(form_frame)  # Fonction pour les champs du formulaire

    def create_form_fields(self, parent):  # Regroupement des champs du formulaire
        # Name field
        self.create_field(parent, "Product Name:", "name_entry")

        # Price field
        self.create_field(parent, "Price:", "price_entry")

        # Quantity field
        self.create_field(parent, "Quantity:", "quantity_entry")

        # Photo field
        self.create_photo_field(parent)  # Fonction spécifique pour le champ photo

        # Category field
        self.create_category_field(
            parent
        )  # Fonction spécifique pour le champ categorie

    def create_field(
        self, parent, label_text, entry_name
    ):  # Fonction générique pour créer un champ label/entry
        label = tk.Label(
            parent,
            text=label_text,
            font=("Helvetica", 12),
            bg="#f5f5f5",
            fg="#333333",
        )
        label.pack(anchor="w", pady=(0, 5))
        entry = tk.Entry(
            parent, font=("Helvetica", 11), bg="white", relief="solid", bd=1
        )
        entry.pack(fill="x", ipady=8, pady=(0, 10))
        setattr(
            self, entry_name, entry
        )  # Permet d'accéder à l'entry via self.entry_name

    def create_photo_field(
        self, parent
    ):  # Fonction spécifique pour le champ photo avec bouton browse
        photo_label = tk.Label(
            parent, text="Photo:", font=("Helvetica", 12), bg="#f5f5f5", fg="#333333"
        )
        photo_label.pack(anchor="w", pady=(0, 5))

        photo_frame = tk.Frame(
            parent, bg="#f5f5f5"
        )  # Frame pour grouper Entry et Button
        photo_frame.pack(fill="x", pady=(0, 10))

        self.photo_entry = tk.Entry(
            photo_frame, font=("Helvetica", 11), bg="white", relief="solid", bd=1
        )
        self.photo_entry.pack(
            side="left", fill="x", ipady=8, expand=True
        )  # Entry prend l'espace disponible

        photo_button = tk.Button(
            photo_frame,
            text="Browse",
            command=self.browse_photo,
            font=("Helvetica", 11),
            bg="#e0e0e0",
            fg="#333333",
            padx=20,
            pady=10,
            relief="flat",
        )
        photo_button.pack(
            side="left", padx=(10, 0)
        )  # Bouton à droite de l'entry avec un peu d'espace

        photo_button.bind("<Enter>", lambda e, b=photo_button: self.on_hover(b, True))
        photo_button.bind("<Leave>", lambda e, b=photo_button: self.on_hover(b, False))

    def create_category_field(
        self, parent
    ):  # Fonction spécifique pour le champ catégorie (Combobox)
        category_label = tk.Label(
            parent,
            text="Category:",
            font=("Helvetica", 12),
            bg="#f5f5f5",
            fg="#333333",
        )
        category_label.pack(anchor="w", pady=(0, 5))

        self.category_controller = CategoryController()
        categories = self.category_controller.get_all_categories()
        self.category_var = tk.StringVar()
        self.category_combobox = ttk.Combobox(
            parent,
            textvariable=self.category_var,
            font=("Helvetica", 11),
        )
        self.category_combobox["values"] = [category.name for category in categories]
        self.category_combobox.pack(fill="x", ipady=8, pady=(0, 15))

    def create_buttons(self, parent):  # Fonction pour créer les boutons Save et Cancel
        button_frame = tk.Frame(parent, bg="#f5f5f5")
        button_frame.pack(
            fill="x", pady=(20, 0), anchor="s", side="bottom"
        )  #  Ancrage en bas et side bottom pour s'assurer qu'ils sont visibles

        cancel_button = tk.Button(
            button_frame,
            text="Cancel",
            command=self.destroy,
            font=("Helvetica", 11),
            bg="#e0e0e0",
            fg="#333333",
            padx=20,
            pady=10,
            relief="flat",
        )
        cancel_button.pack(side="right", padx=5)

        save_button = tk.Button(
            button_frame,
            text="Save",
            command=self.save,
            font=("Helvetica", 11),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=10,
            relief="flat",
        )
        save_button.pack(side="right", padx=5)

        for btn in (cancel_button, save_button):
            btn.bind("<Enter>", lambda e, b=btn: self.on_hover(b, True))
            btn.bind("<Leave>", lambda e, b=btn: self.on_hover(b, False))

    def on_hover(self, button, hovering):
        if button["text"] == "Cancel" or button["text"] == "Browse":
            button["bg"] = "#d0d0d0" if hovering else "#e0e0e0"
        elif button["text"] == "Save":
            button["bg"] = "#45a049" if hovering else "#4CAF50"

    def browse_photo(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png")]
        )
        if file_path:
            self.photo_entry.delete(0, tk.END)
            self.photo_entry.insert(0, file_path)

    def on_dialog_close(self):
        self.current_dialog = None
        self.destroy()

    def save(self):
        name = self.name_entry.get().strip()
        price = self.price_entry.get().strip()
        quantity = self.quantity_entry.get().strip()
        photo = self.photo_entry.get().strip()
        category_name = self.category_var.get().strip()

        if not os.path.exists("uploads"):
            os.makedirs("uploads")

        if photo:
            filename = os.path.basename(photo)
            destination = os.path.join("uploads", filename)
            try:
                with open(photo, "rb") as source, open(destination, "wb") as dest:
                    dest.write(source.read())
                photo = destination
            except Exception as e:
                messagebox.showerror("Error", f"Error saving photo: {e}", parent=self)
                return

        if not name or not price or not quantity or not category_name:
            messagebox.showwarning("Warning", "All fields are required!", parent=self)
            return

        try:
            price = float(price)
            quantity = int(quantity)
        except ValueError:
            messagebox.showwarning(
                "Warning",
                "Price must be a number and Quantity must be an integer!",
                parent=self,
            )
            return

        category = self.category_controller.get_category_by_name(category_name)
        if not category:
            messagebox.showerror(
                "Error", "Selected category does not exist!", parent=self
            )
            return

        product = Product(
            name=name,
            price=price,
            quantity=quantity,
            photo=photo,
            category_id=category.id,
        )
        if self.controller.create_product(product):
            self.on_add()
            self.current_dialog = None
            self.destroy()
            messagebox.showinfo("Success", "Product added successfully!")
        else:
            messagebox.showerror("Error", "Failed to add product", parent=self)
