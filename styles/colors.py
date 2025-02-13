# Main colors
PRIMARY_COLOR = "#2196F3"  # Blue
SECONDARY_COLOR = "#1976D2"  # Darker Blue
ACCENT_COLOR = "#FFC107"  # Amber

# Background colors
BG_COLOR = "#F5F5F5"  # Light Gray
SURFACE_COLOR = "#FFFFFF"  # White
INPUT_BG = "#FFFFFF"  # White background for inputs
CARD_BG = "#FFFFFF"  # White background for cards

# Text colors
TEXT_COLOR = "#212121"  # Almost Black
TEXT_PRIMARY = "#212121"  # Almost Black
TEXT_SECONDARY = "#757575"  # Gray
TEXT_DISABLED = "#BDBDBD"  # Light Gray

# Status colors
SUCCESS_COLOR = "#4CAF50"  # Green
WARNING_COLOR = "#FF9800"  # Orange
DANGER_COLOR = "#F44336"  # Red
INFO_COLOR = "#03A9F4"  # Light Blue

# Interactive colors
HOVER_COLOR = "#1565C0"  # Darker blue for hover
ACTIVE_COLOR = "#0D47A1"  # Even darker blue for click/active state

# Font configurations
TITLE_FONT = ("Helvetica", 24, "bold")
SUBTITLE_FONT = ("Helvetica", 14)
HEADER_FONT = ("Helvetica", 16, "bold")
NORMAL_FONT = ("Helvetica", 12)
BUTTON_FONT = ("Helvetica", 12, "bold")

# Basic styles
BUTTON_STYLE = {
    "bg": PRIMARY_COLOR,
    "fg": "white",
    "font": BUTTON_FONT,
    "relief": "flat",
    "padx": 10,
    "pady": 5,
    "cursor": "hand2",
    "activebackground": ACTIVE_COLOR,
    "activeforeground": "white",
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
    "bd": 0,
}

# Card styles
CARD_STYLE = {"bg": CARD_BG, "relief": "solid", "bd": 1}

# Table styles
TABLE_STYLE = {
    "background": SURFACE_COLOR,
    "fieldbackground": SURFACE_COLOR,
    "foreground": TEXT_COLOR,
    "font": ("Helvetica", 10),
    "rowheight": 40,
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
