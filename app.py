from cv2 import COLOR_RGB2BGR
import numpy as np
import time
from pynput.keyboard import Key, Controller, Listener, KeyCode
import cv2
import dxcam
import threading
from PIL import ImageGrab

camera = dxcam.create()
key_press = Controller()
capture_area = (650,850,1325,970)
start_stop_key = KeyCode(char='t')
stop_key = KeyCode(char='y')
screenshot_key = KeyCode(char='r')
screenshot = 0

class PlayRedux(threading.Thread):
    def __init__(self):
        super(PlayRedux, self).__init__()
        self.running = False
        self.program_running = True
        self.capture_area = capture_area
        self.screenshot = screenshot
        self.images = []
        self.test_images = []
        
    def start_playing(self):
        self.running = True
        
    def stop_playing(self):
        self.running = False
     
    def exit(self):
        self.stop_playing()
        self.program_running = False
                
    def capture(self):
        self.img_check = camera.grab(self.capture_area)
        
    def save_image(self):
        # TODO: Save with OpenCV instead of the actual image capture. It will work instead of maybe working.
        self.capture()
        cv2.imwrite('screenshot_img_{}.png'.format(screenshot), np.array(ImageGrab.grab(bbox=capture_area)))
        self.screenshot += 1
        
    def set_area(self):
        # dxcam will return None if the image it takes would be the exact same image as the previous image. Therefore, this check is necessary.
        if (self.img_check is not None):
            self.gn_chk = self.img_check[74:78, 84:88]
            self.gn_chk_two = self.img_check[60:64, 84:88]
            self.gn_chk_three = self.img_check[50:54, 66:70]
            self.gn_chk_four = self.img_check[40:43, 50:53]
            
            self.r_chk = self.img_check[74:78, 220:224]
            self.r_chk_two = self.img_check[60:64, 220:224]
            self.r_chk_three = self.img_check[50:54, 210:214]
            self.r_chk_four = self.img_check[40:43, 182:185]
            
            self.ye_chk = self.img_check[74:78, 355:359]
            self.ye_chk_two = self.img_check[60:64, 355:359]
            self.ye_chk_three = self.img_check[50:54, 352:356]
            self.ye_chk_four = self.img_check[40:43, 308:311]
            
            self.bl_chk = self.img_check[74:78, 485:489]
            self.bl_chk_two = self.img_check[60:64, 485:489]
            self.bl_chk_three = self.img_check[50:54, 480:484]
            self.bl_chk_four = self.img_check[40:43, 433:436]
            
            self.or_chk = self.img_check[74:78, 538:542]
            self.or_chk_two = self.img_check[60:64, 538:542]
            self.or_chk_three = self.img_check[50:54, 553:557]
            self.or_chk_four = self.img_check[40:43, 565:568]
            
    def set_background(self):
        self.capture()
        self.gn_bg = self.img_check[74:78,84:88]
        self.gn_bg_two = self.img_check[60:64, 84:88]
        self.gn_bg_three = self.img_check[50:54, 66:70]
        self.gn_bg_four = self.img_check[40:43, 50:53]
        
        self.r_bg = self.img_check[74:78, 220:224]
        self.r_bg_two = self.img_check[60:64, 220:224]
        self.r_bg_three = self.img_check[50:54, 210:214]
        self.r_bg_four = self.img_check[40:43, 182:185]
        
        self.ye_bg = self.img_check[74:78, 355:359]
        self.ye_bg_two = self.img_check[60:64, 355:359]
        self.ye_bg_three = self.img_check[50:54, 352:356]
        self.ye_bg_four = self.img_check[40:43, 308:311]
        
        self.bl_bg = self.img_check[74:78, 485:489]
        self.bl_bg_two = self.img_check[60:64, 485:489]
        self.bl_bg_three = self.img_check[50:54, 480:484]
        self.bl_bg_four = self.img_check[40:43, 433:436]
        
        self.or_bg = self.img_check[74:78, 538:542]
        self.or_bg_two = self.img_check[60:64, 538:542]
        self.or_bg_three = self.img_check[50:54, 553:557]
        self.or_bg_four = self.img_check[40:43, 565:568]
        
        cv2.imwrite('background.png', cv2.cvtColor(self.img_check, cv2.COLOR_RGB2BGR))
        
        
    def set_times(self):
        self.green_strum = current_time()
        self.red_strum = current_time()
        self.yellow_strum = current_time()
        self.blue_strum = current_time()
        self.orange_strum = current_time()
    
    def background_subtraction(self):
        self.gn_df = cv2.subtract(np.asarray(self.gn_chk), np.asarray(self.gn_bg)) + cv2.subtract(np.asarray(self.gn_bg), np.asarray(self.gn_chk))
        self.gn_df_two = cv2.subtract(np.asarray(self.gn_chk_two), np.asarray(self.gn_bg_two)) + cv2.subtract(np.asarray(self.gn_bg_two), np.asarray(self.gn_chk_two))
        self.gn_df_three = cv2.subtract(np.asarray(self.gn_chk_three), np.asarray(self.gn_bg_three)) + cv2.subtract(np.asarray(self.gn_bg_three), np.asarray(self.gn_chk_three))
        self.gn_df_four = cv2.subtract(np.asarray(self.gn_chk_four), np.asarray(self.gn_bg_four)) + cv2.subtract(np.asarray(self.gn_bg_four), np.asarray(self.gn_chk_four))
        
        self.r_df = cv2.subtract(np.asarray(self.r_chk), np.asarray(self.r_bg)) + cv2.subtract(np.asarray(self.r_bg), np.asarray(self.r_chk))
        self.r_df_two = cv2.subtract(np.asarray(self.r_chk_two), np.asarray(self.r_bg_two)) + cv2.subtract(np.asarray(self.r_bg_two), np.asarray(self.r_chk_two))
        self.r_df_three = cv2.subtract(np.asarray(self.r_chk_three), np.asarray(self.r_bg_three)) + cv2.subtract(np.asarray(self.r_bg_three), np.asarray(self.r_chk_three))
        self.r_df_four = cv2.subtract(np.asarray(self.r_chk_four), np.asarray(self.r_bg_four)) + cv2.subtract(np.asarray(self.r_bg_four), np.asarray(self.r_chk_four))
        
        self.ye_df = cv2.subtract(np.asarray(self.ye_chk), np.asarray(self.ye_bg)) + cv2.subtract(np.asarray(self.ye_bg), np.asarray(self.ye_chk))
        self.ye_df_two = cv2.subtract(np.asarray(self.ye_chk_two), np.asarray(self.ye_bg_two)) + cv2.subtract(np.asarray(self.ye_bg_two), np.asarray(self.ye_chk_two))
        self.ye_df_three = cv2.subtract(np.asarray(self.ye_chk_three), np.asarray(self.ye_bg_three)) + cv2.subtract(np.asarray(self.ye_bg_three), np.asarray(self.ye_chk_three))
        self.ye_df_four = cv2.subtract(np.asarray(self.ye_chk_four), np.asarray(self.ye_bg_four)) + cv2.subtract(np.asarray(self.ye_bg_four), np.asarray(self.ye_chk_four))
        
        self.bl_df = cv2.subtract(np.asarray(self.bl_chk), np.asarray(self.bl_bg)) + cv2.subtract(np.asarray(self.bl_bg), np.asarray(self.bl_chk))
        self.bl_df_two = cv2.subtract(np.asarray(self.bl_chk_two), np.asarray(self.bl_bg_two)) + cv2.subtract(np.asarray(self.bl_bg_two), np.asarray(self.bl_chk_two))
        self.bl_df_three = cv2.subtract(np.asarray(self.bl_chk_three), np.asarray(self.bl_bg_three)) + cv2.subtract(np.asarray(self.bl_bg_three), np.asarray(self.bl_chk_three))
        self.bl_df_four = cv2.subtract(np.asarray(self.bl_chk_four), np.asarray(self.bl_bg_four)) + cv2.subtract(np.asarray(self.bl_bg_four), np.asarray(self.bl_chk_four))
        
        self.or_df = cv2.subtract(np.asarray(self.or_chk), np.asarray(self.or_bg)) + cv2.subtract(np.asarray(self.or_bg), np.asarray(self.or_chk))
        self.or_df_two = cv2.subtract(np.asarray(self.or_chk_two), np.asarray(self.or_bg_two)) + cv2.subtract(np.asarray(self.or_bg_two), np.asarray(self.or_chk_two))
        self.or_df_three = cv2.subtract(np.asarray(self.or_chk_three), np.asarray(self.or_bg_three)) + cv2.subtract(np.asarray(self.or_bg_three), np.asarray(self.or_chk_three))
        self.or_df_four = cv2.subtract(np.asarray(self.or_chk_four), np.asarray(self.or_bg_four)) + cv2.subtract(np.asarray(self.or_bg_four), np.asarray(self.or_chk_four))
        
    def save_image(self):
        self.images.append({"image": self.img_check, "green": self.gn_df, "red": self.r_df, "yellow": self.ye_df, "blue": self.bl_df, "orange": self.or_df})
    
    def save_test_image(self):
      self.test_images.append({"image": self.img_check, "green": self.gn_df, "second_green": self.gn_df_two, "third_green": self.gn_df_three, "fourth_green": self.gn_df_four,
                               "red": self.r_df, "second_red": self.r_df_two, "third_red": self.r_df_three, "fourth_red": self.r_df_four,
                               "yellow": self.ye_df, "second_yellow": self.ye_df_two, "third_yellow": self.ye_df_three, "fourth_yellow": self.ye_df_four,
                               "blue": self.bl_df, "second_blue": self.bl_df_two, "third_blue": self.bl_df_three, "fourth_blue": self.bl_df_four,
                               "orange": self.or_df, "second_orange": self.or_df_two, "third_orange": self.or_df_three, "fourth_orange": self.or_df_four,
                               "played" : self.played, "notes": self.notes
                               })
      
    def strum(self):
        for x in self.notes:
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
        self.set_area()
        self.set_times()
        self.orange = []
        while self.program_running:
            while self.running:
                self.capture()
                self.notes = []
                self.played = False
                # dxcam will return None if the image it takes would be the exact same image as the previous image. Therefore, this check is necessary.
                if (self.img_check is None):
                    continue
                else:
                    self.set_area()
                    self.background_subtraction()
                    
                    # if(np.sum(self.gn_df_four) > 1200 and np.sum(self.gn_df_four) != 1910 and current_time() - self.red_strum >25):
                    #     print(np.sum(self.gn_df_four))
                    #     # self.save_test_image()
                    # if(np.sum(self.or_df_four) > 0 ):
                    #     print(np.sum(self.or_df_four))
                    if(np.sum(self.gn_df) > 20 and np.sum(self.gn_df_two) > 100 and np.sum(self.gn_df_three) > 20 
                       and np.sum(self.gn_df_four) != 1910 and np.sum(self.gn_df_four) > 1000
                       and current_time() - self.green_strum > 38):  
                        print(str(current_time() - self.green_strum) + " green strum.")
                        self.green_strum = current_time()
                        self.notes.append('a')
                        
                        if(np.sum(self.r_df_two) > 150 and np.sum(self.r_df_three) > 10 and np.sum(self.r_df_four) > 0 
                           and np.sum(self.r_df_four) != 1955 and np.sum(self.r_df_four) != 2051 and current_time() - self.red_strum > 38):
                            self.red_strum = current_time()
                            self.notes.append('s')
                            
                        if(np.sum(self.ye_df_two) > 100 and np.sum(self.ye_df_three) > 10 and np.sum(self.ye_df_four) != 3239 
                           and np.sum(self.ye_df_four) > 0 and np.sum(self.ye_df_four) != 1570 and current_time() - self.yellow_strum > 38):
                            self.yellow_strum = current_time()
                            self.notes.append('d')
                            
                        if(np.sum(self.bl_df_two) > 100 and np.sum(self.bl_df_three) > 10 and np.sum(self.bl_df_four) != 3318
                         and np.sum(self.bl_df_four) > 0 and current_time() - self.blue_strum > 38):
                            self.blue_strum = current_time()
                            self.notes.append('f')
                            
                        if(np.sum(self.or_df_two) > 100 and np.sum(self.or_df_three) > 10 
                           and np.sum(self.or_df_four) > 700 and np.sum(self.or_df_four) != 3456 and current_time() - self.orange_strum > 38):
                            self.orange_strum = current_time()
                            self.notes.append('g')
                    
                    elif(np.sum(self.r_df) > 20 and np.sum(self.r_df_two) > 150 and np.sum(self.r_df_three) > 10 
                       and np.sum(self.r_df_four) > 1000 and np.sum(self.r_df_four) != 1955 and np.sum(self.r_df_four) != 2051
                       and current_time() - self.red_strum > 38):
                        print(str(current_time() - self.red_strum) + " red strum.")
                        self.red_strum = current_time()
                        self.notes.append('s')
                        
                        if(np.sum(self.gn_df_two) > 100 and np.sum(self.gn_df_three) > 20 and np.sum(self.gn_df_four) != 1910 
                           and np.sum(self.gn_df_four) > 0 and current_time() - self.green_strum > 38): 
                            self.green_strum = current_time()
                            self.notes.append('a')
                            
                        if(np.sum(self.ye_df_two) > 100 and np.sum(self.ye_df_three) > 10 and np.sum(self.ye_df_four) != 3239 
                           and np.sum(self.ye_df_four) > 0 and np.sum(self.ye_df_four) != 1570 and current_time() - self.yellow_strum > 38):
                            self.yellow_strum = current_time()
                            self.notes.append('d')
                            
                        if(np.sum(self.bl_df_two) > 100 and np.sum(self.bl_df_three) > 10 and np.sum(self.bl_df_four) != 3324
                         and np.sum(self.bl_df_four) > 0 and current_time() - self.blue_strum > 38):
                            self.blue_strum = current_time()
                            self.notes.append('f')
                            
                        if(np.sum(self.or_df_two) > 100 and np.sum(self.or_df_three) > 10 
                           and np.sum(self.or_df_four) > 700 and np.sum(self.or_df_four) != 3456 and current_time() - self.orange_strum > 38):
                            self.orange_strum = current_time()
                            self.notes.append('g')
                    
                    elif(np.sum(self.ye_df) > 30 and np.sum(self.ye_df_two) > 100 and np.sum(self.ye_df_three) > 10 and np.sum(self.ye_df_four) != 3239 
                       and np.sum(self.ye_df_four) > 1000 and np.sum(self.ye_df_four) != 1570
                       and current_time() - self.yellow_strum > 38):
                        self.played = True
                        self.yellow_strum = current_time()
                        self.notes.append('d')
                        
                        if(np.sum(self.gn_df_two) > 100 and np.sum(self.gn_df_three) > 20 and np.sum(self.gn_df_four) != 1910 
                           and np.sum(self.gn_df_four) > 0 and current_time() - self.green_strum > 38): 
                            self.green_strum = current_time()
                            self.notes.append('a')
                            
                        if(np.sum(self.r_df_two) > 150 and np.sum(self.r_df_three) > 10 and np.sum(self.r_df_four) > 0 
                           and np.sum(self.r_df_four) != 1955 and np.sum(self.r_df_four) != 2051 and current_time() - self.red_strum > 38):
                            self.red_strum = current_time()
                            self.notes.append('s')
                            
                        if(np.sum(self.bl_df_two) > 100 and np.sum(self.bl_df_three) > 10 and np.sum(self.bl_df_four) != 3324
                         and np.sum(self.bl_df_four) > 0 and current_time() - self.blue_strum > 38):
                            self.blue_strum = current_time()
                            self.notes.append('f')
                            
                        if(np.sum(self.or_df_two) > 100 and np.sum(self.or_df_three) > 10 
                           and np.sum(self.or_df_four) > 700 and np.sum(self.or_df_four) != 3456 and current_time() - self.orange_strum > 38):
                            self.orange_strum = current_time()
                            self.notes.append('g')
                        
                    elif(np.sum(self.bl_df) > 10 and np.sum(self.bl_df_two) > 100 and np.sum(self.bl_df_three) > 10 and np.sum(self.bl_df_four) != 3324
                         and np.sum(self.bl_df_four) > 1000 and current_time() - self.blue_strum > 38):
                        print(str(current_time() - self.blue_strum) + " blue strum.")
                        self.played = True
                        self.blue_strum = current_time()
                        self.notes.append('f')
                        if(np.sum(self.gn_df_two) > 100 and np.sum(self.gn_df_three) > 20 and np.sum(self.gn_df_four) != 1910 
                           and np.sum(self.gn_df_four) > 0 and current_time() - self.green_strum > 38): 
                            self.green_strum = current_time()
                            self.notes.append('a')
                            
                        if(np.sum(self.r_df_two) > 150 and np.sum(self.r_df_three) > 10 and np.sum(self.r_df_four) > 0 
                           and np.sum(self.r_df_four) != 1955 and np.sum(self.r_df_four) != 2051 and current_time() - self.red_strum > 38):
                            self.red_strum = current_time()
                            self.notes.append('s')
                            
                        if(np.sum(self.ye_df_two) > 100 and np.sum(self.ye_df_three) > 10 and np.sum(self.ye_df_four) != 3239 
                           and np.sum(self.ye_df_four) > 0 and np.sum(self.ye_df_four) != 1570 and current_time() - self.yellow_strum > 38):
                            self.yellow_strum = current_time()
                            self.notes.append('d')
                            
                        if(np.sum(self.or_df_two) > 100 and np.sum(self.or_df_three) > 10 
                           and np.sum(self.or_df_four) > 700 and np.sum(self.or_df_four) != 3456 and current_time() - self.orange_strum > 38):
                            self.orange_strum = current_time()
                            self.notes.append('g')
                        
                    elif(np.sum(self.or_df) > 20 and np.sum(self.or_df_two) > 100 and np.sum(self.or_df_three) > 10 
                         and np.sum(self.or_df_four) > 700 
                         and np.sum(self.or_df_four) != 3456
                         and current_time() - self.orange_strum > 38):
                        self.orange_strum = current_time()
                        self.notes.append('g')
                        self.orange.append(np.sum(self.or_df_four))
                        
                        if(np.sum(self.gn_df_two) > 100 and np.sum(self.gn_df_three) > 20 and np.sum(self.gn_df_four) != 1910 
                           and np.sum(self.gn_df_four) > 0 and current_time() - self.green_strum > 38): 
                            self.green_strum = current_time()
                            self.notes.append('a')
                            
                        if(np.sum(self.r_df_two) > 150 and np.sum(self.r_df_three) > 10 and np.sum(self.r_df_four) > 0 
                           and np.sum(self.r_df_four) != 1955 and np.sum(self.r_df_four) != 2051 and current_time() - self.red_strum > 38):
                            self.red_strum = current_time()
                            self.notes.append('s')
                            
                        if(np.sum(self.ye_df_two) > 100 and np.sum(self.ye_df_three) > 10 and np.sum(self.ye_df_four) != 3239 
                           and np.sum(self.ye_df_four) > 0 and np.sum(self.ye_df_four) != 1570 and current_time() - self.yellow_strum > 38):
                            self.yellow_strum = current_time()
                            self.notes.append('d')

                        if(np.sum(self.bl_df_two) > 100 and np.sum(self.bl_df_three) > 10 and np.sum(self.bl_df_four) != 3324
                         and np.sum(self.bl_df_four) > 0 and current_time() - self.blue_strum > 38):
                            self.blue_strum = current_time()
                            self.notes.append('f')
                    elif(np.sum(self.gn_df_four) > 0 or np.sum(self.r_df_four) > 0 or np.sum(self.ye_df_four) > 0 or np.sum(self.bl_df_four) > 0 or np.sum(self.or_df_four) > 0):
                        self.save_test_image()
                        
                    if (len(self.notes) > 0):
                        # print(self.notes)
                        # print(str(i)+ " STRUM LINE \n ___________________________")
                        # i+=1
                        
                        self.played = True
                        # self.save_test_image()
                        
                        self.release_all()
                        self.strum()
                        
                        
                        # print(current_time() - start)
                    # self.save_test_image()
            time.sleep(0.01) 

play_thread = PlayRedux()
play_thread.start()   
    
def current_time():
    return int(round(time.time() * 1000))
  
def on_press(key):
    if key == start_stop_key:
        if play_thread.running:
            if(len(play_thread.orange) > 0 ):
                print(str(max(play_thread.orange)) + " Max")
                print(str(min(play_thread.orange)) + " min")
            play_thread.release_all()
            play_thread.stop_playing()
        else:
            play_thread.set_background()
            play_thread.release_all()
            play_thread.start_playing()
    elif key == screenshot_key:
        play_thread.save_image()
    elif key == stop_key:
        cv2.imwrite('test_image.png', cv2.cvtColor(np.asarray(ImageGrab.grab(bbox=capture_area)), cv2.COLOR_RGB2BGR))
        y = 1
        with open('notes.txt', 'w') as f:
            for x in play_thread.test_images:
                cv2.rectangle(x['image'], (83, 73), (89,79), (255,0,0), 1)
                cv2.rectangle(x['image'], (83, 58), (89,64), (255,0,0), 1)
                cv2.rectangle(x['image'], (65,49), (71,55), (255,0,0), 1)
                cv2.rectangle(x['image'], (49,39), (54,44), (255,0,0), 1)
                
                cv2.rectangle(x['image'], (219, 73), (225,79), (0,255,0), 1)
                cv2.rectangle(x['image'], (219, 58), (225,64), (0,255,0), 1)
                cv2.rectangle(x['image'], (209,49), (215,55), (0,255,0), 1)
                cv2.rectangle(x['image'], (181,39), (186,44), (0,255,0), 1)
                
                cv2.rectangle(x['image'], (354, 73), (359,79), (255,0,0), 1)
                cv2.rectangle(x['image'], (354, 58), (359,64), (255,0,0), 1)
                cv2.rectangle(x['image'], (351,49), (357,55), (255,0,0), 1)
                cv2.rectangle(x['image'], (307,39), (312,44), (255,0,0), 1)
                
                cv2.rectangle(x['image'], (484, 73), (490,79), (255,0,0), 1)
                cv2.rectangle(x['image'], (484, 58), (490,64), (255,0,0), 1)
                cv2.rectangle(x['image'], (479, 49), (485,55), (255,0,0), 1)
                cv2.rectangle(x['image'], (432,39), (437,44), (255,0,0), 1)
                
                cv2.rectangle(x['image'], (537, 73), (543,79), (255,0,0), 1)
                cv2.rectangle(x['image'], (537, 58), (543,64), (255,0,0), 1)
                cv2.rectangle(x['image'], (552, 49), (558,55), (255,0,0), 1)
                cv2.rectangle(x['image'], (564,39), (569,44), (255,0,0), 1)
                if(x['played']):
                    f.write('\n Img {} {} {} \n Green o{} tw{} th{} f{} \n Red o{} tw{} th{} f{} \n Yellow o{} tw{} th{} f{} \n Blue o{} tw{} th{} f{} \n Orange o{} tw{} th{} f{} \n'.format(
                        y, x['played'], ''.join(str(z) for z in x['notes']),
                        np.sum(x['green']),np.sum(x['second_green']),np.sum(x['third_green']), np.sum(x['fourth_green']),
                        np.sum(x['red']),np.sum(x['second_red']),np.sum(x['third_red']), np.sum(x['fourth_red']),
                        np.sum(x['yellow']),np.sum(x['second_yellow']),np.sum(x['third_yellow']), np.sum(x['fourth_yellow']),
                        np.sum(x['blue']),np.sum(x['second_blue']),np.sum(x['third_blue']), np.sum(x['fourth_blue']),
                        np.sum(x['orange']),np.sum(x['second_orange']),np.sum(x['third_orange']), np.sum(x['fourth_orange']),
                    ))
                else:
                    f.write('\n Img {} {}  \n Green o{} tw{} th{} f{} \n Red o{} tw{} th{} f{} \n Yellow o{} tw{} th{} f{} \n Blue o{} tw{} th{} f{} \n Orange o{} tw{} th{} f{} \n'.format(
                        y, x['played'],
                        np.sum(x['green']),np.sum(x['second_green']),np.sum(x['third_green']), np.sum(x['fourth_green']),
                        np.sum(x['red']),np.sum(x['second_red']),np.sum(x['third_red']), np.sum(x['fourth_red']),
                        np.sum(x['yellow']),np.sum(x['second_yellow']),np.sum(x['third_yellow']), np.sum(x['fourth_yellow']),
                        np.sum(x['blue']),np.sum(x['second_blue']),np.sum(x['third_blue']), np.sum(x['fourth_blue']),
                        np.sum(x['orange']),np.sum(x['second_orange']),np.sum(x['third_orange']), np.sum(x['fourth_orange']),
                    ))
                cv2.imwrite('img_{}_{}.png'.format(y, x['played']), cv2.cvtColor(x['image'], cv2.COLOR_RGB2BGR))
                y+=1
        play_thread.release_all()
        play_thread.exit()
        listener.stop()
        
with Listener(on_press=on_press) as listener: 
    listener.join()
 
# def main():
    
    
# if __name__ == "main":
#     main()