import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from controllers.category_controller import CategoryController
from styles.colors import *
from styles.theme import (
    Theme,
)


class UpdateProductDialog:
    def __init__(self, parent, product, on_update, on_delete):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Update Product")
        self.theme = Theme.get_dialog_style()
        self.dialog.geometry("500x600")
        self.dialog.resizable(False, False)
        self.dialog.configure(bg="#f5f5f5")
        self.dialog.transient(parent)
        self.dialog.update_idletasks()
        self.dialog.grab_set()

        self.product = product
        self.on_update = on_update
        self.on_delete = on_delete
        self.image = None
        self.image_label = None
        self.image_path = self.product.photo if self.product.photo else None

        self.category_controller = CategoryController()
        self.categories = self.category_controller.get_all_categories()

        self.setup_ui()

    def setup_ui(self):
        self.container = tk.Frame(self.dialog, bg="#f5f5f5")
        self.container.pack(fill="both", expand=True, padx=30, pady=30)

        tk.Label(
            self.container,
            text="Update Product Information",
            font=("Helvetica", 18, "bold"),
            bg="#f5f5f5",
            fg="#333333",
        ).pack(pady=(0, 20))

        self.create_image_preview()
        self.create_form(self.container)

    def create_image_preview(self):
        if self.image_path:
            try:
                self.show_image_preview(self.image_path)
            except Exception as e:
                print(f"Error loading image: {e}")

    def show_image_preview(self, image_path):
        try:
            img = Image.open(image_path)
            fixed_height = 150
            img_width, img_height = img.size
            ratio = fixed_height / img_height
            new_width = int(img_width * ratio)
            img = img.resize((new_width, fixed_height), Image.LANCZOS)

            img_tk = ImageTk.PhotoImage(img)

            if self.image_label:
                self.image_label.configure(image=img_tk)
                self.image_label.image = img_tk
            else:
                self.image_label = tk.Label(self.container, image=img_tk, bg="#f5f5f5")
                self.image_label.pack(pady=(0, 20))
                self.image_label.image = img_tk
            self.image = img_tk
        except Exception as e:
            messagebox.showerror("Error", f"Erreur d'affichage de l'image: {e}")

    def create_form(self, parent):
        self.form_frame = tk.Frame(parent, bg="#f5f5f5")
        self.form_frame.pack(fill="x", pady=10)

        self.name_var = tk.StringVar(value=self.product.name)
        self.quantity_var = tk.StringVar(value=str(self.product.quantity))
        self.price_var = tk.StringVar(value=str(self.product.price))

        row_frame_name_category = tk.Frame(self.form_frame, bg="#f5f5f5")
        row_frame_name_category.pack(fill="x", pady=10)

        self.create_field(
            row_frame_name_category,
            "Product Name:",
            self.name_var,
            side="left",
            expand=True,
        )

        # Catégorie en dropdown
        self.create_category_field(row_frame_name_category, side="right", expand=True)

        row_frame = tk.Frame(self.form_frame, bg="#f5f5f5")
        row_frame.pack(fill="x", pady=10)

        self.create_field(
            row_frame, "Quantity:", self.quantity_var, side="left", expand=True
        )
        self.create_field(
            row_frame, "Price:", self.price_var, side="right", expand=True
        )

        browse_btn = tk.Button(
            self.form_frame,
            text="Browse Image",
            command=self.browse_image,
            font=("Helvetica", 11),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=10,
            relief="flat",
        )
        browse_btn.pack(fill="x", pady=10)

        self.create_buttons(self.form_frame)

    def create_category_field(self, parent, side=None, expand=False):
        frame = tk.Frame(parent, bg="#f5f5f5")
        if side:
            frame.pack(side=side, expand=expand, fill="x", padx=5)
        else:
            frame.pack(fill="x", pady=10)

        tk.Label(
            frame,
            text="Category:",
            font=("Helvetica", 12),
            bg="#f5f5f5",
            fg="#333333",
        ).pack(anchor="w")

        category_names = [category.name for category in self.categories]
        current_category_name = (
            self.product.category.name
            if hasattr(self.product, "category") and self.product.category
            else ""
        )

        self.category_var = tk.StringVar(value=current_category_name)
        self.category_combobox = ttk.Combobox(
            frame,
            textvariable=self.category_var,
            font=("Helvetica", 11),
            values=category_names,
        )
        self.category_combobox.pack(fill="x", ipady=8, pady=(0, 5))

    def create_field(self, parent, label, variable, side=None, expand=False):
        frame = tk.Frame(parent, bg="#f5f5f5")
        if side:
            frame.pack(side=side, expand=expand, fill="x", padx=5)
        else:
            frame.pack(fill="x", pady=10)

        tk.Label(
            frame, text=label, font=("Helvetica", 12), bg="#f5f5f5", fg="#333333"
        ).pack(anchor="w")

        entry = tk.Entry(
            frame,
            textvariable=variable,
            font=("Helvetica", 11),
            bg="white",
            relief="solid",
            bd=1,
        )
        entry.pack(fill="x", ipady=8, pady=(0, 5))

    def browse_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp")],
        )
        if file_path:
            self.image_path = file_path
            self.show_image_preview(file_path)

    def create_buttons(self, parent):
        button_frame = tk.Frame(parent, bg="#f5f5f5")
        button_frame.pack(fill="x", pady=(20, 0))

        cancel_button = tk.Button(
            button_frame,
            text="Cancel",
            command=self.dialog.destroy,
            font=("Helvetica", 11),
            bg="#AAAAAA",
            fg="white",
            padx=20,
            pady=10,
            relief="flat",
        )
        cancel_button.pack(side="left", padx=5)

        update_button = tk.Button(
            button_frame,
            text="Update",
            command=self.update_product,
            font=("Helvetica", 11),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=10,
            relief="flat",
        )
        update_button.pack(side="right", padx=5)

    def update_product(self):
        if self.validate_form():
            selected_category_name = self.category_var.get()
            selected_category = next(
                (cat for cat in self.categories if cat.name == selected_category_name),
                None,
            )
            if not selected_category:
                messagebox.showerror("Error", "Catégorie invalide sélectionnée.")
                return

            updated_data = {
                "id": self.product.id,
                "name": self.name_var.get().strip(),
                "quantity": int(self.quantity_var.get().strip()),
                "price": float(self.price_var.get().strip()),
                "category_id": selected_category.id,
                "photo": self.image_path,
            }
            self.on_update(updated_data)
            self.dialog.destroy()
            messagebox.showinfo("Succès", "Produit mis à jour avec succès !")

    def delete_product(self):
        if messagebox.askyesno(
            "Confirmation",
            "Êtes-vous sûr de vouloir supprimer ce produit ?",
        ):
            self.on_delete(self.product.id)
            self.dialog.destroy()

    def validate_form(self):
        if not self.name_var.get().strip():
            messagebox.showerror("Erreur", "Le nom du produit est obligatoire")
            return False
        if not self.quantity_var.get().strip():
            messagebox.showerror("Erreur", "La quantité est obligatoire")
            return False
        if not self.price_var.get().strip():
            messagebox.showerror("Erreur", "Le prix est obligatoire")
            return False
        try:
            int(self.quantity_var.get().strip())
        except ValueError:
            messagebox.showerror("Erreur", "La quantité doit être un entier")
            return False
        try:
            float(self.price_var.get().strip())
        except ValueError:
            messagebox.showerror("Erreur", "Le prix doit être un nombre")
            return False
        return True
