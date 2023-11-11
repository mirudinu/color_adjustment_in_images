import numpy as np
import os
# opencv for operations on images
import cv2

# tkinter for GUI
import tkinter as tk
from tkinter import filedialog as fd
from PIL import ImageTk, Image  

current_file = 'No file selected'
image_name = ''
simulated_protanopia_path = ''
simulated_deuteranopia_path = ''
simulated_tritanopia_path = ''
crt_dir = os.getcwd()

def simulate_protanopia():
    original_image = cv2.imread(current_file)
    print(simulated_protanopia_path + " :)")
    cv2.imwrite(simulated_protanopia_path, original_image)

def simulate_deuteranopia():
    original_image = cv2.imread(current_file)
    cv2.imwrite(simulated_deuteranopia_path, original_image)

def simulate_tritanopia():
    original_image = cv2.imread(current_file)
    cv2.imwrite(simulated_tritanopia_path, original_image)

def display_protanopia_simulation():
    protanopia_text = tk.Text(window, height=1, width = 40)
    protanopia_text.grid(column=0, row=3, sticky='nw', padx=0, pady=0)
    protanopia_text.insert("0.0", "Protanopia")
    protanopia_text['state'] = 'disabled'

    image2 = Image.open(simulated_protanopia_path)
    image2 = image2.resize((350, 350))
    simulated = ImageTk.PhotoImage(image2)
    label2 = tk.Label(image=simulated)
    label2.image = simulated
    label2.grid(column=0, row=4, sticky='nw', padx=0, pady=0)

def display_deuteranopia_simulation():
    deuteranopia_text = tk.Text(window, height=1, width = 40)
    deuteranopia_text.grid(column=1, row=3, sticky='nw', padx=0, pady=0)
    deuteranopia_text.insert("0.0", "Deuteranopia")
    deuteranopia_text['state'] = 'disabled'

    image2 = Image.open(simulated_deuteranopia_path)
    image2 = image2.resize((350, 350))
    simulated = ImageTk.PhotoImage(image2)
    label2 = tk.Label(image=simulated)
    label2.image = simulated
    label2.grid(column=1, row=4, sticky='nw', padx=0, pady=0)

def display_tritanopia_simulation():
    tritanopia_text = tk.Text(window, height=1, width = 40)
    tritanopia_text.grid(column=2, row=3, sticky='nw', padx=0, pady=0)
    tritanopia_text.insert("0.0", "Tritanopia")
    tritanopia_text['state'] = 'disabled'

    image2 = Image.open(simulated_tritanopia_path)
    image2 = image2.resize((350, 350))
    simulated = ImageTk.PhotoImage(image2)
    label2 = tk.Label(image=simulated)
    label2.image = simulated
    label2.grid(column=2, row=4, sticky='nw', padx=0, pady=0)


def open_file():
    global current_file, image_name, simulated_protanopia_path, simulated_deuteranopia_path, simulated_tritanopia_path
    filetypes = ( ('jpeg files', '*.jpeg'), ('jpg files', '*.jpg'), ('png files', '*.png'), ('All files', '*.*') )

    # get new image path
    current_file = fd.askopenfilename(initialdir = os.getcwd(),title = "Select file",filetypes = filetypes)
    image_name = os.path.splitext(os.path.basename(current_file))[0]
    simulated_protanopia_path = crt_dir + '/simulated_colorblindness_images/' + image_name + '_protanopia.jpeg'
    simulated_deuteranopia_path = crt_dir + '/simulated_colorblindness_images/' + image_name + '_deuteranopia.jpeg'
    simulated_tritanopia_path = crt_dir + '/simulated_colorblindness_images/' + image_name + '_tritanopia.jpeg'

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
    display_protanopia_simulation() 

    # Insert Simulated Deuteranopia Image
    simulate_deuteranopia()
    display_deuteranopia_simulation()

    # Insert Simulated Tritanopia Image
    simulate_tritanopia()
    display_tritanopia_simulation()
    

# Main Application Loop
window = tk.Tk()
window.title('Colorblind Correction in Images')
window.geometry('1080x800')

tmp_file = current_file
open_button = tk.Button(window, text='Open File', command=open_file)
open_button.grid(column=0, row=0, sticky='nw', padx=0, pady=0)

window.mainloop()
