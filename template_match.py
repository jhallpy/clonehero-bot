import cv2 as cv 
import numpy as np 
import uuid
from matplotlib import pyplot as plt

# GREEN_TEMP = cv.cvtColor(cv.imread('./data/template/green_note.png', cv.IMREAD_UNCHANGED), cv.COLOR_BGR2RGB)
# RED_TEMP = cv.cvtColor(cv.imread('./data/template/red_note.png', cv.IMREAD_UNCHANGED), cv.COLOR_BGR2RGB)
# YELLOW_TEMP = cv.cvtColor(cv.imread('./data/template/yellow_note.png', cv.IMREAD_UNCHANGED), cv.COLOR_BGR2RGB)
# BLUE_TEMP = cv.cvtColor(cv.imread('./data/template/blue_note.png', cv.IMREAD_UNCHANGED), cv.COLOR_BGR2RGB)
# ORANGE_TEMP = cv.cvtColor(cv.imread('./data/template/orange_note.png', cv.IMREAD_UNCHANGED), cv.COLOR_BGR2RGB)

GREEN_TEMP = cv.cvtColor(cv.imread('./data/template/green_test2.png', cv.IMREAD_UNCHANGED), cv.COLOR_BGR2RGB)
RED_TEMP = cv.cvtColor(cv.imread('./data/template/red_test.png', cv.IMREAD_UNCHANGED), cv.COLOR_BGR2RGB)
YELLOW_TEMP = cv.cvtColor(cv.imread('./data/template/yellow_test.png', cv.IMREAD_UNCHANGED), cv.COLOR_BGR2RGB)
BLUE_TEMP = cv.cvtColor(cv.imread('./data/template/blue_test.png', cv.IMREAD_UNCHANGED), cv.COLOR_BGR2RGB)
ORANGE_TEMP = cv.cvtColor(cv.imread('./data/template/orange_test.png', cv.IMREAD_UNCHANGED), cv.COLOR_BGR2RGB)

GREEN_GLOW = cv.cvtColor(cv.imread('./data/template/green_glow.png', cv.IMREAD_UNCHANGED), cv.COLOR_BGR2RGB)
# RED_GLOW = cv.imread('./data/template/red_glow.png', 0)
# YELLOW_GLOW = cv.imread('./data/template/yellow_glow.png', 0)
# BLUE_GLOW = cv.imread('./data/template/blue_glow.png', 0)
# ORANGE_GLOW = cv.imread('./data/template/orange_glow.png', 0)

GREEN_STAR_TEMP = cv.cvtColor(cv.imread('./data/template/green_star.png', cv.IMREAD_UNCHANGED), cv.COLOR_BGR2RGB)
RED_STAR_TEMP = cv.imread('./data/template/red_star.png', 0)
YELLOW_STAR_TEMP = cv.imread('./data/template/yellow_star_trial.png', 0)
BLUE_STAR_TEMP = cv.imread('./data/template/blue_star.png', 0)
ORANGE_STAR_TEMP = cv.imread('./data/template/orange_star.png', 0)

Y_CORD = 6

def green_note_match(img):
    # 15, 0 
    # 145. 80 
    img_green = img[5:80, 15:146]
    
    res = cv.matchTemplate(img_green, GREEN_TEMP, cv.TM_CCOEFF_NORMED)
    
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    
    # TODO: 0.35 is max I think?
    if(max_val > 0.20):
        print(str(max_val) + ' ' + str(max_loc))
        return True
    else:
        return False    

def red_note_match(img):
    #150, 0 
    #288, 80
    img_red = img[0:80, 150:288]
    
    res = cv.matchTemplate(img_red, RED_TEMP, cv.TM_CCOEFF_NORMED)
    
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    
    
    #0.23 is the minimum to not catch the note playing spot.
    if(max_val > 0.295):
        # print(max_val)
        return True
    else:
        return False   

def yellow_note_match(img):
    #298, 0
    #434, 80
    img_yellow = img[0:80, 298:434]
    
    res = cv.matchTemplate(img_yellow, YELLOW_TEMP, cv.TM_CCOEFF_NORMED)
    
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    
    # 0.3741 lowest number to miss post so far.
    if(max_val > 0.3741):
        # print(max_val)
        return True
    else:
        return False       
    
def blue_note_match(img):
    #444, 0
    #581, 80
    img_blue = img[0:80, 444:581]
    
    res = cv.matchTemplate(img_blue, BLUE_TEMP, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    
    # 0.2832 lowest value for missing the post so far.
    if(max_val > 0.2832):
        # print(max_val)
        return True
    else:
        return False  
    
def orange_note_match(img):
    #591, 0
    #729, 80
    img_orange = img[0:80, 591:729]
    
    res = cv.matchTemplate(img_orange, ORANGE_TEMP, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    
    if(max_val > 0.2):
        # print(max_val)
        return True
    else:
        return False  
    
def match_all(img):
    # pass_img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    list = []
    if green_note_match(img):
        list.append('a')
    # if red_note_match(img):
    #     list.append('s')
    # if yellow_note_match(img):
    #     list.append('d')
    # if blue_note_match(img):
    #     list.append('f')
    # if orange_note_match(img):
    #     list.append('g')
    return list
    
    # print('match all')






