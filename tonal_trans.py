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

# Function to adjust brightness
def adjust_brightness(value):
    global processed_image
    if original_image:
        enhancer = ImageEnhance.Brightness(original_image)
        bright_img = enhancer.enhance(float(value))
        processed_image = bright_img
        update_images()
    else:
        messagebox.showwarning("Warning", "No image loaded")

# Function to apply image negative
def apply_negative():
    global processed_image
    if original_image:
        processed_image = ImageOps.invert(original_image.convert("RGB"))
        update_images()
    else:
        messagebox.showwarning("Warning", "No image loaded")

# Function to apply log transformation
def apply_log_transformation():
    global processed_image
    if original_image:
        img_array = np.array(original_image.convert('L'))
        img_array = np.log1p(img_array)
        img_array = np.uint8(255 * img_array / np.max(img_array))
        processed_image = Image.fromarray(img_array)
        update_images()
    else:
        messagebox.showwarning("Warning", "No image loaded")

# Function to apply power law transformation
def apply_power_law_transformation():
    global processed_image
    gamma = gamma_entry.get()
    if gamma:
        try:
            gamma = float(gamma)
            img_array = np.array(original_image.convert('L'))
            img_array = np.power(img_array / 255.0, gamma) * 255
            processed_image = Image.fromarray(np.uint8(img_array))
            update_images()
        except ValueError:
            messagebox.showerror("Error", "Invalid gamma value")
    else:
        messagebox.showwarning("Warning", "Enter a gamma value")

# Function to apply piecewise linear transformation
def apply_piecewise_linear_transformation():
    global processed_image
    if original_image:
        img_array = np.array(original_image.convert('L'))
        img_array = np.clip(img_array, 50, 200)  # Example transformation
        processed_image = Image.fromarray(np.uint8(img_array))
        update_images()
    else:
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
root = tk.Tk()
root.title("Image Processing Application")
root.geometry("1200x600")

# Create frames for the UI
left_frame = tk.Frame(root, padx=10, pady=10)
left_frame.pack(side=tk.LEFT, fill=tk.Y)

right_frame = tk.Frame(root, padx=10, pady=10)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Create upload button
upload_btn = ttk.Button(left_frame, text="Upload Image", command=upload_image)
upload_btn.pack(pady=10)

# Create undo button
undo_btn = ttk.Button(left_frame, text="Undo", command=undo)
undo_btn.pack(pady=10)

# Create brightness adjustment controls
brightness_label = tk.Label(left_frame, text="Adjust Brightness", font=('Helvetica', 12))
brightness_label.pack(pady=10)
brightness_slider = ttk.Scale(left_frame, from_=0.1, to=2.0, orient="horizontal", command=adjust_brightness)
brightness_slider.set(1.0)
brightness_slider.pack(pady=10)

# Create image display labels
original_image_label = tk.Label(right_frame, text="Original Image", font=('Helvetica', 12))
original_image_label.pack(pady=10)
processed_image_label = tk.Label(right_frame, text="Processed Image", font=('Helvetica', 12))
processed_image_label.pack(pady=10)

# Create transformation buttons
negative_button = ttk.Button(left_frame, text="Apply Negative", command=apply_negative)
negative_button.pack(pady=10)

log_button = ttk.Button(left_frame, text="Apply Log Transformation", command=apply_log_transformation)
log_button.pack(pady=10)

gamma_entry_label = tk.Label(left_frame, text="Gamma (Power Law):", font=('Helvetica', 12))
gamma_entry_label.pack(pady=5)
gamma_entry = tk.Entry(left_frame)
gamma_entry.pack(pady=5)
power_law_button = ttk.Button(left_frame, text="Apply Power Law Transformation", command=apply_power_law_transformation)
power_law_button.pack(pady=10)

piecewise_button = ttk.Button(left_frame, text="Apply Piecewise Linear Transformation", command=apply_piecewise_linear_transformation)
piecewise_button.pack(pady=10)

# Start the main loop
root.mainloop()
