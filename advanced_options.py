import tkinter as tk
from tkinter import ttk
import os

# Function to open Tonal Transformations window
def open_tonal_transformations():
    os.system("python tonal_trans.py")

# Function to open Color Balancing window
def open_color_balancing():
    os.system("python color_balancing.py")

# Function to open Filters window
def open_filters():
    os.system("python filters.py")

# Function to open Image Segmentation window
def open_image_segmentation():
    os.system("python image_segmentation.py")

# Create the advanced options window
advanced_window = tk.Tk()
advanced_window.title("Advanced Image Manipulation")
advanced_window.geometry("600x500")

# Advanced options content
advanced_label = tk.Label(advanced_window, text="Advanced Image Manipulations", font=('Helvetica', 16, 'bold'))
advanced_label.pack(pady=20)

# Buttons to open tonal transformations and color balancing
tonal_btn = ttk.Button(advanced_window, text="Tonal Transformations", command=open_tonal_transformations)
tonal_btn.pack(pady=20)

color_balancing_btn = ttk.Button(advanced_window, text="Color Balancing", command=open_color_balancing)
color_balancing_btn.pack(pady=20)

filters_btn = ttk.Button(advanced_window, text="Filters", command=open_filters)
filters_btn.pack(pady=20)

image_segmentation_btn = ttk.Button(advanced_window, text="Image Segmentation", command=open_image_segmentation)
image_segmentation_btn.pack(pady=20)

# Start the main loop
advanced_window.mainloop()
