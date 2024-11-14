import tkinter as tk
from xml_generator import generate_xml
from tkinter import messagebox

def on_button_click(entry, placeholder_text):
    """Handles the action when the Generate XML button is clicked."""
    user_input = entry.get()
    if user_input == placeholder_text:
        user_input = ""  # Consider placeholder as empty input
    generate_xml()

def on_entry_click(entry, placeholder_text):
    """Clears placeholder text when entry field is focused."""
    if entry.get() == placeholder_text:
        entry.delete(0, tk.END)
        entry.config(fg="black")

def on_focusout(entry, placeholder_text):
    """Restores placeholder text if entry field is empty on focus out."""
    if entry.get() == "":
        entry.insert(0, placeholder_text)
        entry.config(fg="grey")

def draw_pixel_grid(display_area, width, height, step=50):
    """
    Draws a grid on the display area to visually indicate pixel dimensions.
    
    Parameters:
        display_area (tk.Canvas): The canvas where the grid will be drawn.
        width (int): Width of the display area in pixels.
        height (int): Height of the display area in pixels.
        step (int): The spacing between grid lines in pixels.
    """
    # Clear any existing grid lines
    display_area.delete("grid")

    # Draw vertical lines and X-axis labels
    for x in range(0, width, step):
        display_area.create_line(x, 0, x, height, fill="gray", tags="grid")  # Vertical line
        display_area.create_text(x, 10, text=str(x), anchor="n", fill="black", tags="grid")  # Label

    # Draw horizontal lines and Y-axis labels
    for y in range(0, height, step):
        display_area.create_line(0, y, width, y, fill="gray", tags="grid")  # Horizontal line
        display_area.create_text(10, y, text=str(y), anchor="w", fill="black", tags="grid")  # Label

def on_button_click(entry, placeholder_text):
    """Handles the action when the Generate XML button is clicked."""
    user_input = entry.get()
    if user_input == placeholder_text or not user_input.strip():
        messagebox.showerror("Invalid File Name", "Please enter a valid file name.")
        return

    # Pass the user input as the file name to generate_xml
    generate_xml(user_input.strip())