# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 08:03:00 2021

@author: maurop
"""

import math

import matplotlib.pyplot as plt
import matplotlib.patches as patches

import Blocks


blocks = Blocks.load_blocks()

def draw_rectangle(color, ax = None):
    if ax == None:
        fig, ax = plt.subplots()

    ax.add_patch(patches.Rectangle((0,0), 1, 1, facecolor=color))
    
    plt.show()


def distance(p1, p2):
    
    sq = 0
    
    for i in range(3):
        sq += (p2[i] - p1[i])**2
    
    return math.sqrt(sq)

def wdistance(c1, c2):
    
    c1 = [x * 256 for x in c1]
    c2 = [x * 256 for x in c2]
    
    R1 = c1[0]
    G1 = c1[1]
    B1 = c1[2]
    
    R2 = c2[0]
    G2 = c2[1]
    B2 = c2[2]
    
    
    r = (R1 + R2) / 2
    
    DR = R1 - R2
    DG = G1 - G2
    DB = B1 - B2
    

    dc = math.sqrt((2 + r /256) * DR ** 2 + 4 * DG ** 2 + (2 + (255 - r)/256) * DB ** 2)
    
    return dc



def best_block(color):
    
    mind = None
    best_block = None
    
    for block in blocks:
        
        dblock = wdistance(color, block.average_color())
        
        if mind == None:
            mind = dblock
            best_block = block
            
            
        elif dblock < mind:
        
            mind = dblock
            best_block = block
    
    return best_block



def best_block_image(image):
    
    dim = image.size
    
    colors_analyzed = {}
    
    px_matrix = image.load()
    
    block_matrix = []
    
    for i in range(dim[0]):
        
        row = []
        block_matrix.append(row)

        for j in range(dim[1]):
            
            px = px_matrix[i, j]
            
            color = tuple([x / 256 for x in px])
            
            if color in colors_analyzed:
                row.append(colors_analyzed[color])
            else:
                bblock = best_block(color)
            
                colors_analyzed[color] = bblock
                
                row.append(bblock)
    
    return block_matrix
            
            
class Stack:
    
    def __init__(self):
        
        self.stack_size = 20
        
        self.stack = []
        
        self.refused_blocks = []
    
    
    def add(self, block, distance):
        
        for b, _ in self.stack:
            if block == b:
                print("block already in stack")
                return
        
        for b, _ in self.refused_blocks:
            if block == b:
                print("block lready refused")
        
        
        
        
        if len(self.stack) < self.stack_size:
            self.stack.append((block, distance))
        
        else:
            # append
            
            self.stack.append((block, distance))
            
            # sort
            
            self.stack.sort(key=lambda i : i[1])
            
            # pop
            
            refused = self.stack.pop()
            
            self.refused_blocks.append(refused)
            
    def print_block_names(self):
        for block, distance in self.stack:
            print(block.name, f"{distance:.2f}", [f"{x:.2f}" for x in block.average_color()])
    
    def show_images(self):
        
        for block, _ in self.stack:
        
            fig, axs = plt.subplots(nrows=1, ncols=2)
        
            axs[0].imshow(block.image)
            
            draw_rectangle(block.average_color(), axs[1])
            

def top_matching_blocks(color):
    stack = Stack()


    for block in blocks:
        
        dblock = wdistance(color, block.average_color())
        
        stack.add(block, dblock)  
    
    return stack
