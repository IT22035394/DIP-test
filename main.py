import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageOps, ImageDraw
import os
import numpy as np

# Global variables
img = None
original_img = None  # To store the original image
img_history = []  # To store the image history for undo functionality
cropping = False
crop_rectangle = None  # To hold the cropping rectangle
start_x, start_y = 0, 0  # Starting coordinates for cropping

# Function to upload an image
def upload_image():
    global img, original_img, img_display, img_history
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        img = Image.open(file_path)
        original_img = img.copy()  # Store the original image
        img_history.clear()  # Clear the history on a new upload
        img_display = ImageTk.PhotoImage(img)
        original_label.config(image=img_display)
        original_label.image = img_display
        modified_label.config(image=img_display)
        modified_label.image = img_display
        canvas_left.configure(scrollregion=canvas_left.bbox('all'))  # Update the scrollbar

# Function to save the current image state to history
def save_to_history():
    global img_history
    if img:
        img_history.append(img.copy())

# Function to undo the last operation
def undo_last_operation():
    global img, img_history
    if img_history:
        img = img_history.pop()  # Revert to the previous image
        update_modified_image(img)
    else:
        messagebox.showinfo("Info", "No more steps to undo.")

# Function to reset the image to its original state
def reset_image():
    global img, original_img
    if original_img:
        img = original_img.copy()
        update_modified_image(img)

# Function to update the modified image display
def update_modified_image(new_image):
    modified_img = ImageTk.PhotoImage(new_image)
    modified_label.config(image=modified_img)
    modified_label.image = modified_img

# Function to convert the image to grayscale
def grayscale_image():
    global img
    if img:
        save_to_history()
        gray_img = ImageOps.grayscale(img)
        update_modified_image(gray_img)
        img = gray_img
    else:
        messagebox.showwarning("Warning", "No image loaded")

# Function to convert the image to black and white
def black_and_white_image():
    global img
    if img:
        save_to_history()
        bw_img = img.convert('1')  # Black and white conversion
        update_modified_image(bw_img)
        img = bw_img
    else:
        messagebox.showwarning("Warning", "No image loaded")

# Function to convert the image to HSV
def hsv_image():
    global img
    if img:
        save_to_history()
        hsv_img = img.convert('HSV')  # Convert to HSV
        update_modified_image(hsv_img)
        img = hsv_img
    else:
        messagebox.showwarning("Warning", "No image loaded")

# Function to rotate the image
def rotate_image():
    global img
    if img:
        try:
            save_to_history()
            angle = int(rotation_entry.get())
            rotated_img = img.rotate(angle, expand=True)
            update_modified_image(rotated_img)
            img = rotated_img
        except ValueError:
            messagebox.showerror("Error", "Invalid rotation angle")
    else:
        messagebox.showwarning("Warning", "No image loaded")

# Function to flip the image
def flip_image():
    global img
    if img:
        save_to_history()
        flipped_img = img
        if flip_var.get() == "Vertical":
            flipped_img = ImageOps.flip(img)
        elif flip_var.get() == "Horizontal":
            flipped_img = ImageOps.mirror(img)
        update_modified_image(flipped_img)
        img = flipped_img
    else:
        messagebox.showwarning("Warning", "No image loaded")

# Function to invert the image colors
def invert_image():
    global img
    if img:
        save_to_history()
        inverted_img = ImageOps.invert(img.convert("RGB"))
        update_modified_image(inverted_img)
        img = inverted_img
    else:
        messagebox.showwarning("Warning", "No image loaded")

# Function to start cropping with mouse click and drag
def start_crop(event):
    global crop_rectangle, cropping, start_x, start_y
    cropping = True
    start_x, start_y = event.x, event.y
    canvas_right.delete(crop_rectangle)  # Remove previous rectangle
    crop_rectangle = canvas_right.create_rectangle(event.x, event.y, event.x, event.y, outline='red')

# Function to update the cropping rectangle as the user drags the mouse
def update_crop(event):
    global cropping
    if cropping:
        canvas_right.coords(crop_rectangle, start_x, start_y, event.x, event.y)

# Function to finish cropping and apply the crop
def finish_crop(event):
    global img, cropping, start_x, start_y
    if cropping:
        cropping = False
        end_x, end_y = event.x, event.y
        save_to_history()

        # Crop using the canvas coordinates
        left = min(start_x, end_x)
        top = min(start_y, end_y)
        right = max(start_x, end_x)
        bottom = max(start_y, end_y)

        cropped_img = img.crop((left, top, right, bottom))
        update_modified_image(cropped_img)
        img = cropped_img

# Function to display image properties
def view_image_properties():
    if img:
        properties = f"Dimensions: {img.size[0]}x{img.size[1]}\nMode: {img.mode}"
        if hasattr(img, 'filename'):
            file_size = os.path.getsize(img.filename)
            properties += f"\nFile Size: {file_size / 1024:.2f} KB"
        messagebox.showinfo("Image Properties", properties)
    else:
        messagebox.showwarning("Warning", "No image loaded")

# Function to open the advanced options window
def open_advanced_options():
    os.system("python advanced_options.py")

# Create the main window
root = tk.Tk()
root.title("Image Processing Tool")
root.geometry("1200x750")
root.configure(bg='#F7F9FB')

# Create frames for layout
frame_right = tk.Frame(root, bg='white', width=900, height=700)  # White frame for images
frame_right.pack(side='right', fill='both', expand=True)

# Create a canvas to add scrollbars to the left frame
canvas_left = tk.Canvas(root, bg='#3498DB', width=300, height=700)
canvas_left.pack(side='left', fill='both', expand=True)

# Add vertical scrollbar
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas_left.yview)
scrollbar.pack(side='left', fill='y')

# Configure canvas and scrollbar
canvas_left.configure(yscrollcommand=scrollbar.set)
canvas_left.bind('<Configure>', lambda e: canvas_left.configure(scrollregion=canvas_left.bbox('all')))

# Create a frame inside the canvas to hold the controls
frame_left = tk.Frame(canvas_left, bg='#3498DB')
canvas_left.create_window((0, 0), window=frame_left, anchor="nw")

# Create subframes in frame_right for original and modified images
frame_original = tk.Frame(frame_right, bg='white', width=450, height=700)
frame_original.pack(side='left', fill='both', expand=True)

frame_modified = tk.Frame(frame_right, bg='white', width=450, height=700)
frame_modified.pack(side='right', fill='both', expand=True)

# Original Image display
original_label = tk.Label(frame_original, text="Original Image", bg='white', font=('Helvetica', 16, 'bold'))
original_label.pack(pady=10, fill='both', expand=True)

# Modified Image display
modified_label = tk.Label(frame_modified, text="Modified Image", bg='white', font=('Helvetica', 16, 'bold'))
modified_label.pack(pady=10, fill='both', expand=True)

# Undo button under the Modified Image
undo_btn_modified = ttk.Button(frame_modified, text="Undo", command=undo_last_operation)
undo_btn_modified.pack(pady=10, padx=20)

# Upload Button
upload_btn = ttk.Button(frame_left, text="Upload Image", command=upload_image)
upload_btn.pack(pady=20, padx=20, fill='x')

# Grayscale Button
grayscale_btn = ttk.Button(frame_left, text="Convert to Grayscale", command=grayscale_image)
grayscale_btn.pack(pady=10, padx=20, fill='x')

# Black and White Button
bw_btn = ttk.Button(frame_left, text="Convert to Black & White", command=black_and_white_image)
bw_btn.pack(pady=10, padx=20, fill='x')

# HSV Button
hsv_btn = ttk.Button(frame_left, text="Convert to HSV", command=hsv_image)
hsv_btn.pack(pady=10, padx=20, fill='x')

# Rotation
rotation_label = ttk.Label(frame_left, text="Rotate Image (degrees):", background='#3498DB', foreground='white')
rotation_label.pack(pady=10, padx=20)
rotation_entry = ttk.Entry(frame_left)
rotation_entry.pack(pady=10, padx=20, fill='x')
rotation_btn = ttk.Button(frame_left, text="Rotate", command=rotate_image)
rotation_btn.pack(pady=10, padx=20, fill='x')

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

# Reset Button
reset_btn = ttk.Button(frame_left, text="Reset Image", command=reset_image)
reset_btn.pack(pady=10, padx=20, fill='x')

# Advanced Options Button
advanced_btn = ttk.Button(frame_left, text="Advanced Options", command=open_advanced_options)
advanced_btn.pack(pady=20, padx=20, fill='x')

# Image Properties Button
properties_btn = ttk.Button(frame_left, text="View Image Properties", command=view_image_properties)
properties_btn.pack(pady=10, padx=20, fill='x')

# Crop tool instructions
crop_instruction = ttk.Label(frame_left, text="Click and drag on the image to crop-In the white region under the image.", background='#3498DB', foreground='white')
crop_instruction.pack(pady=10, padx=20)

# Bind cropping functionality
canvas_right = tk.Canvas(frame_modified, bg='white', width=450, height=700)
canvas_right.pack(fill='both', expand=True)
canvas_right.bind("<ButtonPress-1>", start_crop)
canvas_right.bind("<B1-Motion>", update_crop)
canvas_right.bind("<ButtonRelease-1>", finish_crop)

# Start the main loop
root.mainloop()
