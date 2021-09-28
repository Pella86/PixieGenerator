# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 08:36:28 2021

@author: maurop
"""

import PIL

import pathlib

import matplotlib.pyplot as plt
import matplotlib.patches as patches

import math

import Blocks
import FindBestBlock


texture_folder = pathlib.Path("./1.17.1/assets/minecraft/textures/block")




# load the model image
model_image = PIL.Image.open(pathlib.Path("./creeper_head.png"))

plt.imshow(model_image)
plt.show()


px_matrix = model_image.load()







first_px = [x / 256 for x in px_matrix[0, 0]]


if first_px[3] == 0:
    first_px = (1.0, 1.0, 1.0)
else:
    first_px = first_px[:3]

print(first_px)


FindBestBlock.draw_rectangle(first_px)

stack = FindBestBlock.top_matching_blocks(first_px)

stack.print_block_names()
stack.show_images()









# block_matrix = FindBestBlock.best_block_image(model_image)  

# size_x = len(block_matrix[0])
# size_y = len(block_matrix)

# print(size_x, size_y)

# for i in range(size_x):
#     print("\n")
#     for j in range(size_y):
#         print(block_matrix[j][i].name, end=" ")
    

          
            
# new_im = PIL.Image.new("RGB", size=(9 * 16, 9 * 16))
# new_px_matrix = new_im.load()
        
# for i in range(size_x):
#     for j in range(size_y):
#         new_im.paste(block_matrix[i][j].image, (i * 16, j * 16))
    
# plt.imshow(new_im)
# plt.show()
