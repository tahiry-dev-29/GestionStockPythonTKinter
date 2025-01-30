 # Point d'entrée de l'application

import tkinter as tk
from views.stock_window import StockWindow
from controllers.stock_controller import StockController

if __name__ == "__main__":
    root = tk.Tk()
    controller = StockController(None)  # Pass the view in controller after initialization
    view = StockWindow(root, controller)
    controller.view = view  # Link view and controller
    root.mainloop()
