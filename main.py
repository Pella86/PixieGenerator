# -*- coding: utf-8 -*-
"""
Created on Sun Sep 26 14:22:30 2021

@author: maurop
"""

# =============================================================================
# Imports
# =============================================================================

import tkinter
from tkinter import filedialog


import pathlib

import PIL
from PIL import ImageTk


import FindBestBlock

# =============================================================================
# Simple canvas displaying an image
# =============================================================================

class ImageCanvas(tkinter.Canvas):
    
    def __init__(self, parent_frame, w, h):
        super().__init__(parent_frame, height=h, width=w)
        
        self.width = w
        self.height = h
        
    
    def display_image(self, image):
        # resize the image so that it fits the canvas
        # to do: handle non square pictures
        res_img = image.resize((self.width, self.height), PIL.Image.NEAREST)
        res_img = res_img.convert("RGBA")
        
        img = PIL.ImageTk.PhotoImage(res_img) 
        
        self.image = img

        self.create_image(self.width / 2, self.height / 2, image=img)         
        
        
# =============================================================================
# Original Image Frame        
# =============================================================================

class OriginalImage(tkinter.LabelFrame):
    
    def __init__(self, parent_frame):
        super().__init__(parent_frame, text="Original Image")
        
        # button to load images
        open_image = tkinter.Button(self, text="Load image", command=lambda : self.load_image())
        open_image.pack()
        
        # canvas to represent the loaded image
        self.canvas = ImageCanvas(self, 256, 256)
        self.canvas.pack()
             
        # default image
        image = PIL.Image.open(pathlib.Path("./creeper_head.png"))
        image = image.convert("RGB")
        
        self.image = image   
        
        self.canvas.display_image(self.image)
        
    def load_image(self):
        
        filename = tkinter.filedialog.askopenfilename()
        
        if filename:
            
            image = PIL.Image.open(filename)
            
            image = image.convert("RGB")
            
            self.image = image
            
            self.canvas.display_image(self.image)
            
            print("load_image: Loaded", pathlib.Path(filename).name)

# =============================================================================
# Frame Generate 
# =============================================================================

# labelled entry, an extension of entry with a label in front
        
class LabelEntry(tkinter.Frame):
    
    def __init__(self, root_frame, labeltext, default_value=None):
        super().__init__(root_frame)
        
        label = tkinter.Label(self, text=labeltext)
        label.grid(row=0, column=0)
        
        self.entry = tkinter.Entry(self, width=6)
        self.entry.grid(row=0, column=1)
        
        if default_value:
            self.entry.insert(0, str(default_value))
        
    def get(self):
        return self.entry.get()
    
    def get_int(self):
        try:
            self.entry.config({"background" : "white"})
            return int(self.entry.get())
        except ValueError:
            self.entry.config({"background" : "red"})
            return None
    
class GenerateFrame(tkinter.LabelFrame):
    
    def __init__(self, parent_frame, original_image_frame, resized_image_display,
                 block_display, block_list):
        super().__init__(parent_frame, text="Generate PixArt")
        
        self.size_x_entry = LabelEntry(self, "size x:", 9)
        self.size_x_entry.grid(row=0, column=0)

        self.size_y_entry = LabelEntry(self, "size y:", 9)
        self.size_y_entry.grid(row=0, column=1)
        
        b_generate = tkinter.Button(self, text="generate", command = lambda : self.generate())
        b_generate.grid(row=1, column=0, columnspan=2)
        
        
        self.original_image_frame = original_image_frame
        self.resized_image_display = resized_image_display
        self.block_display = block_display
        self.block_list = block_list
        
        
        
    def generate(self):
    
        print("Resizing Image")
        size_x = self.size_x_entry.get_int()
        size_y = self.size_y_entry.get_int()
        
        if size_x != None and size_y != None:
        
            res_image = self.original_image_frame.image.resize((size_x, size_y))
            
            self.resized_image_display.display_image(res_image)
            
            root.update_idletasks()
            
            print("Calculating blocks")
            block_matrix = FindBestBlock.best_block_image(res_image) 
            
            
            block_count = {}
            
            for i in range(size_x):
                for j in range(size_y):
                    block = block_matrix[i][j]
                    
                    try:
                        
                        block_count[block.name] += 1
                    
                    except KeyError:
                        block_count[block.name] = 1
                        
            
            print("Creating Image")
            size_x = len(block_matrix[0])
            size_y = len(block_matrix)
           
                    
            new_im = PIL.Image.new("RGB", size=(size_x * 16, size_y * 16))
            
            printed_blocks = []
            
            self.block_list.clear_list()
                    
            for i in range(size_x):
                for j in range(size_y):
                    block = block_matrix[i][j]
                    
                    new_im.paste(block.image, (i * 16, j * 16))
                    
                    if block.name not in printed_blocks:
                        print(block.name)
                        printed_blocks.append(block.name)
                        
                        self.block_list.add_block(block, block_count[block.name])
                        
            
            
                    
                    
            
            self.block_display.display_image(new_im)
            
            new_im.save("output.png")
            
    

# =============================================================================
# Block list display
# =============================================================================


        
class BlockListDisplay(tkinter.LabelFrame):
    
    def __init__(self, parent_frame):
        super().__init__(parent_frame, text="Block list")
        
        self.block_list = []
        
    
    def add_block(self, block, count):
        
        # create a frame linked to the name of the block
        
        block_frame = tkinter.Frame(self)
        block_frame.pack()
        
        # create a canvas to show the block
        
        image_canvas = ImageCanvas(block_frame, 16, 16)
        image_canvas.grid(row=0, column=0)
        image_canvas.display_image(block.image)
        
        # label for the name and count
        name = block.name.replace("_", " ")
        label = tkinter.Label(block_frame, text=f"{name}: {count}")
        label.grid(row=0, column=1)
        
        self.block_list.append(block_frame)
        

    def clear_list(self):
        
        for frame in self.block_list:
            frame.destroy()

        self.block_list = []
        
    
    
        
        
        
        

            
        
        
        

root = tkinter.Tk()

original_image = OriginalImage(root)
original_image.grid(row=0, column=0)


# resized image display   

resized_image_display = ImageCanvas(root, 256, 256)
resized_image_display.grid(row=0, column=2)

# blocks display

block_display = ImageCanvas(root, 256, 256)
block_display.grid(row=0, column=3)

# block list display
block_list = BlockListDisplay(root)
block_list.grid(row=0, column=4)

# generate function

generate = GenerateFrame(root, original_image, resized_image_display, block_display, block_list)
generate.grid(row=0, column = 1)


root.mainloop()
