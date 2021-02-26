#!/usr/bin/env python
# coding: utf-8

# In[340]:


import csv
from PIL import Image, ImageDraw

#VARIABLES
data = []
line = []
walls = []
width = 256
height = 256

#FUNCTIONS

#Import csv data from robot
def import_csv(filepath):
    global data
    
    if filepath[-4:] != '.csv':
        filepath += '.csv'
    
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append([row[0],row[1]])
        data.pop(0)
        for i in range(len(data)):
            data[i][0] = float(data[i][0])
            data[i][1] = float(data[i][1])
            
#Align data so it fits in the 1. quadrant of a 2D grid
def align_data():
    global width
    global height
    global data
    
    MARGIN = 1.4
    MAX_PIXELS = 1 * (10**6)
    
    #Find edges
    left = data[0][0]
    right = data[0][0]
    top = data[0][1]
    bottom = data[0][1]
    for i in range(1,len(data)):
        if data[i][0] < left:
            left = data[i][0]
        elif data[i][0] > right:
            right = data[i][0]
        if data[i][1] < top:
            top = data[i][1]
        elif data[i][1] > bottom:
            bottom = data[i][1]
    
    #Define image size
    width = (right - left) * MARGIN
    height = (bottom - top) * MARGIN
    
    #Find difference
    x_diff = (width/MARGIN * (MARGIN-1)/2) - left
    y_diff = (height/MARGIN * (MARGIN-1)/2) - top
    
    #Move data points
    for point in data:
        point[0] += x_diff
        point[1] += y_diff
        
    #Scale image
    pixel_amount = width * height
    if pixel_amount > MAX_PIXELS:
        ratio = MAX_PIXELS / (pixel_amount*1.01)
        for point in data:
            point[0] *= ratio
            point[1] *= ratio
        width *= ratio
        height *= ratio
        
    #Flip data points vertically
    mirror_line = height / 2
    for point in data:
        point[1] -= (point[1] - mirror_line)*2

#Draw single points
def img_points():
    global draw
    global data
    
    #Draw start-rectangle
    x0 = data[0]
    draw.rectangle((x0[0]-4,x0[1]-4,x0[0]+4,x0[1]+4), outline=(0,170,255))
    
    for i in range(len(data)):
        draw.point((data[i][0],data[i][1]), fill=128)

#Terminal
print("filename: ")
filepath = input()

import_csv(filepath)
align_data()

im = Image.new("RGB", (int(width), int(height)), color=(187,187,187))
draw = ImageDraw.Draw(im)

img_points()

im.show()
im.save("result.png")

