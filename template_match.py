import cv2 as cv 
import numpy as np 
import uuid
from matplotlib import pyplot as plt

GREEN_TEMP = cv.imread('./data/template/green_note.png', 0)
RED_TEMP = cv.imread('./data/template/red_note.png', 0)
YELLOW_TEMP = cv.imread('./data/template/yellow_note.png', 0)
BLUE_TEMP = cv.imread('./data/template/blue_note.png', 0)
ORANGE_TEMP = cv.imread('./data/template/orange_note.png', 0)

GREEN_GLOW = cv.imread('./data/template/green_glow.png', 0)
RED_GLOW = cv.imread('./data/template/red_glow.png', 0)
YELLOW_GLOW = cv.imread('./data/template/yellow_glow.png', 0)
BLUE_GLOW = cv.imread('./data/template/blue_glow.png', 0)
ORANGE_GLOW = cv.imread('./data/template/orange_glow.png', 0)

GREEN_STAR_TEMP = cv.imread('./data/template/green_star.png', 0)
RED_STAR_TEMP = cv.imread('./data/template/red_star.png', 0)
YELLOW_STAR_TEMP = cv.imread('./data/template/yellow_star_trial.png', 0)
BLUE_STAR_TEMP = cv.imread('./data/template/blue_star.png', 0)
ORANGE_STAR_TEMP = cv.imread('./data/template/orange_star.png', 0)

Y_CORD = 6

def green_note_match(img):
    # 15, 0 
    # 145. 80 
    img_green = img[0:80, 15:145]
    
    res = cv.matchTemplate(img_green, GREEN_TEMP, cv.TM_CCOEFF_NORMED)
    res_glow = cv.matchTemplate(img_green, GREEN_GLOW, cv.TM_CCOEFF_NORMED)
    res_star = cv.matchTemplate(img_green, GREEN_STAR_TEMP, cv.TM_CCOEFF_NORMED)
    
    threshold = 0.5
    
    loc = np.where(res >= threshold)
    loc_glow = np.where(res_glow >= threshold)
    loc_star = np.where(res_star >= threshold)
    
    # min_val, max_val = cv.minMaxLoc(res)
    
    if(len(loc[0]) > 0):
        if (loc[0][0] > Y_CORD):
            return True
        else:
            return False
    elif(len(loc_star[0]) > 0):
        if(loc_star[0][0] > Y_CORD):
            return True
        else:
            return False
    elif(len(loc_glow[0]) > 0):
        if(loc_glow[0][0] > Y_CORD):
            return True
        else:
            return False
    else:
        return False    

def red_note_match(img):
    #150, 0 
    #288, 80
    img_red = img[0:80, 150:288]
    
    res = cv.matchTemplate(img_red, RED_TEMP, cv.TM_CCOEFF_NORMED)
    res_glow = cv.matchTemplate(img_red, RED_GLOW, cv.TM_CCOEFF_NORMED)
    res_star = cv.matchTemplate(img_red, RED_STAR_TEMP, cv.TM_CCOEFF_NORMED)
    
    threshold = 0.5
    
    loc = np.where(res >= threshold)
    loc_glow = np.where(res_glow >= threshold)
    loc_star = np.where(res_star >= threshold)
    
    if(len(loc[0]) > 0):
        if (loc[0][0] > Y_CORD):
            return True
        else:
            return False
    elif(len(loc_star[0]) > 0):
        if(loc_star[0][0] > Y_CORD):
            return True
        else:
            return False
    elif(len(loc_glow[0]) > 0):
        if(loc_glow[0][0] > Y_CORD):
            return True
        else:
            return False
    else:
        return False    

def yellow_note_match(img):
    #298, 0
    #434, 80
    img_yellow = img[0:80, 298:434]
    
    res = cv.matchTemplate(img_yellow, YELLOW_TEMP, cv.TM_CCOEFF_NORMED)
    res_glow = cv.matchTemplate(img_yellow, YELLOW_GLOW, cv.TM_CCOEFF_NORMED)
    res_star = cv.matchTemplate(img_yellow, YELLOW_STAR_TEMP, cv.TM_CCOEFF_NORMED)
    
    threshold = 0.6
    
    loc = np.where( res >= threshold)
    loc_glow = np.where(res_glow >= 0.63)
    loc_star = np.where(res_star >= threshold)
    
    if(len(loc[0]) > 0):
        if (loc[0][0] > Y_CORD):
            print(loc[0][0])
            print('--------------------------- Reg')
            return True
        else:
            return False
    elif(len(loc_star[0]) > 0):
        if(loc_star[0][0] > Y_CORD):
            print(loc_star[0][0])
            print('--------------------------- Star')
            return True
        else:
            return False
    elif(len(loc_glow[0]) > 0):
        if(loc_glow[0][0] > Y_CORD):
            print(loc_glow[0][0])
            print('--------------------------- Glow')
            return True
        else:
            return False
    else:
        return False        
    
def blue_note_match(img):
    #444, 0
    #581, 80
    img_blue = img[0:80, 444:581]
    
    res = cv.matchTemplate(img_blue, BLUE_TEMP, cv.TM_CCOEFF_NORMED)
    res_glow = cv.matchTemplate(img_blue, BLUE_GLOW, cv.TM_CCOEFF_NORMED)
    res_star = cv.matchTemplate(img_blue, BLUE_STAR_TEMP, cv.TM_CCOEFF_NORMED)
    
    threshold = 0.58
    
    loc = np.where(res >= threshold)
    loc_glow = np.where(res_glow >= threshold)
    loc_star = np.where(res_star >= threshold)
    
    if(len(loc[0]) > 0):
        if (loc[0][0] > Y_CORD):
            return True
        else:
            return False
    elif(len(loc_star[0]) > 0):
        if(loc_star[0][0] > Y_CORD):
            return True
        else:
            return False
    elif(len(loc_glow[0]) > 0):
        if(loc_glow[0][0] > Y_CORD):
            return True
        else:
            return False
    else:
        return False    
    
def orange_note_match(img):
    #591, 0
    #729, 80
    img_orange = img[0:80, 591:729]
    
    res = cv.matchTemplate(img_orange, ORANGE_TEMP, cv.TM_CCOEFF_NORMED)
    res_glow = cv.matchTemplate(img_orange, ORANGE_GLOW, cv.TM_CCOEFF_NORMED)
    res_star = cv.matchTemplate(img_orange, ORANGE_STAR_TEMP, cv.TM_CCOEFF_NORMED)
    
    threshold = 0.5
    
    loc = np.where(res >= threshold)
    loc_glow = np.where(res_glow >= threshold)
    loc_star = np.where(res_star >= threshold)
    
    if(len(loc[0]) > 0):
        if (loc[0][0] > Y_CORD):
            return True
        else:
            return False
    elif(len(loc_star[0]) > 0):
        if(loc_star[0][0] > Y_CORD):
            return True
        else:
            return False
    elif(len(loc_glow[0]) > 0):
        if(loc_glow[0][0] > Y_CORD):
            return True
        else:
            return False
    else:
        return False    
    
def match_all(img):
    pass_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    list = []
    if green_note_match(pass_img):
        list.append('a')
    if red_note_match(pass_img):
        list.append('s')
    if yellow_note_match(pass_img):
        list.append('d')
    if blue_note_match(pass_img):
        list.append('f')
    if orange_note_match(pass_img):
        list.append('g')
    return list
    
    # print('match all')






