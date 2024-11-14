import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import tkinter as tk
from scrollable_button_frame import create_scrollable_page
from app_functions import on_button_click, draw_pixel_grid  # Import draw_pixel_grid


# Create the main application window
root = tk.Tk()
root.title("Simple GUI")
root.geometry("800x800")  # Increase window size to fit buttons

# Define the custom font style (ensure "Bebas Neue" is installed on your system)
custom_font = ("Bebas Neue", 12)

# Create a full-page scrollable layout
entry, display_area = create_scrollable_page(root, custom_font)

root.mainloop()
