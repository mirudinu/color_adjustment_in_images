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

'''
Conversion matrices
https://daltonlens.org/understanding-cvd-simulation/
'''
'''
LMS = RGB2LMS_matrix * RGB
'''
# RGB2LMS_matrix = np.array(  [[0.3904725 , 0.54990437, 0.00890159],
#                             [0.07092586, 0.96310739, 0.00135809],
#                             [0.02314268, 0.12801221, 0.93605194]
#                             ], dtype=np.float16)
RGB2LMS_matrix = np.array([[17.88240413, 43.51609057,  4.11934969],
         [ 3.45564232, 27.15538246,  3.86713084],
         [ 0.02995656,  0.18430896,  1.46708614]])
'''
LMS_protanopia = LMS2LMSp_matrix * LMS
'''
# LMS2LMSp_matrix = np.array( [[0, 0.90822864, 0.008192],
#                             [0, 1, 0],
#                             [0, 0, 1]
#                             ], dtype=np.float16)
LMS2LMSp_matrix = np.array( [[0.0, 2.02344377, -2.52580405],
                            [0.0, 1.0, 0.0],
                            [0.0, 0.0, 1.0]])
'''
LMS_deuteranopia = LMS2LMSp_matrix * LMS
'''
# LMS2LMSd_matrix = np.array( [[1, 0, 0],
#                             [1.10104433, 0, -0.00901975],
#                             [0, 0, 1]
#                             ], dtype=np.float16)
LMS2LMSd_matrix = np.array( [[1.0, 0.0, 0.0],
                            [0.49420696, 0.0, 1.24826995],
                            [0.0, 0.0, 1.0]])
'''
LMS_tritanopia = LMS2LMSt_matrix * LMS
'''
# LMS2LMSt_matrix = np.array( [[1, 0, 0],
#                             [0, 1, 0],
#                             [-0.15773032,  1.19465634, 0]
#                             ], dtype=np.float16)
LMS2LMSt_matrix = np.array( [[ 1.0, 0.0, 0.0],
                            [ 0.0, 1.0, 0.0],
                            [-0.01224491, 0.07203435, 0.0]])
'''
RGB = LMS2RGB_matrix * LMS
'''
# LMS2RGB_matrix = np.array(  [[ 2.85831110e+00, -1.62870796e+00, -2.48186967e-02],
#                             [-2.10434776e-01,  1.15841493e+00,  3.20463334e-04],
#                             [-4.18895045e-02, -1.18154333e-01,  1.06888657e+00]
#                             ], dtype=np.float16)
LMS2RGB_matrix = np.array(  [[ 0.0809, -0.1305, 0.1167],
                             [-0.0102, 0.0540, -0.1136],
                             [-0.0004, -0.0041, 0.6935]])

gamma = 2.2
def sRGB2linearRGB(srgb_image):
    for i in range (srgb_image.shape[0]):
        for j in range (srgb_image.shape[1]):
            [r,g,b] = srgb_image[i,j]
            r = pow(r, gamma)
            g = pow(g, gamma)
            b = pow(b, gamma)
            srgb_image[i,j] = [r, g, b]

one_over_gamma = 1.0 / 2.2
def linearRGB2sRGB(rgb_image):
    for i in range (rgb_image.shape[0]):
        for j in range (rgb_image.shape[1]):
            [r,g,b] = rgb_image[i,j]
            r = pow(r, one_over_gamma)
            g = pow(g, one_over_gamma)
            b = pow(b, one_over_gamma)
            rgb_image[i,j] = [r, g, b]

def simulate_colorblindness(type):
    original_image = cv2.imread(current_file)

    # Reorder channels BGR -> RGB
    red = original_image[:,:,2]
    green = original_image[:,:,1]
    blue = original_image[:,:,0]

    rgb_image = np.zeros(original_image.shape)
    rgb_image[:,:,0] = red
    rgb_image[:,:,1] = green
    rgb_image[:,:,2] = blue

    sRGB2linearRGB(rgb_image)

    # Convert RGB->LMS
    lms_image = rgb_image @ RGB2LMS_matrix.T
    # Simulate colorblindness in LMS
    colorblind_simulation_matrix = LMS2LMSp_matrix
    if type == 'deuteranopia':
        colorblind_simulation_matrix = LMS2LMSd_matrix
    elif type == 'tritanopia':
        colorblind_simulation_matrix = LMS2LMSt_matrix
    lms_colorblind_image = lms_image @ colorblind_simulation_matrix.T
    # Convert LMS->RGB
    rbg_colorblind_image = lms_colorblind_image @ LMS2RGB_matrix.T

    # Reorder channels RGB->BGR
    bgr_colorblind_image = np.zeros(original_image.shape)
    bgr_colorblind_image[:,:,0] = rbg_colorblind_image[:,:,2]
    bgr_colorblind_image[:,:,1] = rbg_colorblind_image[:,:,1]
    bgr_colorblind_image[:,:,2] = rbg_colorblind_image[:,:,0]

    linearRGB2sRGB(bgr_colorblind_image)

    # Save result image
    result_image_path = simulated_protanopia_path
    if type == 'deuteranopia':
        result_image_path = simulated_deuteranopia_path
    elif type == 'tritanopia':
        result_image_path = simulated_tritanopia_path
    cv2.imwrite(result_image_path, bgr_colorblind_image)

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
    simulate_colorblindness('protanopia')
    display_protanopia_simulation() 

    # Insert Simulated Deuteranopia Image
    simulate_colorblindness('deuteranopia')
    display_deuteranopia_simulation()

    # Insert Simulated Tritanopia Image
    simulate_colorblindness('tritanopia')
    display_tritanopia_simulation()
    

# Main Application Loop
window = tk.Tk()
window.title('Colorblind Correction in Images')
window.geometry('1080x800')

tmp_file = current_file
open_button = tk.Button(window, text='Open File', command=open_file)
open_button.grid(column=0, row=0, sticky='nw', padx=0, pady=0)

window.mainloop()
