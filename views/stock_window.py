# Interface pour la gestion des stocks (entrées/sorties)

import tkinter as tk
from tkinter import messagebox

class StockWindow:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("Stock Management")
        
        self.product_label = tk.Label(root, text="Product Name:")
        self.product_label.grid(row=0, column=0)
        
        self.product_entry = tk.Entry(root)
        self.product_entry.grid(row=0, column=1)

        self.quantity_label = tk.Label(root, text="Quantity:")
        self.quantity_label.grid(row=1, column=0)
        
        self.quantity_entry = tk.Entry(root)
        self.quantity_entry.grid(row=1, column=1)

        self.add_button = tk.Button(root, text="Add Product", command=self.add_product)
        self.add_button.grid(row=2, column=0, columnspan=2)

    def add_product(self):
        product_name = self.product_entry.get()
        quantity = self.quantity_entry.get()
        
        if not product_name or not quantity.isdigit():
            messagebox.showerror("Input Error", "Please fill all fields correctly.")
            return
        
        self.controller.add_product(product_name, int(quantity))
        messagebox.showinfo("Success", f"Product {product_name} added successfully!")
        self.product_entry.delete(0, tk.END)