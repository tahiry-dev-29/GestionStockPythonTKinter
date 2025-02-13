import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from styles.colors import *
from styles.theme import Theme
from .add_product_view import AddProductDialog
from controllers.product_controller import ProductController
from .update_products import UpdateProductDialog


class StockWindow:
    def __init__(self, parent):
        self.parent = parent
        self.theme = Theme()  # Pour garder un style cohérent
        self.frame = tk.Frame(self.parent, bg=BG_COLOR)
        self.frame.pack(fill="both", expand=True)

        self.controller = ProductController()
        self.products = {}  # Stocke les données des produits par item id
        self.images = (
            {}
        )  # Stocke les images pour éviter leur suppression par le garbage collector
        self.selected_item_id = None  # Pour suivre l'item sélectionné
        self.edit_button = None
        self.delete_button = None
        self.setup_ui()

    def setup_ui(self):
        # --- En-tête de la fenêtre ---
        header = tk.Frame(self.frame, bg=BG_COLOR)
        header.pack(fill="x", padx=20, pady=10)

        title_frame = tk.Frame(header, bg=BG_COLOR)
        title_frame.pack(side="left", pady=10)
        tk.Label(
            title_frame,
            text="Stock Management",
            font=TITLE_FONT,
            bg=BG_COLOR,
            fg=TEXT_COLOR,
        ).pack(side="left")

        # Boutons d'action : Ajouter, Editer, Supprimer et Rafraîchir
        actions_frame = tk.Frame(header, bg=BG_COLOR)
        actions_frame.pack(side="right", pady=10)

        add_btn = tk.Button(
            actions_frame,
            text="➕ Add New Product",
            command=self.show_add_dialog,
            **BUTTON_STYLE,
        )
        add_btn.pack(side="left", padx=5)

        self.edit_button = tk.Button(
            actions_frame,
            text="✏️ Edit Product",
            command=self.edit_selected_product,
            state=tk.DISABLED,  # Désactivé par défaut
            **BUTTON_STYLE,
        )
        self.edit_button.pack(side="left", padx=5)

        self.delete_button = tk.Button(
            actions_frame,
            text="🗑️ Delete Product",
            command=self.delete_selected_product,
            state=tk.DISABLED,  # Désactivé par défaut
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

        # --- Configuration de la table ---
        self.table_container = tk.Frame(self.frame, bg=BG_COLOR)
        self.table_container.pack(fill="both", expand=True, padx=20, pady=10)

        # On encapsule la table dans un frame avec fond blanc et bordure
        table_frame = tk.Frame(self.table_container, bg="white", bd=1, relief="solid")
        table_frame.pack(fill="both", expand=True)

        self.setup_treeview_style()

        # Utilisation de la colonne "tree" (#0) pour afficher l'image et le nom du produit
        self.tree = ttk.Treeview(
            table_frame,
            columns=("ID", "Quantity", "Price"),
            show="tree headings",  # Affiche la colonne tree (#0) ET les colonnes définies
            height=15,
        )
        # Configuration de la colonne "tree" qui affichera l'image ET le nom du produit
        self.tree.heading("#0", text="Product")
        self.tree.column("#0", width=200, anchor="w")

        # Configuration des colonnes supplémentaires
        self.tree.heading("ID", text="ID")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Price", text="Price")

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Quantity", width=100, anchor="center")
        self.tree.column("Price", width=100, anchor="center")

        # Ajout de la scrollbar verticale
        y_scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=y_scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        y_scrollbar.pack(side="right", fill="y")

        # --- Bindings pour les interactions ---
        self.tree.bind("<Motion>", self.on_hover)
        self.tree.tag_configure("hover", background="#E3F2FD")
        self.tree.bind("<ButtonRelease-1>", self.on_item_select)  # Capture la sélection

        self.load_data()

    def setup_treeview_style(self):
        style = ttk.Style()
        treeview_style = self.theme.setup_treeview_style()
        style_name = treeview_style.get("style_name", "Custom.Treeview")

        style.configure(style_name, **treeview_style.get("settings", {}))

        heading_style = treeview_style.get("heading_style", {}).copy()
        heading_style.update({"font": ("Helvetica", 11, "bold"), "padding": 10})
        style.configure(f"{style_name}.Heading", **heading_style)

        style.configure(f"{style_name}.Treeview", rowheight=35, borderwidth=0)

        style.map(
            f"{style_name}.Treeview",
            background=[("selected", "#2196F3")],
            foreground=[("selected", "white")],
        )

    def on_item_select(self, event):
        item_id = self.tree.focus()
        if item_id:
            self.selected_item_id = item_id
            self.edit_button.config(state=tk.NORMAL)
            self.delete_button.config(state=tk.NORMAL)
        else:
            self.selected_item_id = None
            self.edit_button.config(state=tk.DISABLED)
            self.delete_button.config(state=tk.DISABLED)

    def on_hover(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            for row in self.tree.get_children():
                self.tree.item(row, tags=())
            self.tree.item(item, tags=("hover",))

    def show_add_dialog(self):
        AddProductDialog(self.parent, self.controller, self.load_data)

    def show_edit_dialog(self, product):
        UpdateProductDialog(
            self.parent,
            product,
            on_update=self.handle_update,
            on_delete=lambda: self.handle_delete(product),
        )

    def edit_selected_product(self):
        if self.selected_item_id:
            product = self.products.get(self.selected_item_id)
            if product:
                self.show_edit_dialog(product)

    def delete_selected_product(self):
        if self.selected_item_id:
            product = self.products.get(self.selected_item_id)
            if product:
                self.handle_delete(product)

    def handle_update(self, updated_product):
        try:
            self.controller.update_product(updated_product)
            messagebox.showinfo("Success", "Product updated successfully!")
            self.load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update product: {str(e)}")

    def handle_delete(self, product):
        try:
            if messagebox.askyesno(
                "Confirm Delete", "Are you sure you want to delete this product?"
            ):
                self.controller.delete_product(product["id"])
                messagebox.showinfo("Success", "Product deleted successfully!")
                self.load_data()
                self.selected_item_id = None  # Reset selection
                self.edit_button.config(state=tk.DISABLED)  # Disable buttons
                self.delete_button.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete product: {str(e)}")

    def refresh_data(self):
        self.load_data()
        self.selected_item_id = None  # Reset selection on refresh too
        self.edit_button.config(state=tk.DISABLED)
        self.delete_button.config(state=tk.DISABLED)

    def load_data(self):
        # Effacer les anciennes données
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.products.clear()
        self.images.clear()

        products = self.controller.get_all_products()
        for product in products:
            # Charger l'image du produit si disponible (le chemin de l'image doit être dans product.image)
            image = None
            # Utilisation de getattr pour éviter l'erreur si l'attribut "image" n'existe pas
            product_image = getattr(product, "image", None)
            if product_image:
                try:
                    img = Image.open(product_image)
                    img.thumbnail((50, 50))
                    image = ImageTk.PhotoImage(img)
                    self.images[product.id] = image  # Conserver une référence
                except Exception as e:
                    print(f"Error loading image for product {product.id}: {e}")

            # Insertion de l'élément : passer l'option "image" uniquement si elle n'est pas None
            if image is not None:
                item = self.tree.insert("", "end", text=product.name, image=image)
            else:
                item = self.tree.insert("", "end", text=product.name)
            # Affectation des valeurs pour chaque colonne
            self.tree.set(item, "ID", str(product.id))
            self.tree.set(item, "Quantity", str(product.quantity))
            self.tree.set(item, "Price", str(product.price))

            # Stocker les données du produit pour les récupérer lors du double‑clic
            product_data = {
                "id": product.id,
                "name": product.name,
                "quantity": product.quantity,
                "price": product.price,
                "image": product_image,  # Utilise None si l'attribut n'existe pas
            }
            self.products[item] = product_data

    def destroy(self):
        self.frame.destroy()


if __name__ == "__main__":
    # Mock ProductController and other dependencies for standalone testing
    class MockProductController:
        def get_all_products(self):
            return []  # Return empty list for testing UI

        def delete_product(self, product_id):
            print(f"Mock delete product {product_id}")

        def update_product(self, updated_product):
            print(f"Mock update product {updated_product}")

    class MockAddProductDialog:
        def __init__(self, parent, controller, load_data_callback):
            print("Mock AddProductDialog created")

    class MockUpdateProductDialog:
        def __init__(self, parent, product, on_update, on_delete):
            print(f"Mock UpdateProductDialog created for product {product}")

    ProductController = MockProductController
    AddProductDialog = MockAddProductDialog
    UpdateProductDialog = MockUpdateProductDialog

    root = tk.Tk()
    root.title("Stock Management Mock Test")
    stock_window = StockWindow(root)
    root.mainloop()
