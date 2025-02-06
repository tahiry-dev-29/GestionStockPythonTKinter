# Couleurs
PRIMARY_COLOR = "#2196F3"
SECONDARY_COLOR = "#FFC107"
BG_COLOR = "#F5F5F5"
TEXT_COLOR = "#333333"
CARD_BG = "white"
INPUT_BG = "#F8F9FA"
HOVER_COLOR = "#1976D2"
DANGER_COLOR = "#f44336"

# Styles
TITLE_FONT = ("Helvetica", 24, "bold")
SUBTITLE_FONT = ("Helvetica", 14)
HEADER_FONT = ("Helvetica", 16, "bold")
NORMAL_FONT = ("Helvetica", 12)
BUTTON_FONT = ("Helvetica", 12, "bold")

# Button styles
BUTTON_STYLE = {
    "bg": PRIMARY_COLOR,
    "fg": "white",
    "font": BUTTON_FONT,
    "relief": "flat",
    "padx": 10,
    "pady":5,
    "cursor": "hand2"
}

# Label styles
LABEL_STYLE = {
    "font": NORMAL_FONT,
    "bg": "white",
    "fg": TEXT_COLOR,
}

# Entry styles (remove bg from here since it's handled in the labels)
ENTRY_STYLE = {
    "font": NORMAL_FONT,
    "bg": INPUT_BG,
    "fg": TEXT_COLOR,
    "relief": "flat",
    "bd": 0
}

# Card styles
CARD_STYLE = {
    "bg": CARD_BG,
    "relief": "solid",
    "bd": 1
}

# Table styles
TABLE_STYLE = {
    "background": "#ffffff",
    "fieldbackground": "#ffffff",
    "foreground": TEXT_COLOR,
    "font": ("Helvetica", 10),
    "rowheight": 40
}

# Action button styles
ACTION_BUTTON_STYLE = {
    "font": ("Helvetica", 9),
    "borderwidth": 0,
    "relief": "flat",
    "cursor": "hand2",
    "padx": 10,
    "pady": 5,
}

UPDATE_BUTTON_STYLE = {
    **ACTION_BUTTON_STYLE,
    "bg": PRIMARY_COLOR,
    "fg": "white",
}

DELETE_BUTTON_STYLE = {
    **ACTION_BUTTON_STYLE,
    "bg": "#ff4444",
    "fg": "white",
}

