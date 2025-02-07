from .colors import *

# Common Styles
PADDING = 20
BORDER_RADIUS = 10

# Font configurations
FONT_FAMILY = "Helvetica"
TITLE_FONT = (FONT_FAMILY, 24, "bold")
SUBTITLE_FONT = (FONT_FAMILY, 12, "bold")
TEXT_FONT = (FONT_FAMILY, 10)

# Button styles
BUTTON_STYLE = {
    "font": (FONT_FAMILY, 10, "bold"),
    "bg": PRIMARY_COLOR,
    "fg": "white",
    "activebackground": SECONDARY_COLOR,
    "activeforeground": "white",
    "relief": "flat",
    "padx": 15,
    "pady": 8,
    "cursor": "hand2"
}

DANGER_BUTTON = {
    **BUTTON_STYLE,
    "bg": DANGER_COLOR,
    "activebackground": "#ff4444"
}

# Entry styles
ENTRY_STYLE = {
    "font": TEXT_FONT,
    "relief": "solid",
    "bd": 1,
    "highlightthickness": 1,
    "highlightcolor": PRIMARY_COLOR
}

# Dialog styles
DIALOG_STYLE = {
    "bg": BG_COLOR,
    "padx": PADDING,
    "pady": PADDING
}

# Frame styles
FRAME_STYLE = {
    "bg": BG_COLOR,
    "padx": PADDING,
    "pady": PADDING
}

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
