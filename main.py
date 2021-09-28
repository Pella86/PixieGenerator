# -*- coding: utf-8 -*-
"""
Created on Sun Sep 26 14:22:30 2021

@author: maurop
"""

import tkinter
import pathlib

from tkinter import filedialog
from PIL import ImageTk

import PIL


import FindBestBlock


class ImageCanvas(tkinter.Canvas):
    
    def __init__(self, parent_frame, w, h):
        super().__init__(parent_frame, height=h, width=w)
        
        self.width = w
        self.height = h
        
    
    def display_image(self, image):
        
        
        print("display_image")
        res_img = image.resize((self.width, self.height), PIL.Image.NEAREST)
        res_img = res_img.convert("RGBA")
        
        img = PIL.ImageTk.PhotoImage(res_img) 
        
        self.image = img
        

        self.create_image(self.width / 2, self.height / 2, image=img)         
        
        
        







# Original Image

class OriginalImage(tkinter.Frame):
    
    def __init__(self, parent_frame):
        super().__init__(parent_frame)
        
        # default image
        
        image = PIL.Image.open(pathlib.Path("./creeper_head.png"))
        
        image = image.convert("RGB")
        
        self.image = image
        
        open_image = tkinter.Button(self, text="Load image", command=lambda : self.load_image())
        open_image.pack()
        
        
        self.canvas = ImageCanvas(self, 256, 256)
        self.canvas.pack()
        
        
        
        self.canvas.display_image(self.image)
        
    def load_image(self):
        
        filename = tkinter.filedialog.askopenfilename()
        print("load_image", filename)
        
        if filename:
            
            image = PIL.Image.open(filename)
            
            image = image.convert("RGB")
            
            self.image = image
            
            self.canvas.display_image(self.image)

 

# frame generate
        
class LabelEntry(tkinter.Frame):
    
    def __init__(self, root_frame, labeltext, default_value=None):
        super().__init__(root_frame)
        
        label = tkinter.Label(self, text=labeltext)
        label.grid(row=0, column=0)
        
        self.entry = tkinter.Entry(self)
        self.entry.grid(row=0, column=1)
        
        if default_value:
            self.entry.insert(0, str(default_value))
        
    def get(self):
        return self.entry.get()
    
    def get_int(self):
        return int(self.entry.get())
    
    

            
        
        
        

root = tkinter.Tk()

oi = OriginalImage(root)
oi.grid(row=0, column=0)

# size selector

size_select_frame = tkinter.Frame(root)
size_select_frame.grid(row=0, column=1)

size_x_entry = LabelEntry(size_select_frame, "size x:", 9)
size_x_entry.grid(row=0, column=0)

size_y_entry = LabelEntry(size_select_frame, "size y:", 9)
size_y_entry.grid(row=0, column=1)

def generate():
    
    print("Resizing Image")
    
    size_x = size_x_entry.get_int()
    size_y = size_y_entry.get_int()
    
    res_image = oi.image.resize((size_x, size_y))
    
    resized_image_display.display_image(res_image)
    
    root.update_idletasks()
    
    print("Calculating blocks")
    block_matrix = FindBestBlock.best_block_image(res_image)  
    
    print("Creating Image")
    size_x = len(block_matrix[0])
    size_y = len(block_matrix)
   
            
    new_im = PIL.Image.new("RGB", size=(size_x * 16, size_y * 16))
    
    printed_blocks = []
            
    for i in range(size_x):
        for j in range(size_y):
            block = block_matrix[i][j]
            
            new_im.paste(block.image, (i * 16, j * 16))
            
            if block.name not in printed_blocks:
                print(block.name)
                printed_blocks.append(block.name)
            
            
    
    block_display.display_image(new_im)
    
    new_im.save("output.png")
            
    
    
    
    
 

b_generate = tkinter.Button(size_select_frame, text="generate", command = generate)
b_generate.grid(row=1, column=0, columnspan=2)


# resized image display   

resized_image_display = ImageCanvas(root, 256, 256)
resized_image_display.grid(row=0, column=2)

# blocks display

block_display = ImageCanvas(root, 256, 256)
block_display.grid(row=0, column=3)


root.mainloop()
