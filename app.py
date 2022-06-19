#Importing PIL to grab a screenshot of the screen
import keyboard
import numpy as np
import time
from pynput.keyboard import Key, Controller
import cv2
import dxcam
from PIL import Image

camera = dxcam.create()
key = Controller()
dxcam.device_info()

def main(run, ready):
    while(run):
        if not ready and keyboard.is_pressed('F1'):
            ready = True
            releaseAll()
            Play(ready)
            run = False
        elif keyboard.is_pressed('F3'):
            releaseAll()
            camera.stop()
            KeyboardInterrupt()
            break
    
def Play(ready):
    
        last_time = currentTime()
        
        capture_area = (650,850,1325,970)
        img = camera.grab(capture_area)
        cv2.imwrite('test_image.png', img)
        i=0
        
        #77,109 80,112
        green_bg = img[109:113, 77:81]
        # #224,111
        # red_bg = img[111:114, 224:227]
        # 224,103
        red_bg = img[103:106, 224:227]
        #370,111
        yellow_bg = img[111:114, 370:373]
        # 515,115
        blue_bg = img[115:118, 515:518]
        
        
        while(ready):
            
            notes = []
            
            if keyboard.is_pressed('F2'):
                camera.stop()
                ready = False
                releaseAll()
                print('-----------')
                main(True, False)
                break
            
            img = camera.grab(capture_area)
            
            
            
            if not (img is None):
                green_check = img[109:113, 77:81]
                red_check = img[106:109, 224:227]
                yellow_check = img[111:114, 370:373]
                blue_check = img[115:118, 515:518]
            else:
                continue
            
            green_diff = cv2.subtract(np.asarray(green_check), np.asarray(green_bg)) + cv2.subtract(np.asarray(green_bg), np.asarray(green_check))
            green_diff[abs(green_diff) < 20.0] = 0
            
            red_diff = cv2.subtract(np.asarray(red_check), np.asarray(red_bg)) + cv2.subtract(np.asarray(red_bg), np.asarray(red_check))
            red_diff[abs(red_diff) < 58.0] = 0
            
            yellow_diff = cv2.subtract(np.asarray(yellow_check), np.asarray(yellow_bg)) + cv2.subtract(np.asarray(yellow_bg), np.asarray(yellow_check))
            yellow_diff[abs(yellow_diff) < 21.0] = 0
            
            blue_diff = cv2.subtract(np.asarray(blue_check), np.asarray(blue_bg)) + cv2.subtract(np.asarray(blue_bg), np.asarray(blue_check))
            blue_diff[abs(blue_diff) < 20.0] = 0
            
            if(np.sum(green_diff)<=250 and np.sum(red_diff)<=200):
                continue
                
            if(np.sum(green_diff)>250):
                print('Green:   ' +str(np.sum(green_diff)))
                notes.append('a')
            if(np.sum(red_diff)>200):
                print('Red:   ' +str(np.sum(red_diff)))
                notes.append('s')
            # if(np.sum(yellow_diff)>0):
            #     notes.append('d')
            # if(np.sum(blue_diff)>0):
            #     notes.append('f')
            if(np.sum(green_diff)>280 or np.sum(red_diff)>200):
                #  or np.sum(yellow_diff)>0 or np.sum(blue_diff)>0
                
                # print('Green: '+str(np.sum(green_diff)))
                # print('Red: '+str(np.sum(red_diff)))
                # print('Yellow: ' +str(np.sum(yellow_diff)))
                if(currentTime() - last_time > 20):
                    last_time = currentTime()
                    # i+=1
                    # lolworkpls = np.sum(red_diff)
                    # cv2.imwrite('Strum{i}_{lolworkpls}.png'.format(i=i,lolworkpls=lolworkpls), img)
                    releaseAll()
                    strum(notes) 
            
def currentTime():
    return round(time.time() * 1000)

def strum(input):
    for x in input:
        key.press(str(x))
    key.tap(Key.down)     

def releaseAll():
    key.release('a')
    key.release('s')
    key.release('d')
    key.release('f')
    key.release('g')
    
main(True,False)

###########
                #       img[y1:y2, x1:x2]
                ###########
                # green_img_low = img[49:52, 47:50]
                # green_img_high = img[0:4, 66:69]
                
                # red_img_low = img[49:52, 180:183]
                # red_img_high = img[0:4, 190:193]
                
                # yellow_img_low = img[49:52, 307:310]
                # yellow_img_high = img[0:4, 308:311]
                
                # blueImg = img[0:5, 381:385]
                # orangeImg = img[0:5, 481:485]
                # ########### 
        # #       Coordinates go in this fashion for openCV.
        # #               img[y1:y2, x1:x2]
        # ###########
        # #47,49   50,52
        # green_background_low = img[49:52, 47:50]
        # #66,0 69,4
        # green_background_high = img[0:4, 66:69]
        # #180,49 183,52
        # red_background_low = img[49:52, 180:183]
        # #190,0 193,4
        # red_background_high = img[0:4, 190:193]
        # #307,49 310,52
        # yellow_background_low = img[49:52, 307:310]
        # #308,0 311,4
        # yellow_background_high = img[0:4, 308:311]