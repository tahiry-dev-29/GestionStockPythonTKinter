import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from styles.colors import *
from styles.theme import Theme


class UpdateProductDialog:
    def __init__(self, parent, product_data, on_update, on_delete):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Update Product")
        self.theme = Theme.get_dialog_style()
        self.dialog.geometry("500x550")
        self.dialog.resizable(False, False)
        self.dialog.configure(bg="#f5f5f5")
        self.dialog.transient(parent)
        self.dialog.update_idletasks()
        self.dialog.grab_set()

        self.product_data = product_data
        self.on_update = on_update
        self.on_delete = on_delete
        self.image = None  # Pour stocker l'image du produit
        self.setup_ui()

    def setup_ui(self):
        container = tk.Frame(self.dialog, bg="#f5f5f5")
        container.pack(fill="both", expand=True, padx=30, pady=30)

        tk.Label(
            container,
            text="Update Product Information",
            font=("Helvetica", 18, "bold"),
            bg="#f5f5f5",
            fg="#333333",
        ).pack(pady=(0, 20))

        # Afficher l'image du produit si disponible
        if "image" in self.product_data and self.product_data["image"]:
            try:
                img = Image.open(self.product_data["image"])
                img = img.resize((150, 150), Image.LANCZOS)  # 🔹 Taille fixe
                self.image = ImageTk.PhotoImage(img)
                image_label = tk.Label(container, image=self.image, bg="#f5f5f5")
                image_label.pack(pady=(0, 20))
            except Exception as e:
                print(f"Error loading image: {e}")

        self.create_form(container)

    def create_form(self, parent):
        # Initialisation des variables avec les données existantes du produit
        self.name_var = tk.StringVar(value=self.product_data["name"])
        self.quantity_var = tk.StringVar(value=str(self.product_data["quantity"]))
        self.price_var = tk.StringVar(value=str(self.product_data["price"]))

        form = tk.Frame(parent, bg="#f5f5f5")
        form.pack(fill="x", pady=10)

        # Champ Product Name
        self.create_field(form, "Product Name:", self.name_var)

        # 🔹 Frame pour regrouper Quantity & Price sur une seule ligne
        row_frame = tk.Frame(form, bg="#f5f5f5")
        row_frame.pack(fill="x", pady=10)

        self.create_field(
            row_frame, "Quantity:", self.quantity_var, side="left", expand=True
        )
        self.create_field(
            row_frame, "Price:", self.price_var, side="right", expand=True
        )

        self.create_buttons(form)

    def create_field(self, parent, label, variable, side=None, expand=False):
        frame = tk.Frame(parent, bg="#f5f5f5")
        if side:
            frame.pack(side=side, expand=expand, fill="x", padx=5)
        else:
            frame.pack(fill="x", pady=10)

        tk.Label(
            frame, text=label, font=("Helvetica", 12), bg="#f5f5f5", fg="#333333"
        ).pack(anchor="w", pady=(0, 5))

        entry = tk.Entry(
            frame,
            textvariable=variable,
            font=("Helvetica", 11),
            bg="white",
            relief="solid",
            bd=1,
        )
        entry.pack(fill="x", ipady=8)

    def create_buttons(self, parent):
        button_frame = tk.Frame(parent, bg="#f5f5f5")
        button_frame.pack(fill="x", pady=(30, 0))

        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=self.dialog.destroy,
            font=("Helvetica", 11),
            bg="#e0e0e0",
            fg="#333333",
            padx=20,
            pady=10,
            relief="flat",
        )
        cancel_btn.pack(side="right", padx=5)

        delete_btn = tk.Button(
            button_frame,
            text="Delete",
            command=self.delete_product,
            font=("Helvetica", 11),
            bg="#ff4444",
            fg="white",
            padx=20,
            pady=10,
            relief="flat",
        )
        delete_btn.pack(side="right", padx=5)

        update_btn = tk.Button(
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
        update_btn.pack(side="right", padx=5)

        for btn in (cancel_btn, delete_btn, update_btn):
            btn.bind("<Enter>", lambda e, b=btn: self.on_hover(b, True))
            btn.bind("<Leave>", lambda e, b=btn: self.on_hover(b, False))

    def on_hover(self, button, hovering):
        if button["text"] == "Cancel":
            button["bg"] = "#d0d0d0" if hovering else "#e0e0e0"
        elif button["text"] == "Delete":
            button["bg"] = "#ff3333" if hovering else "#ff4444"
        else:  # Update button
            button["bg"] = "#45a049" if hovering else "#4CAF50"

    def update_product(self):
        if not self.validate_form():
            return

        updated_data = {
            "id": self.product_data["id"],
            "name": self.name_var.get().strip(),
            "quantity": self.quantity_var.get().strip(),
            "price": self.price_var.get().strip(),
            "image": self.product_data.get("image", None),
        }
        self.on_update(updated_data)
        self.dialog.destroy()

    def delete_product(self):
        if messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete product {self.product_data['name']}?",
        ):
            try:
                self.on_delete()
                self.dialog.destroy()
            except Exception as e:
                messagebox.showinfo("Success", "Product deleted successfully!")
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
