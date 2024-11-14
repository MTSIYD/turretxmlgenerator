import tkinter as tk
from tkinter import Canvas

from button_frame import create_button_frame
from app_functions import on_entry_click, on_focusout, on_button_click

def create_scrollable_page(root, custom_font):
    """
    Creates a scrollable page with an entry, display area, and buttons.
    """
    # Create a canvas to contain the scrollable content
    scroll_canvas = tk.Canvas(root, width=780, height=780)
    scroll_canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    # Add a scrollbar to the canvas
    scrollbar = tk.Scrollbar(root, orient="vertical", command=scroll_canvas.yview)
    scrollbar.pack(side="right", fill="y")

    # Configure the canvas to work with the scrollbar
    scroll_canvas.configure(yscrollcommand=scrollbar.set)
    
    # Create a frame inside the canvas to hold all content
    main_frame = tk.Frame(scroll_canvas)
    scroll_canvas.create_window((0, 0), window=main_frame, anchor="nw")

    # Update scroll region to include the full content area
    main_frame.bind("<Configure>", lambda e: scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all")))

    # Entry field with placeholder
    entry_label = tk.Label(main_frame, text="Define file name", font=custom_font)
    entry_label.pack(pady=(20, 5), anchor="w")

    entry = tk.Entry(main_frame, font=custom_font, fg="grey")
    placeholder_text = "define file name"
    entry.insert(0, placeholder_text)
    entry.pack(pady=5, anchor="w")

    # Configure placeholder text behavior
    entry.bind("<FocusIn>", lambda e: on_entry_click(entry, placeholder_text))
    entry.bind("<FocusOut>", lambda e: on_focusout(entry, placeholder_text))

    # Generate XML button
    generate_xml_button = tk.Button(
        main_frame, text="Generate XML",
        command=lambda: on_button_click(entry, placeholder_text),
        font=custom_font
    )
    generate_xml_button.pack(pady=10, anchor="w")

    # Display area for images with updated dimensions (600x1200)
    display_area = Canvas(main_frame, width=600, height=1200, bg="white")
    display_area.pack(pady=20, anchor="center")  # Center-aligned

    # Call the grid creation function to add a grid to the display area
    create_grid(display_area, 600, 1200, spacing=20)

    # Separate frame for the scrollable buttons
    button_frame_container = tk.Frame(main_frame)
    button_frame_container.pack(fill="x", pady=10)

    # Scrollable button area inside main_frame
    create_button_frame(button_frame_container, custom_font, display_area)

    # Bind scrolling to the entire window content using the canvas scroll bar
    root.bind_all("<MouseWheel>", lambda event: scroll_canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

    return entry, display_area

def create_grid(canvas, width, height, spacing=20):
    """Draw a grid on the canvas."""
    # Draw vertical lines
    for x in range(0, width, spacing):
        canvas.create_line(x, 0, x, height, fill="#e0e0e0")

    # Draw horizontal lines
    for y in range(0, height, spacing):
        canvas.create_line(0, y, width, y, fill="#e0e0e0")
