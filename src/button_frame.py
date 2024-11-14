import tkinter as tk
from file_selector import select_file, CURSOR_COLORS, display_cursor

def create_button_frame(root, font, display_area):
    button_labels = {
        "Base": "SwappableItem-origin",
        "Rail": "Turret-barrelpos",
        "Barrel": None,
        "Muzzle Flash": None
    }

    for label, cursor_name in button_labels.items():
        path_label = tk.Label(root, text="No file selected", font=font)
        path_label.pack(pady=2)

        # Button configuration with color and cursor setup
        button = tk.Button(root, text=label, font=font, bg=CURSOR_COLORS.get(label, "gray"))
        button.config(command=lambda lbl=label, pl=path_label, cn=cursor_name: select_file(lbl, pl, display_area, cursor_name=cn))
        button.pack(pady=5, anchor="w")

    # Auto-generate a cursor for "AutoCursor" (not tied to a button)
    display_cursor(display_area, "AutoCursor-origin", 150, 150, CURSOR_COLORS["AutoCursor"])
