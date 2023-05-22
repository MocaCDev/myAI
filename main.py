import cv2
import numpy as np
from color_attributes import C_Attr

src = cv2.imread('testIMG2.jpg', 1)
(b, g, r) = cv2.split(src)

r = r.flatten()
g = g.flatten()
b = b.flatten()

colors_count = {}

for i in range(len(b)):
    RGB = (r[i], g[i], b[i])
    if RGB in colors_count:
        colors_count[RGB] += 1
    else:
        colors_count[RGB] = 1

total_black = 0
total_red_b = 0
others = 0
others_list = []
IS_BLACK_BACK = False

color_attr = C_Attr()

for val in sorted(colors_count, key=colors_count.__getitem__):
    if color_attr.is_in_range(val, C_Attr.black, 'black'):
       total_black += 1 
    else:
        others_list.append(val)
        if color_attr.is_in_range(val, C_Attr.red, 'red') or color_attr.is_in_range(val, C_Attr.orange, 'orange'):
            total_red_b += 1            
        others += 1

if total_black > others: IS_BLACK_BACK = True
if total_red_b > total_black: print('All Red.')

if IS_BLACK_BACK:
    total_red = 0
    found_red = False
    red_vals = []
    
    for val in sorted(colors_count, key=colors_count.__getitem__):
        if found_red == True:
            if color_attr.is_in_range(val, C_Attr.black, 'black'):
                found_red = False
            continue
        
        if color_attr.is_in_range(val, C_Attr.red, 'red') or color_attr.is_in_range(val, C_Attr.orange, 'orange'):
            total_red += 1
            found_red = True
            red_vals.append(val)
    
    for i in red_vals:
        if color_attr.is_in_range(i, C_Attr.gray, 'gray'):
            total_red -= 1
                
    print(total_red)
    color_attr.finished()