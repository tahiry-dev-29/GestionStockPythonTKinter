import tkinter as tk
from tkinter import ttk, messagebox
from styles.colors import *
from styles.theme import Theme

class StockWindow:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(self.parent, bg=BG_COLOR)
        self.frame.pack(fill='both', expand=True)
        
        self.setup_ui()

    def setup_ui(self):
        # Header avec titre et boutons d'action
        header = tk.Frame(self.frame, bg=BG_COLOR)
        header.pack(fill='x', padx=20, pady=10)

        # Titre
        tk.Label(
            header,
            text="Stock Management",
            font=TITLE_FONT,
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack(side='left', pady=10)

        # Boutons d'action
        actions_frame = tk.Frame(header, bg=BG_COLOR)
        actions_frame.pack(side='right', pady=10)

        # Bouton Add New Product
        add_btn = tk.Button(
            actions_frame,
            text="➕ Add New Product",
            command=self.show_add_dialog,
            **BUTTON_STYLE
        )
        add_btn.pack(side='left', padx=5)
        
        # Bouton Refresh
        refresh_btn = tk.Button(
            actions_frame,
            text="🔄 Refresh",
            command=self.refresh_data,
            **{**BUTTON_STYLE, 'bg': SECONDARY_COLOR}
        )
        refresh_btn.pack(side='left', padx=5)

        # Table container
        self.table_container = tk.Frame(self.frame, bg=BG_COLOR)
        self.table_container.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.setup_table()
        self.load_data()

    def setup_table(self):
        # Créer le treeview avec colonnes
        columns = ("ID", "Name", "Quantity", "Price", "Actions")
        self.tree = ttk.Treeview(
            self.table_container, 
            columns=columns,
            show="headings",
            style="Custom.Treeview"
        )

        # Configurer les colonnes
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Product Name")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Actions", text="Actions")

        # Configurer les largeurs des colonnes
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Name", width=200, anchor="w")
        self.tree.column("Quantity", width=100, anchor="center")
        self.tree.column("Price", width=100, anchor="center")
        self.tree.column("Actions", width=150, anchor="center")

        # Ajouter les scrollbars
        y_scrollbar = ttk.Scrollbar(self.table_container, orient="vertical", command=self.tree.yview)
        x_scrollbar = ttk.Scrollbar(self.table_container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        # Placer les éléments
        self.tree.pack(side='left', fill='both', expand=True)
        y_scrollbar.pack(side='right', fill='y')
        x_scrollbar.pack(side='bottom', fill='x')

    def add_action_buttons(self, item, product):
        # Créer le frame pour les boutons
        actions_frame = tk.Frame(self.tree, bg='white')
        
        # Bouton Edit
        edit_btn = tk.Button(
            actions_frame,
            text="✏️",
            command=lambda: self.show_edit_dialog(product),
            **UPDATE_BUTTON_STYLE
        )
        edit_btn.pack(side='left', padx=2)
        
        # Bouton Delete
        delete_btn = tk.Button(
            actions_frame,
            text="🗑️",
            command=lambda: self.confirm_delete(product),
            **DELETE_BUTTON_STYLE
        )
        delete_btn.pack(side='left', padx=2)

        # Positionner les boutons
        bbox = self.tree.bbox(item, "Actions")
        if bbox:
            actions_frame.place(
                in_=self.tree,
                x=bbox[0] + (bbox[2] - bbox[0])//2,
                y=bbox[1] + (bbox[3] - bbox[1])//2,
                anchor='center'
            )

    def show_add_dialog(self):
        # À implémenter: Afficher la boîte de dialogue d'ajout
        pass

    def show_edit_dialog(self, product):
        # À implémenter: Afficher la boîte de dialogue de modification
        pass

    def confirm_delete(self, product):
        # À implémenter: Confirmer et supprimer le produit
        pass

    def refresh_data(self):
        # À implémenter: Rafraîchir les données
        pass

    def load_data(self):
        # À implémenter: Charger les données
        pass

    def destroy(self):
        self.frame.destroy()
