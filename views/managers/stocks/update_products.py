import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from controllers.category_controller import CategoryController
from styles.colors import *
from styles.theme import Theme


class UpdateProductDialog:
    def __init__(self, parent, product_data, on_update, on_delete):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Update Product")
        self.theme = Theme.get_dialog_style()
        self.dialog.geometry("500x600")
        self.dialog.resizable(False, False)
        self.dialog.configure(bg="#f5f5f5")
        self.dialog.transient(parent)
        self.dialog.update_idletasks()
        self.dialog.grab_set()

        self.product_data = product_data
        self.on_update = on_update
        self.on_delete = on_delete  # Keep on_delete, in case delete functionality is needed elsewhere later
        self.image = None
        self.image_label = None
        self.image_path = self.product_data.get("image", None)

        self.category_controller = CategoryController()

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
                self.image_label.image = img_tk  # Keep a reference
            else:
                self.image_label = tk.Label(self.container, image=img_tk, bg="#f5f5f5")
                self.image_label.pack(pady=(0, 20))
                self.image_label.image = img_tk  # Keep a reference

            self.image = img_tk  # Store the image so it's not garbage collected
        except Exception as e:
            messagebox.showerror("Error", f"Error displaying image: {e}")

    def create_form(self, parent):
        self.name_var = tk.StringVar(value=self.product_data["name"])
        self.quantity_var = tk.StringVar(value=str(self.product_data["quantity"]))
        self.price_var = tk.StringVar(value=str(self.product_data["price"]))

        form = tk.Frame(parent, bg="#f5f5f5")
        form.pack(fill="x", pady=10)

        # Product Name & Category on the same row
        row_frame_name_category = tk.Frame(form, bg="#f5f5f5")
        row_frame_name_category.pack(fill="x", pady=10)

        # Nom du produit
        self.create_field(
            row_frame_name_category,
            "Product Name:",
            self.name_var,
            side="left",
            expand=True,
        )

        # Catégorie en dropdown
        self.create_category_field(row_frame_name_category, side="right", expand=True)

        # Prix & Quantité sur la même ligne
        row_frame = tk.Frame(form, bg="#f5f5f5")
        row_frame.pack(fill="x", pady=10)

        self.create_field(
            row_frame, "Quantity:", self.quantity_var, side="left", expand=True
        )
        self.create_field(
            row_frame, "Price:", self.price_var, side="right", expand=True
        )

        # Bouton pour choisir une image
        browse_btn = tk.Button(
            form,
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

        self.create_buttons(form)

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

        categories = self.category_controller.get_all_categories()
        self.category_var = tk.StringVar(
            value=self.product_data["category"]
        )  # Sélectionne la catégorie actuelle
        self.category_combobox = ttk.Combobox(
            frame, textvariable=self.category_var, font=("Helvetica", 11)
        )
        self.category_combobox["values"] = [category.name for category in categories]
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
            self.image_path = file_path  # Update image path
            self.show_image_preview(file_path)  # Directly call the existing function

    def create_buttons(self, parent):
        button_frame = tk.Frame(parent, bg="#f5f5f5")
        button_frame.pack(fill="x", pady=(20, 0))

        # Cancel Button instead of Delete
        cancel_button = tk.Button(
            button_frame,
            text="Cancel",
            command=self.dialog.destroy,  # Simply destroy the dialog
            font=("Helvetica", 11),
            bg="#AAAAAA",  # Grey color for cancel button
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
        if self.validate_form():  # Validate before updating
            updated_data = {
                "name": self.name_var.get().strip(),
                "quantity": int(self.quantity_var.get().strip()),
                "price": float(self.price_var.get().strip()),
                "category": self.category_var.get().strip(),
                "image": self.image_path,  # Use the updated image path
            }
            self.on_update(updated_data)
            self.dialog.destroy()
            messagebox.showinfo("Success", "Product updated successfully!")

    def delete_product(
        self,
    ):  # Keep delete_product function, but not used on button anymore
        if messagebox.askyesno(
            "Confirm", "Are you sure you want to delete this product?"
        ):
            self.on_delete(self.product_data)
            self.dialog.destroy()

    def validate_form(self):
        if not self.name_var.get().strip():
            messagebox.showerror("Error", "Product name is required")
            return False
        if not self.quantity_var.get().strip():
            messagebox.showerror("Error", "Quantity is required")
            return False
        if not self.price_var.get().strip():
            messagebox.showerror("Error", "Price is required")
            return False
        try:
            int(self.quantity_var.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Quantity must be an integer")
            return False
        try:
            float(self.price_var.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Price must be a number")
            return False
        return True
