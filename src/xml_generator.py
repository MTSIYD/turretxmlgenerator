import os
from bs4 import BeautifulSoup
from tkinter import messagebox, Tk
from file_selector import file_paths, cursor_positions

def generate_xml(file_name):
    # Define the path to the turret template XML file
    template_path = os.path.join(os.path.dirname(__file__), "turret.xml")
    
    # Check if the template file exists
    if not os.path.exists(template_path):
        messagebox.showerror("Error", "Template file 'turret.xml' not found.")
        return

    # Load and parse the template XML structure with BeautifulSoup
    with open(template_path, "r", encoding="utf-8") as template_file:
        soup = BeautifulSoup(template_file, "xml")

    # Locate the main Item element
    item_element = soup.find("Item")
    if item_element is None:
        messagebox.showerror("Error", "Main Item element not found in template.")
        return

    # Ensure required files are in file_paths
    required_files = ["Base", "Rail", "Barrel", "Muzzle Flash"]
    missing_files = [file for file in required_files if file not in file_paths]
    if missing_files:
        messagebox.showerror("Missing Files", f"Please include all files. Missing: {', '.join(missing_files)}")
        return

    # Depth counter, starting with the first file having the lowest depth
    depth_increment = 0.001
    current_depth = 0.01

    # Add elements based on the order of file addition, for increasing depth
    ordered_elements = ["Muzzle Flash","Barrel", "Rail","Base", "Turret"]

    for element_name in ordered_elements:
        print("for loop print")
        if element_name not in file_paths:
            continue  # Skip if the file is not present

        info = file_paths[element_name]

        if element_name == "Base":
            print("1")
            sprite_element = item_element.find("Sprite")
            if sprite_element:
                print("2")
                sprite_element["texture"] = info["path"]
                sprite_element["depth"] = f"{current_depth:.2f}"
                sprite_element["sourcerect"] = f"{info['sourcerect'][0]},{info['sourcerect'][1]},{info['sourcerect'][2]},{info['sourcerect'][3]}"
#                print(sprite_element)

#        for element_name in ordered_elements:
        if element_name == "Rail":
            print("3")
            rail_element = item_element.find("RailSprite")
            if rail_element:
                print("4")
#                cursor_x, cursor_y = cursor_positions["Turret-barrelpos"][0]
#                rail_x, rail_y, rail_width, rail_height = info['sourcerect']
#                origin_x = (cursor_x - rail_x) / rail_width
#                origin_y = (cursor_y - rail_y) / rail_height
                rail_element["texture"] = info["path"]
                rail_element["depth"] = f"{current_depth:.2f}"
                rail_element["sourcerect"] = f"{info['sourcerect'][0]},{info['sourcerect'][1]},{info['sourcerect'][2]},{info['sourcerect'][3]}"
#                rail_element["origin"] = f"{origin_x:.2f},{origin_y:.2f}"
#                print(rail_element)
#            else:
#                print("railnotfound")

        if element_name == "Barrel":
            print("5")
            barrel_element = item_element.find("BarrelSprite")
            if barrel_element:
                print("6")
#                cursor_x, cursor_y = cursor_positions["Turret-barrelpos"][0]
#                barrel_x, barrel_y, barrel_width, barrel_height = info['sourcerect']
#                origin_x = (cursor_x - barrel_x) / barrel_width
#                origin_y = (cursor_y - barrel_y) / barrel_height
                barrel_element["texture"] = info["path"]
                barrel_element["depth"] = f"{current_depth:.3f}"
                barrel_element["sourcerect"] = f"{info['sourcerect'][0]},{info['sourcerect'][1]},{info['sourcerect'][2]},{info['sourcerect'][3]}"
#                barrel_element["origin"] = f"{origin_x:.3f},{origin_y:.3f}"
#                print(barrel_element)

        if element_name == "Turret":
            print("2" + element_name)

            turret_element = item_element.find("Turret")
            if turret_element:
                print("1" + element_name)
        else:
            print(element_name)
            # Get cursor position for dynamic adjustments
#                cursor_x, cursor_y = cursor_positions["Turret-barrelpos"][0]
            
            # Calculate firingoffset based on cursor position
#                firing_offset_x = cursor_x  # Example adjustment for dynamic values
#                firing_offset_y = cursor_y
#                turret_element["firingoffset"] = f"{firing_offset_x},{firing_offset_y}"
            
            # Calculate barrelpos based on cursor position and dimensions from info['sourcerect']
#                turret_base_x, turret_base_y = info['sourcerect'][0], info['sourcerect'][1]
#                barrel_x = cursor_x - turret_base_x
#                barrel_y = cursor_y - turret_base_y
#                turret_element["barrelpos"] = f"{barrel_x},{barrel_y}"
        print("complete")

    # Use the Auto-Generated Cursor for a specific XML attribute (e.g., firingoffset)
    if "AutoCursor" in cursor_positions:
        auto_cursor = cursor_positions["AutoCursor"][0]  # Get the cursor's position
        turret_element = item_element.find("Turret")
        if turret_element:
            turret_element["firingoffset"] = f"{auto_cursor[0]},{auto_cursor[1]}"


    # Define the output directory and path for saving the modified XML
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "output"))
    output_path = os.path.join(output_dir, f"{file_name}.xml")
    os.makedirs(output_dir, exist_ok=True)

    # Save the modified XML structure
    with open(output_path, "w", encoding="utf-8") as output_file:
        output_file.write(soup.prettify())

    # Copy the output file path to clipboard and notify the user
    root = Tk()
    root.withdraw()
    root.clipboard_clear()
    root.clipboard_append(output_path)
    root.update()
    root.destroy()
    
    messagebox.showinfo("XML Generated", f"The sprite layout has been saved to {output_path} (copied to clipboard)")
