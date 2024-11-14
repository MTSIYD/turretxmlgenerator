import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

# Dictionary to store file paths, images, and cursor details
cursor_positions = {}
file_paths = {}
image_references = {}

CURSOR_COLORS = {
    "Base": "#00FFFF",      # Neon blue
    "Rail": "#39FF14",      # Neon green
    "Barrel": "#FF1493",    # Neon pink
    "Muzzle Flash": "#FFFF00", # Neon yellow
    "AutoCursor": "#FF4500" # Neon orange
}

def select_file(button_label, path_label, display_area, cursor_name=None):
    file_path = filedialog.askopenfilename(
        title="Select an Image File",
        filetypes=(("Image Files", "*.png;*.jpg"), ("All Files", "*.*"))
    )
    
    if file_path:
        path_label.config(text=file_path)
        load_and_display_image(file_path, button_label, display_area, cursor_name)
    else:
        messagebox.showwarning("No File Selected", f"No file selected for {button_label}")


def display_cursor(display_area, cursor_name, x, y, color=None):
    """Create a visual cursor with a label at the specified coordinates."""
    # Set default color if none provided
    color = color or CURSOR_COLORS.get(cursor_name, "black")
    
    # Draw a plus-shaped cursor at (x, y) position
    line1 = display_area.create_line(x - 5, y, x + 5, y, fill=color, width=2)
    line2 = display_area.create_line(x, y - 5, x, y + 5, fill=color, width=2)

    # Label the cursor next to its position for identification
    label_id = display_area.create_text(x + 10, y, text=cursor_name, anchor="w", fill=color, font=("Arial", 8))

    # Return cursor lines and label ID as a tuple for easy handling
    return (line1, line2, label_id)

def load_and_display_image(file_path, label, display_area, cursor_name=None):
    """Load and display an image in the GUI and create a labeled, colored cursor on the canvas."""
    original_img = Image.open(file_path)
    tk_img = ImageTk.PhotoImage(original_img)

    # Set initial position based on the number of images already added
    img_x, img_y = 100, len(file_paths) * 120 + 100

    # Draw the image on the canvas
    img_id = display_area.create_image(img_x, img_y, image=tk_img, anchor="center")
    image_references[label] = tk_img  # Keep a reference to prevent garbage collection

    # Determine cursor color and label based on cursor_name
    color = CURSOR_COLORS.get(cursor_name, "black")
    cursor = draw_cursor(display_area, img_x, img_y, color, label_text=cursor_name or "Cursor")

    # Store file information
    file_paths[label] = {
        "path": file_path,
        "img_id": img_id,
        "original_img": original_img,
        "cursor": cursor,
        "sourcerect": (img_x - original_img.width // 2, img_y - original_img.height // 2, original_img.width, original_img.height),
        "origin": (img_x, img_y)
    }

    add_drag_and_drop_image(display_area, img_id, label)
    add_drag_and_drop_cursor(display_area, cursor, label)

    bring_all_cursors_to_front(display_area)


def draw_cursor(canvas, x, y, color, label_text):
    """Draw a colored, plus-shaped cursor at the specified coordinates with a label."""
    # Draw the cursor as a plus sign
    line1 = canvas.create_line(x - 5, y, x + 5, y, fill=color, width=2)
    line2 = canvas.create_line(x, y - 5, x, y + 5, fill=color, width=2)

    # Add a label next to the cursor to identify it
    label_id = canvas.create_text(x + 10, y, text=label_text, anchor="w", fill=color, font=("Arial", 8))

    # Return cursor lines and label ID for easy access
    return (line1, line2, label_id)



def bring_all_cursors_to_front(canvas):
    """Bring all cursors to the front of the canvas."""
    for label, info in file_paths.items():
        cursor = info["cursor"]
        canvas.tag_raise(cursor[0])  # Horizontal line
        canvas.tag_raise(cursor[1])  # Vertical line

def add_drag_and_drop_image(canvas, img_id, label):
    """Enable drag-and-drop functionality for the image and update its sourcerect in file_paths."""
    def on_start_drag(event):
        canvas.startX = event.x
        canvas.startY = event.y

    def on_drag(event):
        dx = event.x - canvas.startX
        dy = event.y - canvas.startY
        canvas.startX = event.x
        canvas.startY = event.y
        canvas.move(img_id, dx, dy)

    def on_drop(event):
        x, y = canvas.coords(img_id)
        width, height = file_paths[label]["original_img"].width, file_paths[label]["original_img"].height
        file_paths[label]["sourcerect"] = (int(x - width / 2), int(y - height / 2), width, height)

    canvas.tag_bind(img_id, "<Button-1>", on_start_drag)
    canvas.tag_bind(img_id, "<B1-Motion>", on_drag)
    canvas.tag_bind(img_id, "<ButtonRelease-1>", on_drop)

def add_drag_and_drop_cursor(canvas, cursor, label):
    """Enable drag-and-drop functionality for the cursor and update its position in file_paths."""
    def on_start_drag(event):
        canvas.startX = event.x
        canvas.startY = event.y

    def on_drag(event):
        dx = event.x - canvas.startX
        dy = event.y - canvas.startY
        canvas.startX = event.x
        canvas.startY = event.y
        line1, line2, label_id = cursor  # Unpack all three parts of the cursor

        # Move both lines and the label
        canvas.move(line1, dx, dy)
        canvas.move(line2, dx, dy)
        canvas.move(label_id, dx, dy)

    def on_drop(event):
        # Calculate the new center position of the cursor
        line1, line2, label_id = cursor
        x1, y1, x2, y2 = canvas.coords(line1)
        cursor_x = (x1 + x2) // 2
        cursor_y = (y1 + y2) // 2
        file_paths[label]["origin"] = (int(cursor_x), int(cursor_y))

    # Bind mouse events to enable dragging
    canvas.tag_bind(cursor[0], "<Button-1>", on_start_drag)
    canvas.tag_bind(cursor[0], "<B1-Motion>", on_drag)
    canvas.tag_bind(cursor[0], "<ButtonRelease-1>", on_drop)
    canvas.tag_bind(cursor[1], "<Button-1>", on_start_drag)
    canvas.tag_bind(cursor[1], "<B1-Motion>", on_drag)
    canvas.tag_bind(cursor[1], "<ButtonRelease-1>", on_drop)
    canvas.tag_bind(cursor[2], "<Button-1>", on_start_drag)
    canvas.tag_bind(cursor[2], "<B1-Motion>", on_drag)
    canvas.tag_bind(cursor[2], "<ButtonRelease-1>", on_drop)
