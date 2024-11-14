import tkinter as tk

def create_entry_with_placeholder(root, custom_font):
    placeholder_text = "define file name"

    # Label for the entry field
    entry_label = tk.Label(root, text="Define file name", font=custom_font)
    entry_label.pack(pady=(20, 5), anchor="w")  # Align the label to the left

    # Entry field with placeholder text
    entry = tk.Entry(root, font=custom_font, fg="grey")
    entry.insert(0, placeholder_text)  # Insert placeholder text
    entry.pack(pady=5, anchor="w")  # Align the entry field to the left

    # Focus events for clearing and restoring placeholder text
    entry.bind("<FocusIn>", lambda event: on_entry_click(entry, placeholder_text))
    entry.bind("<FocusOut>", lambda event: on_focusout(entry, placeholder_text))

    return entry, placeholder_text

def on_entry_click(entry, placeholder_text):
    if entry.get() == placeholder_text:
        entry.delete(0, tk.END)
        entry.config(fg="black")

def on_focusout(entry, placeholder_text):
    if entry.get() == "":
        entry.insert(0, placeholder_text)
        entry.config(fg="grey")
