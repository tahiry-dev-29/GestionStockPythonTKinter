# Classe pour représenter un produit

class Product:
    def __init__(self, id, name, quantity, price):
        self.id = id
        self.name = name
        self.quantity = quantity
        self.price = price

    def __str__(self):
        return f"Product {self.name} (ID: {self.id})"
