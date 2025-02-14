import tkinter as tk
from tkinter import ttk, messagebox, Toplevel, Label
from PIL import Image, ImageTk
import datetime
from styles.colors import *
from styles.theme import Theme
from .add_product_view import AddProductDialog
from controllers.product_controller import ProductController
from .update_products import UpdateProductDialog
from controllers.category_controller import (
    CategoryController,
)


class StockWindow:
    _image_dialog_open = False

    def __init__(self, parent):
        self.parent = parent
        self.theme = Theme()
        self.frame = tk.Frame(self.parent, bg=BG_COLOR)
        self.frame.pack(fill="both", expand=True)

        self.controller = ProductController()
        self.products = {}
        self.all_products = []
        self.images = {}
        self.selected_item_id = None
        self.edit_button = None
        self.delete_button = None
        self.view_image_button = None
        self._add_dialog_open = False

        self.setup_ui()

    def setup_ui(self):
        # --- En-tête de la fenêtre ---
        header = tk.Frame(self.frame, bg=BG_COLOR)
        header.pack(fill="x", padx=20, pady=10)

        title_frame = tk.Frame(header, bg=BG_COLOR)
        title_frame.pack(fill="x", pady=10)
        tk.Label(
            title_frame,
            text="Stock Management",
            font=TITLE_FONT,
            bg=BG_COLOR,
            fg=TEXT_COLOR,
        ).pack(side="left", fill="x", expand=True)

        # Boutons d'actions
        actions_frame = tk.Frame(header, bg=BG_COLOR)
        actions_frame.pack(fill="x", pady=10)

        add_btn = tk.Button(
            actions_frame,
            text="➕ Add Product",
            command=self.show_add_dialog,
            **BUTTON_STYLE,
        )
        add_btn.pack(side="left", padx=5)

        self.edit_button = tk.Button(
            actions_frame,
            text="📝 Edit Product",
            command=self.edit_selected_product,
            state=tk.DISABLED,
            **BUTTON_STYLE,
        )
        self.edit_button.pack(side="left", padx=5)

        self.delete_button = tk.Button(
            actions_frame,
            text="🗑️ Delete Product",
            command=self.delete_selected_product,
            state=tk.DISABLED,
            **{**BUTTON_STYLE, "bg": DANGER_COLOR},
        )
        self.delete_button.pack(side="left", padx=5)

        refresh_btn = tk.Button(
            actions_frame,
            text="🔄 Refresh",
            command=self.refresh_data,
            **{**BUTTON_STYLE, "bg": SECONDARY_COLOR},
        )
        refresh_btn.pack(side="left", padx=5)

        self.view_image_button = tk.Button(
            actions_frame,
            text="🖼️ View Image",
            command=self.show_image_dialog,
            state=tk.DISABLED,
            **BUTTON_STYLE,
        )
        self.view_image_button.pack(side="left", padx=5)

        # --- Section Filtrage par catégorie ---
        self.setup_category_list()

        # --- Table des produits ---
        self.table_container = tk.Frame(self.frame, bg=BG_COLOR)
        self.table_container.pack(fill="both", expand=True, padx=20, pady=10)

        table_frame = tk.Frame(
            self.table_container, bg=SURFACE_COLOR, bd=0, relief="solid"
        )
        table_frame.pack(fill="both", expand=True)

        self.setup_treeview_style()

        self.tree = ttk.Treeview(
            table_frame,
            columns=("ID", "Name", "Category", "Quantity", "Price", "Created At"),
            show="headings",
            height=15,
            style="Custom.Treeview",
        )

        self.tree.heading("ID", text="ID", anchor="center")
        self.tree.heading("Name", text="Name", anchor="center")
        self.tree.heading("Category", text="Category", anchor="center")
        self.tree.heading("Quantity", text="Quantity", anchor="center")
        self.tree.heading("Price", text="Price", anchor="center")
        self.tree.heading("Created At", text="Created At", anchor="center")

        self.tree.column("ID", anchor="center", width=50)
        self.tree.column("Name", anchor="center", width=150)
        self.tree.column("Category", anchor="center", width=100)
        self.tree.column("Quantity", anchor="center", width=100)
        self.tree.column("Price", anchor="center", width=100)
        self.tree.column("Created At", anchor="center", width=150)

        y_scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=y_scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        y_scrollbar.pack(side="right", fill="y")

        # --- Bindings ---
        self.tree.bind("<Motion>", self.on_hover)
        self.tree.tag_configure("hover", background=HOVER_COLOR, foreground="white")
        self.tree.bind("<ButtonRelease-1>", self.on_item_select)

        self.load_data()

    def setup_treeview_style(self):
        style = ttk.Style()
        treeview_style = self.theme.setup_treeview_style()
        style_name = treeview_style.get("style_name", "Custom.Treeview")
        style.configure(style_name, **treeview_style.get("settings", {}))
        heading_style = treeview_style.get("heading_style", {}).copy()
        heading_style.update(
            {"font": ("Helvetica", 11, "bold"), "padding": 8, "relief": "flat"}
        )
        style.configure(f"{style_name}.Heading", **heading_style)
        style.configure(f"{style_name}.Treeview", rowheight=60, borderwidth=0)
        style.map(
            f"{style_name}.Treeview",
            background=[("selected", ACCENT_COLOR)],
            foreground=[("selected", TEXT_COLOR)],
        )

    def setup_category_list(self):
        category_frame = tk.Frame(self.frame, bg=BG_COLOR)
        category_frame.pack(fill="x", padx=20, pady=5)
        tk.Label(
            category_frame,
            text="Filter by Category:",
            font=("Helvetica", 12, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
        ).pack(side="left", padx=(0, 5))
        try:
            category_controller = CategoryController()
            categories = category_controller.get_all_categories()
            category_names = [category.name for category in categories]
        except Exception as e:
            print("Error loading categories:", e)
            category_names = []
        self.category_filter_var = tk.StringVar()
        self.category_filter_combobox = ttk.Combobox(
            category_frame,
            textvariable=self.category_filter_var,
            font=("Helvetica", 11),
            style="FilterCombobox.TCombobox",
        )
        self.category_filter_combobox["values"] = ["All"] + category_names
        self.category_filter_combobox.current(0)
        self.category_filter_combobox.pack(side="left", padx=(0, 5))
        filter_button = tk.Button(
            category_frame,
            text="Filter",
            command=self.filter_by_category,
            **BUTTON_STYLE,
        )
        filter_button.pack(side="left", padx=5)

        # --- Beautiful Style for Combobox ---
        style = ttk.Style(self.parent)
        style.configure(
            "FilterCombobox.TCombobox",
            background=SURFACE_COLOR,
            foreground=TEXT_COLOR,
            borderwidth=0,
            relief="flat",
            padding=(10, 8),
            font=("Helvetica", 11),
        )
        style.map(
            "FilterCombobox.TCombobox",
            background=[("active", HOVER_COLOR), ("focus", ACCENT_COLOR)],
            foreground=[("focus", TEXT_COLOR), ("active", TEXT_COLOR)],
        )

    def filter_by_category(self):
        selected_category = self.category_filter_var.get()
        if selected_category == "All":
            filtered_products = self.all_products
        else:
            filtered_products = []
            for product in self.all_products:
                cat = getattr(product, "category", None)
                cat_name = cat.name if cat and hasattr(cat, "name") else "N/A"
                if cat_name == selected_category:
                    filtered_products.append(product)
        self.display_products(filtered_products)

    def on_item_select(self, event):
        item_id = self.tree.focus()
        if item_id:
            self.selected_item_id = item_id
            self.edit_button.config(state=tk.NORMAL)
            self.delete_button.config(state=tk.NORMAL)
            self.view_image_button.config(state=tk.NORMAL)
        else:
            self.selected_item_id = None
            self.edit_button.config(state=tk.DISABLED)
            self.delete_button.config(state=tk.DISABLED)
            self.view_image_button.config(state=tk.DISABLED)

    def on_hover(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            for row in self.tree.get_children():
                self.tree.item(row, tags=())
            self.tree.item(item, tags=("hover",))

    def show_add_dialog(self):
        if self._add_dialog_open:
            return
        self._add_dialog_open = True
        dialog = AddProductDialog(self.parent, self.controller, self.load_data)
        dialog.bind("<Destroy>", self.reset_add_flag)

    def reset_add_flag(self, event=None):
        self._add_dialog_open = False

    def show_edit_dialog(self, product_object):

        if product_object:
            UpdateProductDialog(
                self.parent,
                product_object,
                on_update=self.handle_update,
                on_delete=lambda product_to_delete=product_object: self.handle_delete(
                    product_to_delete
                ),
            )
        else:
            messagebox.showerror(
                "Error", "Impossible de charger les détails du produit pour l'édition."
            )

    def edit_selected_product(self):
        if self.selected_item_id:
            product_object = self.products.get(self.selected_item_id)
            if product_object:
                self.show_edit_dialog(product_object)

    def delete_selected_product(self):
        if self.selected_item_id:
            product_object = self.products.get(self.selected_item_id)
            if product_object:
                self.handle_delete(product_object)

    def handle_update(self, updated_data):
        try:
            self.controller.update_product(
                updated_data["id"],
                updated_data["name"],
                updated_data["price"],
                updated_data["quantity"],
                updated_data["photo"],
                updated_data["category_id"],
            )
            messagebox.showinfo("Success", "Product updated successfully!")
            self.load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update product: {str(e)}")

    def handle_delete(self, product):
        try:
            if messagebox.askyesno(
                "Confirm Delete", "Are you sure you want to delete this product?"
            ):
                self.controller.delete_product(product.id)
                messagebox.showinfo("Success", "Product deleted successfully!")
                self.load_data()
                self.selected_item_id = None
                self.edit_button.config(state=tk.DISABLED)
                self.delete_button.config(state=tk.DISABLED)
                self.view_image_button.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete product: {str(e)}")

    def refresh_data(self):
        self.load_data()
        self.selected_item_id = None
        self.edit_button.config(state=tk.DISABLED)
        self.delete_button.config(state=tk.DISABLED)
        self.view_image_button.config(state=tk.DISABLED)

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.products.clear()
        self.images.clear()

        products = self.controller.get_all_products()
        self.all_products = products
        self.display_products(products)

    def display_products(self, products):
        for product in products:
            product_image_path = product.photo
            image_for_table = None
            if product_image_path:
                try:
                    img = Image.open(product_image_path)
                    img.thumbnail((50, 50))
                    image_for_table = ImageTk.PhotoImage(img)
                    self.images[product.id] = image_for_table
                except Exception as e:
                    print(f"Error loading image for product {product.id}: {e}")

            created_at = product.created_at
            if created_at:
                if isinstance(created_at, (datetime.datetime, datetime.date)):
                    created_at = created_at.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    created_at = str(created_at)
            else:
                created_at = "N/A"

            cat = getattr(product, "category", None)
            category_name = cat.name if cat and hasattr(cat, "name") else "N/A"

            item = self.tree.insert("", "end")
            self.tree.set(item, "ID", str(product.id))
            self.tree.set(item, "Name", str(product.name))
            self.tree.set(item, "Category", category_name)
            self.tree.set(item, "Quantity", str(product.quantity))
            self.tree.set(item, "Price", str(product.price))
            self.tree.set(item, "Created At", created_at)

            self.products[item] = product

    def show_image_dialog(self):
        if StockWindow._image_dialog_open:
            return
        if self.selected_item_id:
            product_data = self.products.get(self.selected_item_id)
            if product_data:
                StockWindow._image_dialog_open = True
                ImageViewDialog(self.parent, product_data)

    def destroy(self):
        self.frame.destroy()


class ImageViewDialog(Toplevel):
    def __init__(self, parent, product_data):
        super().__init__(parent)
        self.withdraw()
        self.title(f"Image Viewer - Product ID: {product_data.id}")
        self.product_data = product_data
        self.protocol("WM_DELETE_WINDOW", self.close_dialog)
        self.setup_ui()
        self.center_window()
        self.deiconify()

    def setup_ui(self):
        container = tk.Frame(self, padx=20, pady=20)
        container.pack(fill="both", expand=True)
        image_path = self.product_data.photo
        image_display = None
        if image_path:
            try:
                img = Image.open(image_path)
                img.thumbnail((300, 300))
                image_display = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Error loading image for dialog: {e}")
                image_path = None
        if image_display:
            image_label = Label(container, image=image_display)
            image_label.image = image_display
            image_label.pack(pady=10)
        else:
            no_image_label = Label(container, text="No Image Available", fg="grey")
            no_image_label.pack(pady=10)

        details_frame = tk.Frame(container)
        details_frame.pack(fill="x")
        tk.Label(details_frame, text="ID:", font=("Helvetica", 10, "bold")).grid(
            row=0, column=0, sticky="e", padx=5, pady=2
        )
        tk.Label(details_frame, text=str(self.product_data.id)).grid(
            row=0, column=1, sticky="w", padx=5, pady=2
        )
        tk.Label(details_frame, text="Name:", font=("Helvetica", 10, "bold")).grid(
            row=1, column=0, sticky="e", padx=5, pady=2
        )
        tk.Label(details_frame, text=self.product_data.name).grid(
            row=1, column=1, sticky="w", padx=5, pady=2
        )
        tk.Label(details_frame, text="Quantity:", font=("Helvetica", 10, "bold")).grid(
            row=2, column=0, sticky="e", padx=5, pady=2
        )
        tk.Label(details_frame, text=str(self.product_data.quantity)).grid(
            row=2, column=1, sticky="w", padx=5, pady=2
        )
        tk.Label(details_frame, text="Price:", font=("Helvetica", 10, "bold")).grid(
            row=3, column=0, sticky="e", padx=5, pady=2
        )
        tk.Label(details_frame, text=str(self.product_data.price)).grid(
            row=3, column=1, sticky="w", padx=5, pady=2
        )

        created_at_str = self.product_data.created_at
        if isinstance(created_at_str, (datetime.datetime, datetime.date)):
            created_at_str = created_at_str.strftime("%Y-%m-%d %H:%M:%S")
        elif created_at_str is None:
            created_at_str = "N/A"
        else:
            created_at_str = str(created_at_str)
        tk.Label(
            details_frame, text="Created At:", font=("Helvetica", 10, "bold")
        ).grid(row=4, column=0, sticky="e", padx=5, pady=2)
        tk.Label(details_frame, text=created_at_str).grid(
            row=4, column=1, sticky="w", padx=5, pady=2
        )

    def close_dialog(self):
        StockWindow._image_dialog_open = False
        self.destroy()

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"+{x}+{y}")


# ----- Code de test (Mock) -----
# if __name__ == "__main__":

#     class MockCategory:
#         def __init__(self, name):
#             self.name = name

#     class MockProduct:
#         def __init__(self, id, name, quantity, price, photo, created_at, category=None):
#             self.id = id
#             self.name = name
#             self.quantity = quantity
#             self.price = price
#             self.photo = photo
#             self.created_at = created_at
#             self.category = category

#     class MockProductController:
#         def get_all_products(self):
#             products = []
#             categories = [MockCategory("Electronics"), MockCategory("Books")]
#             for i in range(5):
#                 cat = categories[i % 2]
#                 products.append(
#                     MockProduct(
#                         id=i + 1,
#                         name=f"Product {i+1}",
#                         quantity=10 * (i + 1),
#                         price=25.99 * (i + 1),
#                         photo=("path/to/your/image.png" if i % 2 == 0 else None),
#                         created_at=datetime.datetime.now() - datetime.timedelta(days=i),
#                         category=cat,
#                     )
#                 )
#             return products

#         def delete_product(self, product_id):
#             print(f"Mock delete product {product_id}")

#         def update_product(self, *args):
#             print(f"Mock update product with args: {args}")

#     class MockAddProductDialog(tk.Toplevel):
#         def __init__(self, parent, controller, on_add):
#             super().__init__(parent)
#             self.controller = controller
#             self.on_add = on_add
#             self.title("Add Product")
#             self.geometry("500x630")
#             self.resizable(False, False)
#             self.transient(parent)
#             self.after(100, lambda: self.grab_set())
#             self.protocol("WM_DELETE_WINDOW", self.on_dialog_close)
#             tk.Label(self, text="Mock Add Product Dialog").pack(pady=20)

#         def on_dialog_close(self):
#             self.destroy()

#     class MockUpdateProductDialog:
#         def __init__(self, parent, product, on_update, on_delete):
#             print(f"Mock UpdateProductDialog created for product {product}")

#     ProductController = MockProductController
#     AddProductDialog = MockAddProductDialog
#     UpdateProductDialog = MockUpdateProductDialog

#     root = tk.Tk()
#     root.title("Stock Management Mock Test")
#     stock_window = StockWindow(root)
#     root.mainloop()
