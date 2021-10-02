# -*- coding: utf-8 -*-
"""
Created on Sun Sep 26 14:22:30 2021

@author: maurop
"""

# =============================================================================
# Imports
# =============================================================================

# tkinter import
import tkinter
from tkinter import filedialog
from tkinter import scrolledtext

# Python Image Library imports
import PIL
from PIL import ImageTk

# py imports
import pathlib

# my imports
import FindBestBlock

# =============================================================================
# Simple canvas displaying an image
# =============================================================================

class ImageCanvas(tkinter.Canvas):
    
    def __init__(self, parent_frame, w, h):
        super().__init__(parent_frame, height=h, width=w)
        
        self.width = w
        self.height = h
        self.image = None
        
    
    def display_image(self, image):
        # store the image
        self.image = image
        print(self.image.size)
        
        # resize the image so that it fits the canvas
        # to do: handle non square pictures
        res_img = image.resize((self.width, self.height), PIL.Image.NEAREST)
        res_img = res_img.convert("RGBA")
        
        img = ImageTk.PhotoImage(res_img) 

        self.image_reference = img

        self.create_image(self.width / 2, self.height / 2, image=img)   
        

class SelectPixelImageBase(ImageCanvas):
    ''' This class is the base class for images where you can click a pixel
    and the x most similar pixel will be shown in a list'''

    def __init__(self, parent_frame, w, h, block_list_display):
        super().__init__(parent_frame, w, h)
        
        # assign the widget where the similar blocks will be displayed
        self.block_list_display = block_list_display 
        
        # bind the mouse button
        self.bind("<Button-1>", lambda event : self.click(event))
        
        # have a matrix of colors
        self.matrix = []

    def click(self, event):
        # when the user clicks the coordinates clicked needs to be converted
        # into the color matrix
        i, j = self.convert_coord_clicked_matrix(event)
        
        # once converted we access the color
        color = self.matrix[i][j]
        
        # which we show in the widget with similar colors
        self.display_blocks(color)        

    def display_blocks(self, color): 
        # first find the 10 most similar blocks
        stack = FindBestBlock.top_matching_blocks(color) 
        
        # clear the widget
        self.block_list_display.clear_list()
        
        # show the block and the % in similarity
        
        # calculate which has the most distance
        max_d = max([d for _, d in stack.stack])
        
        # it will be shown the blocks + the similarity in %
        for block, d in stack.stack:
            wd = 100 - d / max_d * 100
            strd = f"{wd:.1f}%"
            # same block will show a 100% similarity
            self.block_list_display.add_block(block, strd)
    
    def limit_click_coords(self, event):  
        # sometimes the user can click slightly off the image, since thecanvas
        # has some remaining pixels, this limits the click to the image size
        x = event.x if event.x <= self.width - 1 else self.width - 1
        y = event.y if event.y <= self.height - 1 else self.height - 1
        return x, y
    
    # methods to be overridden by the subclasses
    
    def convert_coord_clicked_matrix(self, event):
        pass
    
    def set_color_matrix(self):
        pass
    
    

class SelectBlockImage(SelectPixelImageBase):
    ''' This class will hold the blocks image if clicked the most similar
    block in the image to the blocks will be shown'''
    
    
    def __init__(self, parent_frame, w, h, block_list_display):
        super().__init__(parent_frame, w, h, block_list_display)
                
        
    def set_color_matrix(self, block_matrix):
        self.matrix = []
        
        # takes the block matrix and calculates a color matrix based on the
        # average color
        
        lex = len(block_matrix)
        ley = len(block_matrix[0])
        
        for i in range(lex):
            self.matrix.append([])
            for j in range(ley):
                self.matrix[i].append(block_matrix[i][j].average_color())
        
            
    def convert_coord_clicked_matrix(self, event):
        # make sure the click is inside the image coordinates 
        x, y = self.limit_click_coords(event)
        
        # convert the click into "block coordinates"
        i = int(x / self.width * self.image.size[0] / 16)
        j = int(y / self.height * self.image.size[1] / 16)
        
        return i, j        
        
class SelectPixelImage(SelectPixelImageBase):
    def __init__(self, parent_frame, w, h, block_list_display):
        super().__init__(parent_frame, w, h, block_list_display)
        
    def set_color_matrix(self):
        self.matrix = []
        # converts the image color pixels in the color matrix I use
        
        print("set_color_matrix:", self.image.size)
        
        px_matrix = self.image.load()
        
        for i in range(self.image.size[0]):
            self.matrix.append([])
            for j in range(self.image.size[1]):
                color = px_matrix[i, j]
                color = [c / 256 for c in color]
                
                self.matrix[i].append(color)

            
    def convert_coord_clicked_matrix(self, event):
        x, y = self.limit_click_coords(event)
        
        i = int(x / self.width * self.image.size[0])
        j = int(y / self.height * self.image.size[1])

        return i, j               
    
    
        
        
# =============================================================================
# Original Image Frame        
# =============================================================================

class OriginalImage(tkinter.LabelFrame):
    ''' This class will hold the original picture and allow the user to load
    an image from disk'''
    
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
   
        
        self.canvas.display_image(image)
        
    def get_image(self):
        print("get_image:", self.canvas.image.size)
        return self.canvas.image
        
        
    def load_image(self):
        
        filename = filedialog.askopenfilename()
        
        if filename:
            
            image = PIL.Image.open(filename)
            
            image = image.convert("RGB")

            self.canvas.display_image(image)
            
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
        
        # size in blocks for the new created image
        self.size_x_entry = LabelEntry(self, "size x:", 9)
        self.size_x_entry.grid(row=0, column=0)

        self.size_y_entry = LabelEntry(self, "size y:", 9)
        self.size_y_entry.grid(row=0, column=1)
        
        # button that will generate the block composition
        b_generate = tkinter.Button(self, text="generate", command = lambda : self.generate())
        b_generate.grid(row=1, column=0, columnspan=2)
        
        # the various displays that will be called by generate
        self.original_image_frame = original_image_frame
        self.resized_image_display = resized_image_display
        self.block_display = block_display
        self.block_list = block_list
        
        # generate the images
        self.generate()
        
        
        
    def generate(self):
    
        
        
        # get the user wanted size for the pixel art
        size_x = self.size_x_entry.get_int()
        size_y = self.size_y_entry.get_int()
        
        if size_x != None and size_y != None:
            
            print("Resizing Image")
            
            original_image = self.original_image_frame.get_image()
        
            res_image = original_image.resize((size_x, size_y), PIL.Image.NEAREST)
            
            self.resized_image_display.display_image(res_image)
            self.resized_image_display.set_color_matrix()
            
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

                        printed_blocks.append(block.name)
                        
                        self.block_list.add_block(block, block_count[block.name])
                        
            
            
                    
            self.block_display.set_color_matrix(block_matrix)      
            
            self.block_display.display_image(new_im)
            
            
            
            new_im.save("output.png")
            
    

# =============================================================================
# Block list display
# =============================================================================
            
class BlockListDisplay(tkinter.LabelFrame):
    
    def __init__(self, parent_frame, title):
        super().__init__(parent_frame, text=title)

        self.scroll_text = scrolledtext.ScrolledText(self, width=40, height=17)
        self.scroll_text.pack()
        
        self.scroll_text.images = []
    
    def add_block(self, block, count):
        
        img = ImageTk.PhotoImage(block.image)
        self.scroll_text.image_create(tkinter.END, image=img)
        self.scroll_text.images.append(img)
        
        name = block.name.replace("_", " ")
        self.scroll_text.insert(tkinter.END, f"{name}: {count}\n")
        
    def clear_list(self):
        self.scroll_text.delete("1.0", tkinter.END)
        self.scroll_text.images = []



    
    
        
        
        
        

            
        
        
        

root = tkinter.Tk()

original_image = OriginalImage(root)
original_image.grid(row=0, column=0)





# similar blocks list display
similar_block_list = BlockListDisplay(root, "Similar blocks")
similar_block_list.grid(row=1, column=2)

# resized image display   

resized_image_display = SelectPixelImage(root, 256, 256, similar_block_list)
resized_image_display.grid(row=0, column=2)

# blocks display

block_display = SelectBlockImage(root, 256, 256, similar_block_list)
block_display.grid(row=1, column=0)

# block list display
block_list = BlockListDisplay(root, "Block list")
block_list.grid(row=1, column=1)




# generate function

generate = GenerateFrame(root, original_image, resized_image_display, block_display, block_list)
generate.grid(row=0, column = 1)


root.mainloop()
