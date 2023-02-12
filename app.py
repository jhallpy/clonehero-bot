import numpy as np
import time
import cv2
import dxcam
import threading
import uuid
import os
import template_match as match
from pynput.keyboard import Key, Controller, Listener, KeyCode
from matplotlib import pyplot as plt

camera = dxcam.create()
key_press = Controller()
# capture_area = (595, 900, 1325, 985)
capture_area = (595, 925, 1325, 987)
start_stop_key = KeyCode(char='t')
stop_key = KeyCode(char='y')

STRUM_TIME = 3

class PlayRedux(threading.Thread):
    def __init__(self):
        super(PlayRedux, self).__init__()
        self.background_img = cv2.imread('background.png')
        self.running = False
        self.program_running = True
        self.capture_area = capture_area
        self.images = []
        
        self.green_time = []
        self.red_time = []
        self.yellow_time = []
        self.blue_time = []
        self.orange_time = []
        self.purple_time = []
        
    def start_playing(self):
        self.running = True
        
    def stop_playing(self):
        self.running = False
     
    def exit(self):
        self.stop_playing()
        self.program_running = False
                
    def capture(self):
        self.img_check = camera.grab(self.capture_area)
  
    def set_times(self):
        self.green_strum = current_time()
        self.red_strum = current_time()
        self.yellow_strum = current_time()
        self.blue_strum = current_time()
        self.orange_strum = current_time()
        self.purple_strum = current_time()
       
    def save_image(self):
        self.images.append({"image": self.img_check, "notes": self.notes}) 
        
    def strum(self):
        self.release_all()
        for x in self.notes:
            if (str(x) == 'p'):
                continue
            else:
                key_press.press(str(x))
        key_press.tap(Key.down)
        
    def release_all(self):
        key_press.release('a')
        key_press.release('s')
        key_press.release('d')
        key_press.release('f')
        key_press.release('g')  
        
    def run(self):
        self.capture()
        self.set_times()
        while self.program_running:
            while self.running:
                self.capture()
                self.notes = []
                self.played = False
                start = current_time()
                # NOTE: dxcam will return None if the image it takes would be the exact same image as the previous image. Therefore, this check is necessary.
                if (self.img_check is None):
                    continue
                else:
                    self.template_match = match.match_all(self.img_check)
                    # print(self.test)
                    # self.save_image()
                    if self.template_match:
                        if 'a' in self.template_match and current_time() - self.green_strum > STRUM_TIME:
                            self.green_time.append(current_time() - self.green_strum)
                            self.green_strum = current_time()
                            self.notes.append('a')
                            self.save_image()
                        if 's' in self.template_match and current_time() - self.red_strum > STRUM_TIME:
                            self.red_time.append(current_time() - self.red_strum)
                            self.red_strum = current_time()
                            self.notes.append('s')
                            # self.save_image()
                        if 'd' in self.template_match and current_time() - self.yellow_strum > STRUM_TIME:
                            self.yellow_time.append(current_time() - self.yellow_strum)
                            self.yellow_strum = current_time()
                            self.notes.append('d')
                            # self.save_image()
                        if 'f' in self.template_match and current_time() - self.blue_strum > STRUM_TIME:
                            self.blue_time.append(current_time() - self.blue_strum)
                            self.blue_strum = current_time()
                            self.notes.append('f')
                            # self.save_image()
                        if 'g' in self.template_match and current_time() - self.orange_strum > STRUM_TIME:
                            self.orange_time.append(current_time() - self.orange_strum)
                            self.orange_strum = current_time()
                            self.notes.append('g')
                        # self.save_image()
                        # print(self.notes) 
                        if self.notes:
                        #     # print('strum')
                        #     # self.save_image()
                            self.strum()
                        
                # try:
                #     print('FPS:', 1000 / (current_time() - start))
                # except ZeroDivisionError:
                #     print('FPS:', 1000)
                        
            time.sleep(0.01) 

play_thread = PlayRedux()
play_thread.start()   
    
def current_time():
    return int(round(time.time() * 1000))
  
def on_press(key):
    if key == start_stop_key:
        if play_thread.running:
            play_thread.release_all()
            play_thread.stop_playing()
            y=1
            
            try:
                if (len(play_thread.green_time) > 0):
                    play_thread.green_time.sort()
                    print(str(play_thread.green_time[0]) + '\t Green Time')
                if (len(play_thread.red_time) > 0):
                    play_thread.red_time.sort()
                    print(str(play_thread.red_time[0]) + '\t Red Time')
                if (len(play_thread.yellow_time) > 0):
                    play_thread.yellow_time.sort()
                    print(str(play_thread.yellow_time[0]) + '\t Yellow Time')
                if (len(play_thread.blue_time) > 0):
                    play_thread.blue_time.sort()
                    print(str(play_thread.blue_time[0]) + '\t Blue Time')
                if (len(play_thread.orange_time) > 0):
                    play_thread.orange_time.sort()
                    print(str(play_thread.orange_time[0]) + '\t Orange Time')
                if (len(play_thread.purple_time) > 0):
                    play_thread.purple_time.sort()
                    print(str(play_thread.purple_time[0]) + '\t Purple Time')
            except:
                print('Error')

            IMAGES_PATH = os.path.join('data', 'images')
            
            # NOTE: Only useful for saving images for debugging purposes. 
            for img_num in play_thread.images:
                
                imgname = os.path.join(IMAGES_PATH, str(y) + str(img_num["notes"]) +'.png')
                corrected_colors = cv2.cvtColor(img_num['image'], cv2.COLOR_BGR2GRAY)
                cv2.imwrite(imgname, corrected_colors)
                y+=1   

            play_thread.images = []
            print('Bot Stopped.')
        else:
            print('Bot Running...')
            # play_thread.set_background()
            play_thread.release_all()
            play_thread.start_playing()
    elif key == stop_key:
        play_thread.release_all()
        play_thread.exit()
        print('Exiting...')
        listener.stop()
        
with Listener(on_press=on_press) as listener: 
    listener.join()

# def main():
    
# NOTE: Should work but doesn't. Will look for fix when I finish the program.
# if __name__ == "main":
#     main()