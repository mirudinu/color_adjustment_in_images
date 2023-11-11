import numpy as np
import os
# opencv for operations on images
import cv2

# tkinter for GUI
import tkinter as tk
from tkinter import filedialog as fd
from PIL import ImageTk, Image  

# from skimage.segmentation import felzenszwalb, chan_vese
# from skimage.feature import canny as skimage_canny

current_file = "No file selected"
crt_dir = os.getcwd()

def simulate_protanopia():
    original_image = cv2.imread(current_file)
    cv2.imwrite(crt_dir + '/simulated_colorblindness_images/protanopia.jpeg', original_image)

def simulate_deuteranopia():
    original_image = cv2.imread(current_file)
    cv2.imwrite(crt_dir + '/simulated_colorblindness_images/deuteranopia.jpeg', original_image)

def simulate_tritanopia():
    original_image = cv2.imread(current_file)
    cv2.imwrite(crt_dir + '/simulated_colorblindness_images/tritanopia.jpeg', original_image)

def open_file():
    global current_file
    filetypes = ( ('jpeg files', '*.jpeg'), ('jpg files', '*.jpg'), ('png files', '*.png'), ('All files', '*.*') )

    # get new image path
    current_file = fd.askopenfilename(initialdir = os.getcwd(),title = "Select file",filetypes = filetypes)

    # update displayed image path
    original_text = tk.Text(window, height=1, width = 40)
    original_text.grid(column=0, row=1, sticky='nsew', padx=0, pady=0)
    original_text.insert("0.0", "Original")
    original_text['state'] = 'disabled'

    #update original image
    image1 = Image.open(current_file)
    image1 = image1.resize((350, 350))
    original = ImageTk.PhotoImage(image1)
    label1 = tk.Label(image=original)
    label1.image = original
    label1.grid(column=0, row=2, sticky='nw', padx=0, pady=0)

    # Insert Simulated Protanopia Image
    simulate_protanopia()
    protanopia_text = tk.Text(window, height=1, width = 40)
    protanopia_text.grid(column=0, row=3, sticky='nw', padx=0, pady=0)
    protanopia_text.insert("0.0", "Protanopia")
    protanopia_text['state'] = 'disabled'

    image2 = Image.open(os.getcwd() + '/simulated_colorblindness_images/protanopia.jpeg')
    image2 = image2.resize((350, 350))
    simulated = ImageTk.PhotoImage(image2)
    label2 = tk.Label(image=simulated)
    label2.image = simulated
    label2.grid(column=0, row=4, sticky='nw', padx=0, pady=0)

    # Insert Simulated Deuteranopia Image
    simulate_deuteranopia()
    deuteranopia_text = tk.Text(window, height=1, width = 40)
    deuteranopia_text.grid(column=1, row=3, sticky='nw', padx=0, pady=0)
    deuteranopia_text.insert("0.0", "Deuteranopia")
    deuteranopia_text['state'] = 'disabled'

    image2 = Image.open(os.getcwd() + '/simulated_colorblindness_images/deuteranopia.jpeg')
    image2 = image2.resize((350, 350))
    simulated = ImageTk.PhotoImage(image2)
    label2 = tk.Label(image=simulated)
    label2.image = simulated
    label2.grid(column=1, row=4, sticky='nw', padx=0, pady=0)

    # Insert Simulated Tritanopia Image
    simulate_tritanopia()
    tritanopia_text = tk.Text(window, height=1, width = 40)
    tritanopia_text.grid(column=2, row=3, sticky='nw', padx=0, pady=0)
    tritanopia_text.insert("0.0", "Tritanopia")
    tritanopia_text['state'] = 'disabled'

    image2 = Image.open(os.getcwd() + '/simulated_colorblindness_images/tritanopia.jpeg')
    image2 = image2.resize((350, 350))
    simulated = ImageTk.PhotoImage(image2)
    label2 = tk.Label(image=simulated)
    label2.image = simulated
    label2.grid(column=2, row=4, sticky='nw', padx=0, pady=0)

# Main Application Loop
window = tk.Tk()
window.title('Colorblind Correction in Images')
window.geometry('1080x800')

tmp_file = current_file
open_button = tk.Button(window, text='Open File', command=open_file)
open_button.grid(column=0, row=0, sticky='nw', padx=0, pady=0)

window.mainloop()
