import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import cv2

# Global variables
original_image = None
processed_image = None

# Function to upload an image
def upload_image():
    global original_image, processed_image
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        original_image = Image.open(file_path)
        processed_image = original_image.copy()
        update_images()

# Function to update the displayed images
def update_images():
    if original_image:
        tk_original_image = ImageTk.PhotoImage(original_image)
        img_label_original.config(image=tk_original_image)
        img_label_original.image = tk_original_image
    
    if processed_image:
        tk_processed_image = ImageTk.PhotoImage(processed_image)
        img_label_processed.config(image=tk_processed_image)
        img_label_processed.image = tk_processed_image

# Function to resize the image
def resize_image():
    global processed_image
    try:
        new_width = int(width_entry.get())
        new_height = int(height_entry.get())
        processed_image = original_image.resize((new_width, new_height))
        update_images()
    except ValueError:
        messagebox.showerror("Error", "Invalid width or height value")

# Function for simple image segmentation (thresholding)
def segment_image():
    global processed_image
    try:
        threshold = int(threshold_entry.get())
        gray_image = processed_image.convert("L")
        binary_image = gray_image.point(lambda p: p > threshold and 255)
        processed_image = binary_image
        update_images()
    except ValueError:
        messagebox.showerror("Error", "Invalid threshold value")

# Function for region-based segmentation using OpenCV
def region_based_segmentation():
    global processed_image
    
    if processed_image:
        # Convert PIL image to numpy array for OpenCV
        image_np = np.array(original_image.convert("RGB"))
        gray_image = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
        
        # Thresholding
        _, thresh = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)
        
        # Edge Detection
        edges = cv2.Canny(thresh, 100, 200)
        
        # Contour Detection
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Draw contours on the image
        contour_image = image_np.copy()
        cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 2)
        
        # Convert back to PIL image
        processed_image = Image.fromarray(contour_image)
        update_images()
    else:
        messagebox.showwarning("Warning", "No image loaded")

# Function for Erosion
def apply_erosion():
    global processed_image
    if processed_image:
        image_np = np.array(processed_image.convert("L"))  # Convert to grayscale numpy array
        kernel = np.ones((5,5), np.uint8)
        eroded_image = cv2.erode(image_np, kernel, iterations=1)
        processed_image = Image.fromarray(eroded_image)
        update_images()
    else:
        messagebox.showwarning("Warning", "No image loaded")

# Function for Dilation
def apply_dilation():
    global processed_image
    if processed_image:
        image_np = np.array(processed_image.convert("L"))  # Convert to grayscale numpy array
        kernel = np.ones((5,5), np.uint8)
        dilated_image = cv2.dilate(image_np, kernel, iterations=1)
        processed_image = Image.fromarray(dilated_image)
        update_images()
    else:
        messagebox.showwarning("Warning", "No image loaded")

# Function to reset the image to the original state
def reset_image():
    global processed_image
    if original_image:
        processed_image = original_image.copy()  # Restore the processed image to the original
        update_images()  # Update the display
    else:
        messagebox.showwarning("Warning", "No image loaded")

# Function to rotate the image
def rotate_image():
    global processed_image
    try:
        angle = int(angle_entry.get())
        if processed_image:
            processed_image = processed_image.rotate(angle, expand=True)
            update_images()
        else:
            messagebox.showwarning("Warning", "No image loaded")
    except ValueError:
        messagebox.showerror("Error", "Invalid angle value")

# Function to crop the image
def crop_image():
    global processed_image
    try:
        left = int(crop_left_entry.get())
        top = int(crop_top_entry.get())
        right = int(crop_right_entry.get())
        bottom = int(crop_bottom_entry.get())
        if processed_image:
            processed_image = processed_image.crop((left, top, right, bottom))
            update_images()
        else:
            messagebox.showwarning("Warning", "No image loaded")
    except ValueError:
        messagebox.showerror("Error", "Invalid crop values")

# Function to invert the colors
def invert_colors():
    global processed_image
    if processed_image:
        processed_image = Image.eval(processed_image, lambda p: 255 - p)
        update_images()
    else:
        messagebox.showwarning("Warning", "No image loaded")

# Function to change image color modes
def change_color(mode):
    global processed_image
    if original_image:
        if mode == "color":
            processed_image = original_image.convert("RGB")
        elif mode == "grayscale":
            processed_image = original_image.convert("L")
        elif mode == "bw":
            processed_image = original_image.convert("1")
        update_images()
    else:
        messagebox.showwarning("Warning", "No image loaded")

# Initialize the main window
root = tk.Tk()
root.title("Image Processing Application")

# Set the background color of the main window
root.configure(bg='#D4D0D0')  # Darker gray background for the main window

# Create a canvas and scrollbar for button frame
canvas = tk.Canvas(root, bg='#D4D0D0')  # Match the main window background
scrollbar = tk.Scrollbar(root, orient='vertical', command=canvas.yview)
scrollbar.pack(side='right', fill='y')
canvas.pack(side='left', fill='both', expand=True)

# Create a frame to hold the buttons and images
main_frame = tk.Frame(canvas, bg='#D4D0D0')  # Match the canvas background
canvas.create_window((0, 0), window=main_frame, anchor='nw')

# Configure the scrollbar
scrollbar.config(command=canvas.yview)

# Update the canvas scroll region
def on_main_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox('all'))

main_frame.bind('<Configure>', on_main_frame_configure)

# Create UI components for buttons
button_frame = tk.Frame(main_frame, bg='#D4D0D0')  # Match the canvas background
button_frame.pack(side='left', fill='y', padx=10, pady=10)

font_style = ('Arial', 12)  # Font style: Arial, 12 pt, regular

# Adjusted button sizes: width increased, height decreased
upload_button = tk.Button(button_frame, text="Upload Image", command=upload_image, bg='#a7beae', fg='black', width=30, height=1, borderwidth=2, relief='raised', font=font_style)
upload_button.pack(fill='x', pady=5)

save_button = tk.Button(button_frame, text="Save Image", command=lambda: processed_image.save("processed_image.png") if processed_image else messagebox.showwarning("Warning", "No image to save!"), bg='#b85042', fg='white', width=30, height=1, borderwidth=2, relief='raised', font=font_style)
save_button.pack(fill='x', pady=5)

reset_button = tk.Button(button_frame, text="Reset Image", command=reset_image, bg='#e7e8d1', fg='black', width=30, height=1, borderwidth=2, relief='raised', font=font_style)
reset_button.pack(fill='x', pady=5)

properties_button = tk.Button(button_frame, text="Image Properties", command=lambda: messagebox.showinfo("Image Properties", f"Width: {original_image.width}\nHeight: {original_image.height}\nFormat: {original_image.format}") if original_image else messagebox.showerror("Error", "No image uploaded!"), bg='#e7e8d1', fg='black', width=30, height=1, borderwidth=2, relief='raised', font=font_style)
properties_button.pack(fill='x', pady=5)

tk.Button(button_frame, text="Color", command=lambda: change_color("color"), bg='#a7beae', fg='black', width=30, height=1, borderwidth=2, relief='raised', font=font_style).pack(fill='x', pady=5)
tk.Button(button_frame, text="Grayscale", command=lambda: change_color("grayscale"), bg='#a7beae', fg='black', width=30, height=1, borderwidth=2, relief='raised', font=font_style).pack(fill='x', pady=5)
tk.Button(button_frame, text="B&W", command=lambda: change_color("bw"), bg='#a7beae', fg='black', width=30, height=1, borderwidth=2, relief='raised', font=font_style).pack(fill='x', pady=5)
tk.Button(button_frame, text="Invert Colors", command=invert_colors, bg='#a7beae', fg='black', width=30, height=1, borderwidth=2, relief='raised', font=font_style).pack(fill='x', pady=5)

# Angle and Rotate button
tk.Label(button_frame, text="Angle:", font=font_style, bg='#D4D0D0').pack(pady=5)
angle_entry = tk.Entry(button_frame, font=font_style)
angle_entry.pack(pady=5)

rotate_button = tk.Button(button_frame, text="Rotate Image", command=rotate_image, bg='#b85042', fg='white', width=30, height=1, borderwidth=2, relief='raised', font=font_style)
rotate_button.pack(fill='x', pady=5)

# Cropping controls continued
tk.Label(button_frame, text="Left:", font=font_style, bg='#D4D0D0').pack(pady=5)
crop_left_entry = tk.Entry(button_frame, font=font_style)
crop_left_entry.pack(pady=5)

tk.Label(button_frame, text="Top:", font=font_style, bg='#D4D0D0').pack(pady=5)
crop_top_entry = tk.Entry(button_frame, font=font_style)
crop_top_entry.pack(pady=5)

tk.Label(button_frame, text="Right:", font=font_style, bg='#D4D0D0').pack(pady=5)
crop_right_entry = tk.Entry(button_frame, font=font_style)
crop_right_entry.pack(pady=5)

tk.Label(button_frame, text="Bottom:", font=font_style, bg='#D4D0D0').pack(pady=5)
crop_bottom_entry = tk.Entry(button_frame, font=font_style)
crop_bottom_entry.pack(pady=5)

crop_button = tk.Button(button_frame, text="Crop Image", command=crop_image, bg='#b85042', fg='white', width=30, height=1, borderwidth=2, relief='raised', font=font_style)
crop_button.pack(fill='x', pady=5)

# Segmentation controls
tk.Label(button_frame, text="Threshold:", font=font_style, bg='#D4D0D0').pack(pady=5)
threshold_entry = tk.Entry(button_frame, font=font_style)
threshold_entry.pack(pady=5)

segment_button = tk.Button(button_frame, text="Segment Image", command=segment_image, bg='#a7beae', fg='black', width=30, height=1, borderwidth=2, relief='raised', font=font_style)
segment_button.pack(fill='x', pady=5)

region_button = tk.Button(button_frame, text="Region-based Segmentation", command=region_based_segmentation, bg='#a7beae', fg='black', width=30, height=1, borderwidth=2, relief='raised', font=font_style)
region_button.pack(fill='x', pady=5)

# Erosion and Dilation controls
erosion_button = tk.Button(button_frame, text="Apply Erosion", command=apply_erosion, bg='#a7beae', fg='black', width=30, height=1, borderwidth=2, relief='raised', font=font_style)
erosion_button.pack(fill='x', pady=5)

dilation_button = tk.Button(button_frame, text="Apply Dilation", command=apply_dilation, bg='#a7beae', fg='black', width=30, height=1, borderwidth=2, relief='raised', font=font_style)
dilation_button.pack(fill='x', pady=5)

# Create UI components for image display
image_frame = tk.Frame(main_frame, bg='#F0F0F0')  # Lighter background for image display
image_frame.pack(side='right', fill='both', expand=True)

# Frame for image labels
image_display_frame = tk.Frame(image_frame, bg='#F0F0F0')
image_display_frame.pack(side='top', fill='both', expand=True)

img_label_original = tk.Label(image_display_frame)
img_label_original.pack(side='left', padx=10, pady=10)

img_label_processed = tk.Label(image_display_frame)
img_label_processed.pack(side='right', padx=10, pady=10)

# Start the main event loop
root.mainloop()
