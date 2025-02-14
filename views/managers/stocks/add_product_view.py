import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk

from controllers.category_controller import CategoryController
from models.product import Product


class AddProductDialog(tk.Toplevel):
    def __init__(self, parent, controller, on_add):
        super().__init__(parent)
        self.controller = controller
        self.on_add = on_add

        self.configure(bg="#f9f9f9")
        self.title("Add Product")
        self.geometry("500x630")
        self.resizable(False, False)

        # Pour que la fenêtre soit toujours au-dessus de la fenêtre parente
        self.transient(parent)
        self.after(100, lambda: self.grab_set())
        self.protocol("WM_DELETE_WINDOW", self.on_dialog_close)

        self.image_path = None
        self.setup_ui()

    def on_dialog_close(self):
        """Ferme proprement la boîte de dialogue."""
        self.destroy()

    def setup_ui(self):
        """Configure la disposition générale de la fenêtre."""
        container = tk.Frame(self, bg="#f9f9f9", padx=30, pady=30)
        container.pack(fill="both", expand=True)

        self.create_title_label(container)
        self.create_form(container)
        self.create_buttons(container)

    def create_title_label(self, parent):
        """Crée et place le titre de la fenêtre."""
        tk.Label(
            parent,
            text="Add New Product",
            font=("Helvetica", 18, "bold"),
            bg="#f9f9f9",
            fg="#333333",
        ).pack(pady=(0, 20))

    def create_form(self, parent):
        """Crée le formulaire (champs, combobox, etc.)."""
        form_frame = tk.Frame(parent, bg="#f9f9f9")
        form_frame.pack(fill="x", pady=10)
        self.create_form_fields(form_frame)

    def create_form_fields(self, parent):
        """Crée les champs du formulaire : Nom, Catégorie, Prix, Quantité, Photo."""
        # Ligne 1 : Nom et Catégorie
        row1 = tk.Frame(parent, bg="#f9f9f9")
        row1.pack(fill="x", pady=5)
        self.create_field(row1, "Product Name:", "name_entry", side="left")
        self.create_category_field(row1, side="right")

        row2 = tk.Frame(parent, bg="#f9f9f9")
        row2.pack(fill="x", pady=5)
        self.create_field(row2, "Price:", "price_entry", side="left")
        self.create_field(row2, "Quantity:", "quantity_entry", side="right")

        # Champ Photo et aperçu
        self.create_photo_field(parent)
        self.create_image_preview(parent)

    def create_field(self, parent, label_text, entry_name, side="top"):
        """
        Crée un champ (Label + Entry).
        - label_text : Texte du label.
        - entry_name : Nom de l'attribut de la classe pour l'Entry.
        - side : Positionnement dans le parent (left, right, top, etc.).
        """
        field_frame = tk.Frame(parent, bg="#f9f9f9")
        field_frame.pack(fill="x", side=side, expand=True, padx=5)

        label = tk.Label(
            field_frame,
            text=label_text,
            font=("Helvetica", 12),
            bg="#f9f9f9",
            fg="#333333",
        )
        label.pack(anchor="w")

        entry = tk.Entry(
            field_frame, font=("Helvetica", 11), bg="white", relief="solid", bd=1
        )
        entry.pack(fill="x", ipady=8, pady=(0, 5))
        entry.config(borderwidth=2, relief="solid", highlightthickness=0)
        setattr(self, entry_name, entry)

    def create_category_field(self, parent, side="top"):
        """Crée un champ de sélection pour la catégorie."""
        field_frame = tk.Frame(parent, bg="#f9f9f9")
        field_frame.pack(fill="x", side=side, expand=True, padx=5)

        label = tk.Label(
            field_frame,
            text="Category:",
            font=("Helvetica", 12),
            bg="#f9f9f9",
            fg="#333333",
        )
        label.pack(anchor="w")

        self.category_controller = CategoryController()
        categories = self.category_controller.get_all_categories()
        self.category_var = tk.StringVar()
        self.category_combobox = ttk.Combobox(
            field_frame, textvariable=self.category_var, font=("Helvetica", 11)
        )
        self.category_combobox["values"] = [category.name for category in categories]
        self.category_combobox.pack(fill="x", ipady=8, pady=(0, 5))

    def create_photo_field(self, parent):
        """Crée le champ pour sélectionner la photo."""
        photo_label = tk.Label(
            parent, text="Photo:", font=("Helvetica", 12), bg="#f9f9f9", fg="#333333"
        )
        photo_label.pack(anchor="w", pady=(0, 5))

        photo_frame = tk.Frame(parent, bg="#f9f9f9")
        photo_frame.pack(fill="x", pady=(0, 10))

        self.photo_entry = tk.Entry(
            photo_frame, font=("Helvetica", 11), bg="white", relief="solid", bd=1
        )
        self.photo_entry.pack(side="left", fill="x", ipady=8, expand=True)

        photo_button = tk.Button(
            photo_frame,
            text="Browse",
            command=self.browse_photo,
            font=("Helvetica", 11),
            bg="#7C7C7C",
            fg="white",
            padx=20,
            pady=10,
            relief="flat",
        )
        photo_button.pack(side="left", padx=(10, 0))

    def create_image_preview(self, parent):
        """Crée la zone d'aperçu de l'image."""
        self.image_preview_frame = tk.Frame(parent, bg="#f9f9f9")
        self.image_preview_frame.pack(fill="both", expand=True, pady=(10, 20))

        self.image_preview_label = tk.Label(
            self.image_preview_frame, bg="white", relief="solid", bd=1
        )
        self.image_preview_label.pack(pady=10)

    def browse_photo(self):
        """Ouvre un dialogue pour sélectionner une photo et lance l'aperçu."""
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png")]
        )
        if file_path:
            self.image_path = file_path
            self.photo_entry.delete(0, tk.END)
            self.photo_entry.insert(0, file_path)
            self.show_image_preview(file_path)

    def show_image_preview(self, image_path):
        """
        Affiche l'image avec une hauteur fixe de 150px.
        La largeur est ajustée pour préserver le ratio original.
        """
        try:
            img = Image.open(image_path)
            fixed_height = 150
            img_width, img_height = img.size

            ratio = fixed_height / img_height
            new_height = fixed_height
            new_width = int(img_width * ratio)

            img = img.resize((new_width, new_height), resample=Image.LANCZOS)

            img_tk = ImageTk.PhotoImage(img)
            self.image_preview_label.configure(image=img_tk)
            self.image_preview_label.image = img_tk

        except Exception as e:
            messagebox.showerror("Error", f"Error displaying image: {e}")

    def create_buttons(self, parent):
        """Crée les boutons de validation et d'annulation."""
        button_frame = tk.Frame(parent, bg="#f9f9f9")
        button_frame.pack(fill="x", pady=(20, 0))

        cancel_button = tk.Button(
            button_frame,
            text="Cancel",
            command=self.destroy,
            font=("Helvetica", 11),
            bg="#f9f9f9",
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

    def save(self):
        """
        Valide les champs, crée un objet Product et le transmet au contrôleur.
        Affiche un message de succès ou d'erreur selon le résultat.
        """
        name = self.name_entry.get().strip()
        price = self.price_entry.get().strip()
        quantity = self.quantity_entry.get().strip()
        photo = self.image_path
        category_name = self.category_var.get().strip()

        # Vérification que tous les champs sont remplis
        if not name or not price or not quantity or not category_name:
            messagebox.showwarning("Warning", "All fields are required!")
            return

        try:
            price = float(price)
            quantity = int(quantity)
        except ValueError:
            messagebox.showwarning(
                "Warning", "Price must be a number and Quantity must be an integer!"
            )
            return

        category = self.category_controller.get_category_by_name(category_name)
        if not category:
            messagebox.showerror("Error", "Selected category does not exist!")
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
            self.destroy()
            messagebox.showinfo("Success", "Product added successfully!")
        else:
            messagebox.showerror("Error", "Failed to add product")
