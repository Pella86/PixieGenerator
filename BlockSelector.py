# -*- coding: utf-8 -*-
"""
Created on Sun Sep 26 22:17:24 2021

@author: maurop
"""

# =============================================================================
# Imports
# =============================================================================

import PIL

import os
import pathlib

import matplotlib.pyplot as plt

# =============================================================================
# Constants
# =============================================================================

# this is the folder found in the Minecraft folder containing all the textures
texture_folder = pathlib.Path("./Minecraft_version/1.17.1/assets/minecraft/textures/block")

# =============================================================================
# Program
# =============================================================================

# the program is used as a stand alone to filter which blocks can be used
# the program stores the names of the blocks that can be used for building
# it excludes blocks like wheat stages and grass

# read the good and bad block file
good_block_file = pathlib.Path("./good_blocks.txt")
bad_block_file = pathlib.Path("./bad_blocks.txt")

def load_block_list(file_path):
    block_list = []
    
    if file_path.is_file():
        
        with open(file_path, "r") as f:
            lines = f.readlines()
            
        for line in lines:
            block_list.append(line.strip())
            
        print("load_block_list:", file_path , "Loaded", len(block_list), "blocks")
            
        return block_list
            
        
    else:
        print("load_file: File not found", file_path)
        return block_list
    
# load the files if already present
good_blocks_filenames = load_block_list(good_block_file)
bad_blocks_filenames = load_block_list(bad_block_file)

# read all the blocks textures
files = os.listdir(texture_folder)

# for each texture ask the user if is fitting
for file in files:
    
    path = texture_folder / pathlib.Path(file)
    
    # chose only files that are .png
    if path.is_file() and path.suffix == ".png":
        
        im = PIL.Image.open(path)
        
        # chose only 16x16 block textures
        if im.size == (16, 16): 
            
            # chose if block is appropriate
            if file in good_blocks_filenames:
                print(file, "block already good")
                continue
                
            elif file in bad_blocks_filenames:
                print(file, "block already bad")
                continue
            
            else:
                
                # show the block
                plt.imshow(im)
                plt.show()
                
                # print the name of the block
                print(file)            
                
                # wait for user to decide
                user_input = input("is block appropriate: ")
                
                # if the user press enter the block is good, if the user gives
                # any character instead of q the block is considered bad
                # if the user gives q the program quits
                
                # the blocks will be appended to the file
        
                if user_input == "":
                    with open(good_block_file, "a") as f:
                        f.write(file + "\n")
                elif user_input != "q":
                    with open(bad_block_file, "a") as f:
                        f.write(file + "\n")
                else:
                    print("program quit")
                    break