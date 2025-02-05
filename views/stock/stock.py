import tkinter as tk
from tkinter import ttk, messagebox
from database import Database

class StockWindow:
    def __init__(self):
        self.db = Database()
        self.window = tk.Tk()
        self.window.title("Stock Management")
        self.window.geometry("800x600")

        # Form Frame
        form_frame = tk.Frame(self.window)
        form_frame.pack(pady=20)

        tk.Label(form_frame, text="Product Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Quantity:").grid(row=1, column=0, padx=5, pady=5)
        self.quantity_entry = tk.Entry(form_frame)
        self.quantity_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Price:").grid(row=2, column=0, padx=5, pady=5)
        self.price_entry = tk.Entry(form_frame)
        self.price_entry.grid(row=2, column=1, padx=5, pady=5)

        # Buttons
        buttons_frame = tk.Frame(self.window)
        buttons_frame.pack(pady=10)

        tk.Button(buttons_frame, text="Add Product", command=self.add_product).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="Update Product", command=self.update_product).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="Delete Product", command=self.delete_product).pack(side=tk.LEFT, padx=5)

        # Treeview
        self.tree = ttk.Treeview(self.window, columns=("ID", "Name", "Quantity", "Price"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Price", text="Price")
        self.tree.pack(pady=20, padx=20)

        self.tree.bind("<<TreeviewSelect>>", self.item_selected)
        
        self.load_products()
        self.window.mainloop()

    def load_products(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT * FROM products")
        for product in cursor.fetchall():
            self.tree.insert("", "end", values=product)

    def add_product(self):
        name = self.name_entry.get()
        quantity = self.quantity_entry.get()
        price = self.price_entry.get()

        if name and quantity and price:
            cursor = self.db.conn.cursor()
            cursor.execute("INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)",
                         (name, quantity, price))
            self.db.conn.commit()
            self.load_products()
            self.clear_entries()
        else:
            messagebox.showerror("Error", "All fields are required")

    def update_product(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a product to update")
            return

        product_id = self.tree.item(selected_item)['values'][0]
        name = self.name_entry.get()
        quantity = self.quantity_entry.get()
        price = self.price_entry.get()

        if name and quantity and price:
            cursor = self.db.conn.cursor()
            cursor.execute("UPDATE products SET name=?, quantity=?, price=? WHERE id=?",
                         (name, quantity, price, product_id))
            self.db.conn.commit()
            self.load_products()
            self.clear_entries()
        else:
            messagebox.showerror("Error", "All fields are required")

    def delete_product(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a product to delete")
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this product?"):
            product_id = self.tree.item(selected_item)['values'][0]
            cursor = self.db.conn.cursor()
            cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
            self.db.conn.commit()
            self.load_products()
            self.clear_entries()

    def item_selected(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)['values']
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, item[1])
            self.quantity_entry.delete(0, tk.END)
            self.quantity_entry.insert(0, item[2])
            self.price_entry.delete(0, tk.END)
            self.price_entry.insert(0, item[3])

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
