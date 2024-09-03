import tkinter as tk
from tkinter import ttk, filedialog, messagebox, Toplevel
from PIL import Image, ImageTk, ImageOps

# Global variables
img = None

# Function to upload an image
def upload_image():
    global img, img_display
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        img = Image.open(file_path)
        img_display = ImageTk.PhotoImage(img)
        original_label.config(image=img_display)
        original_label.image = img_display
        modified_label.config(image=img_display)
        modified_label.image = img_display

# Function to convert the image to grayscale
def grayscale_image():
    global img
    if img:
        gray_img = ImageOps.grayscale(img)
        update_modified_image(gray_img)
    else:
        messagebox.showwarning("Warning", "No image loaded")

# Function to convert the image to CMYK
def cmyk_image():
    global img
    if img:
        cmyk_img = img.convert("CMYK")
        update_modified_image(cmyk_img)
    else:
        messagebox.showwarning("Warning", "No image loaded")

# Function to convert the image to RGB
def rgb_image():
    global img
    if img:
        rgb_img = img.convert("RGB")
        update_modified_image(rgb_img)
    else:
        messagebox.showwarning("Warning", "No image loaded")

# Function to rotate the image
def rotate_image():
    global img
    if img:
        try:
            angle = int(rotation_entry.get())
            rotated_img = img.rotate(angle, expand=True)
            update_modified_image(rotated_img)
        except ValueError:
            messagebox.showerror("Error", "Invalid rotation angle")
    else:
        messagebox.showwarning("Warning", "No image loaded")

# Function to crop the image
def crop_image():
    global img
    if img:
        cropped_img = img.crop((100, 100, img.width - 100, img.height - 100))
        update_modified_image(cropped_img)
    else:
        messagebox.showwarning("Warning", "No image loaded")

# Function to flip the image
def flip_image():
    global img
    if img:
        flipped_img = img
        if flip_var.get() == "Vertical":
            flipped_img = ImageOps.flip(img)
        elif flip_var.get() == "Horizontal":
            flipped_img = ImageOps.mirror(img)
        update_modified_image(flipped_img)
    else:
        messagebox.showwarning("Warning", "No image loaded")

# Function to invert the image colors
def invert_image():
    global img
    if img:
        inverted_img = ImageOps.invert(img.convert("RGB"))
        update_modified_image(inverted_img)
    else:
        messagebox.showwarning("Warning", "No image loaded")

# Function to update the modified image display
def update_modified_image(new_image):
    modified_img = ImageTk.PhotoImage(new_image)
    modified_label.config(image=modified_img)
    modified_label.image = modified_img

# Function to open the advanced options window
def open_advanced_options():
    advanced_window = Toplevel(root)
    advanced_window.title("Advanced Image Manipulation")
    advanced_window.geometry("600x400")
    
    # Advanced options content
    advanced_label = tk.Label(advanced_window, text="Advanced Image Manipulations", font=('Helvetica', 16, 'bold'))
    advanced_label.pack(pady=20)

    # Placeholders for advanced options
    placeholder = tk.Label(advanced_window, text="Advanced options coming soon...", font=('Helvetica', 12))
    placeholder.pack(pady=20)

# Create the main window
root = tk.Tk()
root.title("Image Processing Tool")
root.geometry("1200x600")
root.configure(bg='#F0F0F0')

# Create frames for layout
frame_left = tk.Frame(root, bg='#4A90E2', width=300, height=600)  # Blue frame for controls
frame_left.pack(side='left', fill='y')

frame_right = tk.Frame(root, bg='white', width=900, height=600)  # White frame for images
frame_right.pack(side='right', fill='both', expand=True)

# Create subframes in frame_right for original and modified images
frame_original = tk.Frame(frame_right, bg='white', width=450, height=600)
frame_original.pack(side='left', fill='both', expand=True)

frame_modified = tk.Frame(frame_right, bg='white', width=450, height=600)
frame_modified.pack(side='right', fill='both', expand=True)

# Original Image display
original_label = tk.Label(frame_original, text="Original Image", bg='white', font=('Helvetica', 16, 'bold'))
original_label.pack(pady=10, fill='both', expand=True)

# Modified Image display
modified_label = tk.Label(frame_modified, text="Modified Image", bg='white', font=('Helvetica', 16, 'bold'))
modified_label.pack(pady=10, fill='both', expand=True)

# Upload Button
upload_btn = ttk.Button(frame_left, text="Upload Image", command=upload_image)
upload_btn.pack(pady=20, padx=20, fill='x')

# Grayscale Button
grayscale_btn = ttk.Button(frame_left, text="Convert to Grayscale", command=grayscale_image)
grayscale_btn.pack(pady=10, padx=20, fill='x')

# CMYK Button
cmyk_btn = ttk.Button(frame_left, text="Convert to CMYK", command=cmyk_image)
cmyk_btn.pack(pady=10, padx=20, fill='x')

# RGB Button
rgb_btn = ttk.Button(frame_left, text="Convert to RGB", command=rgb_image)
rgb_btn.pack(pady=10, padx=20, fill='x')

# Rotation
rotation_label = ttk.Label(frame_left, text="Rotate Image (degrees):", background='#4A90E2', foreground='white')
rotation_label.pack(pady=10, padx=20)
rotation_entry = ttk.Entry(frame_left)
rotation_entry.pack(pady=10, padx=20, fill='x')
rotation_btn = ttk.Button(frame_left, text="Rotate", command=rotate_image)
rotation_btn.pack(pady=10, padx=20, fill='x')

# Crop Button
crop_btn = ttk.Button(frame_left, text="Crop Image", command=crop_image)
crop_btn.pack(pady=10, padx=20, fill='x')

# Flip Options
flip_var = tk.StringVar(value="Vertical")
flip_frame = ttk.LabelFrame(frame_left, text="Flip Options", padding=(10, 5))
flip_frame.pack(pady=10, padx=20, fill='x')

flip_vertical_rb = ttk.Radiobutton(flip_frame, text="Vertical", variable=flip_var, value="Vertical")
flip_vertical_rb.pack(anchor='w')

flip_horizontal_rb = ttk.Radiobutton(flip_frame, text="Horizontal", variable=flip_var, value="Horizontal")
flip_horizontal_rb.pack(anchor='w')

flip_btn = ttk.Button(frame_left, text="Flip Image", command=flip_image)
flip_btn.pack(pady=10, padx=20, fill='x')

# Invert Button
invert_btn = ttk.Button(frame_left, text="Invert Colors", command=invert_image)
invert_btn.pack(pady=10, padx=20, fill='x')

# Advanced Options Button
advanced_btn = ttk.Button(frame_left, text="Advanced Options", command=open_advanced_options)
advanced_btn.pack(pady=20, padx=20, fill='x')

# Start the main loop
root.mainloop()
