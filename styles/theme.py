from .colors import *

class Theme:
    @staticmethod
    def setup_treeview_style():
        return {
            "style_name": "Custom.Treeview",
            "settings": {
                "background": "#ffffff",
                "fieldbackground": "#ffffff",
                "foreground": TEXT_COLOR,
                "rowheight": 40,
                "font": ("Helvetica", 10)
            },
            "heading_style": {
                "background": PRIMARY_COLOR,
                "foreground": "white",
                "font": ("Helvetica", 10, "bold"),
                "padding": 10
            }
        }

    @staticmethod
    def get_dialog_style():
        return {
            "bg": "white",
            "title_style": {
                "font": TITLE_FONT,
                "bg": "white",
                "fg": TEXT_COLOR
            }
        }

    @staticmethod
    def get_table_columns():
        return {
            "ID": {"width": 50, "anchor": "center"},
            "Username": {"width": 150, "anchor": "center"},
            "Email": {"width": 200, "anchor": "center"},
            "Role": {"width": 100, "anchor": "center"},
        }
