import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageEnhance, ImageOps, ImageTk
import numpy as np

# Global variables
original_image = None
processed_image = None
previous_image = None

# Function to upload an image
def upload_image():
    global original_image, processed_image, previous_image
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        original_image = Image.open(file_path)
        processed_image = original_image.copy()
        previous_image = original_image.copy()  # Store the original image for undo
        update_images()

# Function to update both the original and processed images
def update_images():
    if original_image and processed_image:
        tk_original = ImageTk.PhotoImage(original_image)
        tk_processed = ImageTk.PhotoImage(processed_image)

        original_image_label.config(image=tk_original)
        original_image_label.image = tk_original

        processed_image_label.config(image=tk_processed)
        processed_image_label.image = tk_processed

# Function to adjust color balance
def adjust_color_balance(value):
    global processed_image
    if original_image:
        enhancer = ImageEnhance.Color(original_image)
        color_img = enhancer.enhance(float(value))
        processed_image = color_img
        update_images()
    else:
        messagebox.showwarning("Warning", "No image loaded")

# Function to adjust color channels
def adjust_color_channel():
    global processed_image
    if original_image:
        img_array = np.array(original_image.convert('RGB'), dtype=np.float32)
        red_factor = red_slider.get()
        green_factor = green_slider.get()
        blue_factor = blue_slider.get()
        img_array[..., 0] = np.clip(img_array[..., 0] * red_factor, 0, 255)
        img_array[..., 1] = np.clip(img_array[..., 1] * green_factor, 0, 255)
        img_array[..., 2] = np.clip(img_array[..., 2] * blue_factor, 0, 255)
        processed_image = Image.fromarray(np.uint8(img_array))
        update_images()
    else:
        if not original_image:
            messagebox.showwarning("Warning", "No image loaded")

# Function to undo the last operation
def undo():
    global processed_image, previous_image
    if previous_image:
        processed_image = previous_image.copy()
        update_images()
    else:
        messagebox.showwarning("Warning", "No action to undo")

# Create the main window
color_window = tk.Tk()
color_window.title("Color Balancing")
color_window.geometry("900x700")

# Create frames for the UI
left_frame = tk.Frame(color_window, padx=10, pady=10)
left_frame.pack(side=tk.LEFT, fill=tk.Y)

right_frame = tk.Frame(color_window, padx=10, pady=10)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Create upload button
upload_btn = ttk.Button(left_frame, text="Upload Image", command=upload_image)
upload_btn.pack(pady=10)

# Create undo button
undo_btn = ttk.Button(left_frame, text="Undo", command=undo)
undo_btn.pack(pady=10)

# Create color balance slider
color_label = tk.Label(left_frame, text="Adjust Color Balance", font=('Helvetica', 12))
color_label.pack(pady=10)
color_slider = ttk.Scale(left_frame, from_=0.1, to=2.0, orient="horizontal", command=adjust_color_balance)
color_slider.set(1.0)
color_slider.pack(pady=10)

# Create color channel sliders
red_label = tk.Label(left_frame, text="Red Channel", font=('Helvetica', 12))
red_label.pack(pady=10)
red_slider = ttk.Scale(left_frame, from_=0.0, to=2.0, orient="horizontal", command=lambda x: adjust_color_channel())
red_slider.set(1.0)
red_slider.pack(pady=10)

green_label = tk.Label(left_frame, text="Green Channel", font=('Helvetica', 12))
green_label.pack(pady=10)
green_slider = ttk.Scale(left_frame, from_=0.0, to=2.0, orient="horizontal", command=lambda x: adjust_color_channel())
green_slider.set(1.0)
green_slider.pack(pady=10)

blue_label = tk.Label(left_frame, text="Blue Channel", font=('Helvetica', 12))
blue_label.pack(pady=10)
blue_slider = ttk.Scale(left_frame, from_=0.0, to=2.0, orient="horizontal", command=lambda x: adjust_color_channel())
blue_slider.set(1.0)
blue_slider.pack(pady=10)

# Create image display labels
original_image_label = tk.Label(right_frame, text="Original Image", font=('Helvetica', 12))
original_image_label.pack(pady=10)
processed_image_label = tk.Label(right_frame, text="Processed Image", font=('Helvetica', 12))
processed_image_label.pack(pady=10)

# Start the main loop
color_window.mainloop()
