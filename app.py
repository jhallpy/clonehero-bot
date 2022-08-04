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
            self.green_check = self.img_check[74:78, 74:78]
            self.green_check_two = self.img_check[60:64, 74:78]
            self.green_check_three = self.img_check[50:54, 66:70]
            self.green_check_four = self.img_check[40:43, 50:53]
            
            self.red_check = self.img_check[74:78, 220:224]
            self.red_check_two = self.img_check[60:64, 220:224]
            self.red_check_three = self.img_check[50:54, 210:214]
            self.red_check_four = self.img_check
            
            self.yellow_check = self.img_check[74:78, 355:359]
            self.yellow_check_two = self.img_check[60:64, 355:359]
            self.yellow_check_three = self.img_check[50:54, 352:356]
            self.yelow_four = self.img_check[40:43, 308:311]
            
            self.blue_check = self.img_check[74:78, 500:504]
            self.blue_check_two = self.img_check[60:64, 500:504]
            self.blue_check_three = self.img_check[50:54, 450:454]
            self.blue_check_four = self.img_check
            
            self.orange_check = self.img_check[74:78, 538:542]
            self.orange_check_two = self.img_check[60:64, 538:542]
            self.orange_check_three = self.img_check[50:54, 553:557]
            
    def set_background(self):
        self.capture()
        self.green_bg = self.img_check[74:78, 74:78]
        self.green_bg_two = self.img_check[60:64, 74:78]
        self.green_bg_three = self.img_check[50:54, 66:70]
            
        self.red_bg = self.img_check[74:78, 220:224]
        self.red_bg_two = self.img_check[60:64, 220:224]
        self.red_bg_three = self.img_check[50:54, 210:214]
        
        self.yellow_bg = self.img_check[74:78, 355:359]
        self.yellow_bg_two = self.img_check[60:64, 355:359]
        self.yellow_bg_three = self.img_check[50:54, 352:356]
        
        self.blue_bg = self.img_check[74:78, 500:504]
        self.blue_bg_two = self.img_check[60:64, 500:504]
        self.blue_bg_three = self.img_check[50:54, 450:454]
        
        self.orange_bg = self.img_check[74:78, 538:542]
        self.orange_bg_two = self.img_check[60:64, 538:542]
        self.orange_bg_three = self.img_check[50:54, 553:557]
        
        cv2.imwrite('background.png', cv2.cvtColor(self.img_check, cv2.COLOR_RGB2BGR))
        
        
    def set_times(self):
        self.green_strum = current_time()
        self.red_strum = current_time()
        self.yellow_strum = current_time()
        self.blue_strum = current_time()
        self.orange_strum = current_time()
    
    def background_subtraction(self):
        self.green_diff = cv2.subtract(np.asarray(self.green_check), np.asarray(self.green_bg)) + cv2.subtract(np.asarray(self.green_bg), np.asarray(self.green_check))
        self.green_diff_two = cv2.subtract(np.asarray(self.green_check_two), np.asarray(self.green_bg_two)) + cv2.subtract(np.asarray(self.green_bg_two), np.asarray(self.green_check_two))
        self.green_diff_three = cv2.subtract(np.asarray(self.green_check_three), np.asarray(self.green_bg_three)) + cv2.subtract(np.asarray(self.green_bg_three), np.asarray(self.green_check_three))
        
        self.red_diff = cv2.subtract(np.asarray(self.red_check), np.asarray(self.red_bg)) + cv2.subtract(np.asarray(self.red_bg), np.asarray(self.red_check))
        self.red_diff_two = cv2.subtract(np.asarray(self.red_check_two), np.asarray(self.red_bg_two)) + cv2.subtract(np.asarray(self.red_bg_two), np.asarray(self.red_check_two))
        self.red_diff_three = cv2.subtract(np.asarray(self.red_check_three), np.asarray(self.red_bg_three)) + cv2.subtract(np.asarray(self.red_bg_three), np.asarray(self.red_check_three))
        
        self.yellow_diff = cv2.subtract(np.asarray(self.yellow_check), np.asarray(self.yellow_bg)) + cv2.subtract(np.asarray(self.yellow_bg), np.asarray(self.yellow_check))
        self.yellow_diff_two = cv2.subtract(np.asarray(self.yellow_check_two), np.asarray(self.yellow_bg_two)) + cv2.subtract(np.asarray(self.yellow_bg_two), np.asarray(self.yellow_check_two))
        self.yellow_diff_three = cv2.subtract(np.asarray(self.yellow_check_three), np.asarray(self.yellow_bg_three)) + cv2.subtract(np.asarray(self.yellow_bg_three), np.asarray(self.yellow_check_three))
        
        self.blue_diff = cv2.subtract(np.asarray(self.blue_check), np.asarray(self.blue_bg)) + cv2.subtract(np.asarray(self.blue_bg), np.asarray(self.blue_check))
        self.blue_diff_two = cv2.subtract(np.asarray(self.blue_check_two), np.asarray(self.blue_bg_two)) + cv2.subtract(np.asarray(self.blue_bg_two), np.asarray(self.blue_check_two))
        self.blue_diff_three = cv2.subtract(np.asarray(self.blue_check_three), np.asarray(self.blue_bg_three)) + cv2.subtract(np.asarray(self.blue_bg_three), np.asarray(self.blue_check_three))
        
        self.orange_diff = cv2.subtract(np.asarray(self.orange_check), np.asarray(self.orange_bg)) + cv2.subtract(np.asarray(self.orange_bg), np.asarray(self.orange_check))
        self.orange_diff_two = cv2.subtract(np.asarray(self.orange_check_two), np.asarray(self.orange_bg_two)) + cv2.subtract(np.asarray(self.orange_bg_two), np.asarray(self.orange_check_two))
        self.orange_diff_three = cv2.subtract(np.asarray(self.orange_check_three), np.asarray(self.orange_bg_three)) + cv2.subtract(np.asarray(self.orange_bg_three), np.asarray(self.orange_check_three))
        
    def save_image(self):
        self.images.append({"image": self.img_check, "green": self.green_diff, "red": self.red_diff, "yellow": self.yellow_diff, "blue": self.blue_diff, "orange": self.orange_diff})
    
    def save_test_image(self):
      self.test_images.append({"image": self.img_check, "green": self.green_diff, "second_green": self.green_diff_two, "third_green": self.green_diff_three,
                               "red": self.red_diff, "second_red": self.red_diff_two, "third_red": self.red_diff_three,
                               "yellow": self.yellow_diff, "second_yellow": self.yellow_diff_two, "third_yellow": self.yellow_diff_three,
                               "blue": self.blue_diff, "second_blue": self.blue_diff_two, "third_blue": self.blue_diff_three,
                               "orange": self.orange_diff, "second_orange": self.orange_diff_two, "third_orange": self.orange_diff_three
                               })
      
    def strum(self):
        # start = time.time()
        for x in self.notes:
            key_press.press(str(x))
        key_press.tap(Key.down)
        # print(time.time() - start)
        
    def release_all(self):
        key_press.release('a')
        key_press.release('s')
        key_press.release('d')
        key_press.release('f')
        key_press.release('g')  

    def run(self):
        i = 1
        self.capture()
        self.set_area()
        self.set_times()
        while self.program_running:
            while self.running:
                self.capture()
                self.notes = []
                # dxcam will return None if the image it takes would be the exact same image as the previous image. Therefore, this check is necessary.
                if (self.img_check is None):
                    continue
                else:
                    self.set_area()
                    self.background_subtraction()
                    if(np.sum(self.green_diff) > 750 and np.sum(self.green_diff_two) > 750 and np.sum(self.green_diff_three) > 200 and current_time() - self.green_strum > 25):   
                        self.green_strum = current_time()
                        self.notes.append('a')
                        if(np.sum(self.red_diff) > 200 and np.sum(self.red_diff_two) > 200 and np.sum(self.red_diff_three) > 200 and current_time() - self.red_strum >25):
                            # print(str(np.sum(self.red_diff_two)) +" secondary red")
                            self.red_strum = current_time()
                            self.notes.append('s')
                        if(np.sum(self.yellow_diff) > 100 and np.sum(self.yellow_diff_two) > 100 and np.sum(self.yellow_diff_three) > 150 and current_time() - self.yellow_strum >25):
                            # print(str(np.sum(self.yellow_diff_two)) +" secondary yellow")
                            self.yellow_strum = current_time()
                            self.notes.append('d')
                        if(np.sum(self.blue_diff_two) > 150 and np.sum(self.blue_diff_three) > 150 and current_time() - self.blue_strum >25):
                            # print(str(np.sum(self.blue_diff_two)) +" secondary blue")
                            self.blue_strum = current_time()
                            self.notes.append('f')
                        if(np.sum(self.orange_diff_two)>100):
                            # print(str(np.sum(self.orange_diff_two)) +" secondary orange")
                            self.orange_strum = current_time()
                            self.notes.append('g')
                        # print(np.sum(self.green_check))
                    elif(np.sum(self.red_diff) > 200 and np.sum(self.red_diff_two) > 200 and np.sum(self.red_diff_three) > 200 and current_time() - self.red_strum >25):
                        self.red_strum = current_time()
                        self.notes.append('s')
                        if(np.sum(self.green_diff) > 750 and np.sum(self.green_diff_two) > 750 and np.sum(self.green_diff_three) > 200 and current_time() - self.green_strum > 25):
                            # print(str(np.sum(self.green_diff_two)) +" secondary green")
                            self.green_strum = current_time()
                            self.notes.append('a')
                        if(np.sum(self.yellow_diff) > 100 and np.sum(self.yellow_diff_two) > 100 and np.sum(self.yellow_diff_three) > 150 and current_time() - self.yellow_strum >25):
                            # print(str(np.sum(self.yellow_diff_two)) +" secondary yellow")
                            self.yellow_strum = current_time()
                            self.notes.append('d')
                        if(np.sum(self.blue_diff_two) > 150 and np.sum(self.blue_diff_three) > 150 and current_time() - self.blue_strum >25):
                            # print(str(np.sum(self.blue_diff_two)) +" secondary blue")
                            self.blue_strum = current_time()
                            self.notes.append('f')
                        if(np.sum(self.orange_diff_two) > 100 and np.sum(self.orange_diff_three) > 100 ):
                            # print(str(np.sum(self.orange_diff_two)) +" secondary orange")
                            self.orange_strum = current_time()
                            self.notes.append('g')
                    elif(np.sum(self.yellow_diff) > 100 and np.sum(self.yellow_diff_two) > 100 and np.sum(self.yellow_diff_three) > 150 and current_time() - self.yellow_strum >25):
                        self.yellow_strum = current_time()
                        self.notes.append('d')
                        if(np.sum(self.green_diff) > 750 and np.sum(self.green_diff_two) > 750 and np.sum(self.green_diff_three) > 200 and current_time() - self.green_strum > 25):
                            # print(str(np.sum(self.green_diff_two)) +" secondary green")
                            self.green_strum = current_time()
                            self.notes.append('a')
                        if(np.sum(self.red_diff) > 200 and np.sum(self.red_diff_two) > 200 and np.sum(self.red_diff_three) > 200 and current_time() - self.red_strum >25):
                            # print(str(np.sum(self.red_diff_two)) +" secondary red")
                            self.red_strum = current_time()
                            self.notes.append('s')
                        if(np.sum(self.blue_diff_two) > 150 and np.sum(self.blue_diff_three) > 150 and current_time() - self.blue_strum >25):
                            # print(str(np.sum(self.blue_diff_two)) +" secondary blue")
                            self.blue_strum = current_time()
                            self.notes.append('f')
                        # if(np.sum(self.orange_diff_two)>100):
                        #     print(str(np.sum(self.orange_diff_two)) +" secondary orange")
                        #     self.orange_strum = current_time()
                        #     self.notes.append('g')
                    elif(np.sum(self.blue_diff) > 150 and np.sum(self.blue_diff_two) > 150 and np.sum(self.blue_diff_three) > 150 and current_time() - self.blue_strum >25):
                        # print(str(current_time() - self.blue_strum) +" blue strum")
                        self.blue_strum = current_time()
                        self.notes.append('f')
                        if(np.sum(self.green_diff) > 750 and np.sum(self.green_diff_two) > 750 and np.sum(self.green_diff_three) > 200 and current_time() - self.green_strum > 25):
                            # print(str(np.sum(self.green_diff_two)) +" secondary green")
                            self.green_strum = current_time()
                            self.notes.append('a')
                        if(np.sum(self.red_diff) > 200 and np.sum(self.red_diff_two) > 200 and np.sum(self.red_diff_three) > 200 and current_time() - self.red_strum >25):
                            # print(str(np.sum(self.red_diff_two)) +" secondary red")
                            self.red_strum = current_time()
                            self.notes.append('s')
                        if(np.sum(self.yellow_diff) > 100 and np.sum(self.yellow_diff_two) > 100 and np.sum(self.yellow_diff_three) > 150 and current_time() - self.yellow_strum >25):
                            # print(str(np.sum(self.yellow_diff_two)) +" secondary yellow")
                            self.yellow_strum = current_time()
                            self.notes.append('d')
                        # if(np.sum(self.orange_diff_two)>100):
                        #     print(str(np.sum(self.orange_diff_two)) +" secondary orange")
                        #     self.orange_strum = current_time()
                        #     self.notes.append('g')
                    # elif(np.sum(self.red_diff) > 200 and np.sum(self.red_diff_two) > 200 and np.sum(self.red_diff_three) > 200 and current_time() - self.red_strum >25):
                    #     # print(str(current_time() - self.red_strum) +" red strum")
                    #     print(np.sum(self.red_diff))
                    #     print(np.sum(self.red_diff_two))
                    #     print(np.sum(self.red_diff_three))
                    #     print('RED \n -------------------')
                    #     self.red_strum = current_time()
                    #     self.notes.append('s')
                    
                    #     # key_press.tap(Key.down)
                    #     # print(current_time() - start)   
                    # elif(np.sum(self.orange_diff) > 50 and np.sum(self.orange_diff_two) > 100 and current_time() - self.orange_strum > 25):
                    #     print(str(current_time() - self.orange_strum) + " orange strum")
                    #     self.orange_strum = current_time()
                    #     self.notes.append('g')
                    #     if(np.sum(self.green_diff_two)>100):
                    #         # print(str(np.sum(self.green_diff_two)) +" secondary green")
                    #         self.green_strum = current_time()
                    #         self.notes.append('a')
                    #     if(np.sum(self.red_diff_two)>100):
                    #         # print(str(np.sum(self.red_diff_two)) +" secondary red")
                    #         self.red_strum = current_time()
                    #         self.notes.append('s')
                    #     if(np.sum(self.yellow_diff_two)>100):
                    #         # print(str(np.sum(self.yellow_diff_two)) +" secondary yellow")
                    #         self.yellow_strum = current_time()
                    #         self.notes.append('d')
                    #     if(np.sum(self.blue_diff_two)>100):
                    #         # print(str(np.sum(self.blue_diff_two)) +" secondary blue")
                    #         self.blue_strum = current_time()
                    #         self.notes.append('f')
                    #     # print(current_time() - start)   
                    self.save_test_image()
                    if (len(self.notes) > 0):
                        # print(self.notes)
                        # print(str(i)+ " STRUM LINE \n ___________________________")
                        # i+=1
                        self.release_all()
                        self.strum()
                        # self.save_test_image()
                        # print(current_time() - start)
                    # self.save_image()
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
        else:
            play_thread.set_background()
            play_thread.release_all()
            play_thread.start_playing()
    elif key == screenshot_key:
        play_thread.save_image()
    elif key == stop_key:
        cv2.imwrite('test_image.png', cv2.cvtColor(np.asarray(ImageGrab.grab(bbox=capture_area)), cv2.COLOR_RGB2BGR))
        y = 1
        z = 1
        for x in play_thread.test_images:
            # self.green_check = self.img_check[74:78, 74:78]
            # self.green_check_two = self.img_check[60:64, 74:78]
            # self.green_check_three = self.img_check[56:59, 66:70]
            
            # self.red_check = self.img_check[74:78, 220:224]
            # self.red_check_two = self.img_check[60:64, 220:224]
            # self.red_check_three = self.img_check[56:59, 210:214]
            
            # self.yellow_bg = self.img_check[74:78, 355:359]
            # self.yellow_bg_two = self.img_check[60:64, 355:359]
            # self.yellow_bg_three = self.img_check[50:54, 324:328]
            
            # self.blue_check = self.img_check[74:78, 512:516]
            # self.blue_check_two = self.img_check[60:64, 512:516]
            # self.blue_check_three = self.img_check[56:59, 450:454]
            
            # self.orange_check = self.img_check[74:78, 538:542]
            # self.orange_check_two = self.img_check[60:64, 538:542]
            # self.orange_check_three = self.img_check[56:59, 553:557]
            cv2.rectangle(x['image'], (73, 73), (79,79), (255,0,0), 1)
            cv2.rectangle(x['image'], (73, 58), (79,64), (255,0,0), 1)
            cv2.rectangle(x['image'], (65,49), (71,55), (255,0,0), 1)
            
            cv2.rectangle(x['image'], (219, 73), (225,79), (255,0,0), 1)
            cv2.rectangle(x['image'], (219, 58), (225,64), (255,0,0), 1)
            cv2.rectangle(x['image'], (209,49), (215,55), (255,0,0), 1)
            
            cv2.rectangle(x['image'], (354, 73), (359,79), (255,0,0), 1)
            cv2.rectangle(x['image'], (354, 58), (359,64), (255,0,0), 1)
            cv2.rectangle(x['image'], (350,49), (356,55), (255,0,0), 1)
            
            cv2.rectangle(x['image'], (499, 73), (504,79), (255,0,0), 1)
            cv2.rectangle(x['image'], (499, 58), (504,64), (255,0,0), 1)
            cv2.rectangle(x['image'], (449, 49), (455,55), (255,0,0), 1)
            
            cv2.rectangle(x['image'], (537, 73), (543,79), (255,0,0), 1)
            cv2.rectangle(x['image'], (537, 58), (543,64), (255,0,0), 1)
            cv2.rectangle(x['image'], (552, 49), (558,55), (255,0,0), 1)
            
            cv2.imwrite('img_{}_g{}_gtw{}_gth{}_r{}_rtw{}_rth{}_y{}_ytw{}_yth{}_b{}_btw{}_bth{}_o{}_otw{}_oth{}.png'.format(z,
                np.sum(x['green']),np.sum(x['second_green']),np.sum(x['third_green']),
                np.sum(x['red']),np.sum(x['second_red']),np.sum(x['third_red']),
                np.sum(x['yellow']),np.sum(x['second_yellow']),np.sum(x['third_yellow']),
                np.sum(x['blue']),np.sum(x['second_blue']),np.sum(x['third_blue']),
                np.sum(x['orange']),np.sum(x['second_orange']),np.sum(x['third_orange']),
                ),
                        cv2.cvtColor(x['image'], cv2.COLOR_RGB2BGR))
            z+=1
        for x in play_thread.images:
            cv2.rectangle(x['image'], (76, 108), (82,114), (255,0,0), 1)
            cv2.rectangle(x['image'], (223, 108), (229,114), (0,255,0), 1)
            cv2.rectangle(x['image'], (369, 108), (375,114), (255,0,0), 1)
            cv2.rectangle(x['image'], (514, 108), (520,114), (255,0,0), 1)
            # cv2.rectangle(x, (76, 108), (82,114), (255,0,0), 1)
            cv2.imwrite('img_{}_g{}_r{}_y{}_b{}_o{}.png'.format(y,np.sum(x['green']),np.sum(x['red']),np.sum(x['yellow']),np.sum(x['blue']),np.sum(x['orange'])), cv2.cvtColor(x['image'], cv2.COLOR_RGB2BGR))
            y+=1
        play_thread.release_all()
        play_thread.exit()
        listener.stop()
        
with Listener(on_press=on_press) as listener: 
    listener.join()
 
# def main():
    
    
# if __name__ == "main":
#     main()