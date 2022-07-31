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
        img_bg = camera.grab(self.capture_area)
        self.green_bg = img_bg[109:113, 77:81]
        self.red_bg = img_bg[111:114, 224:227]
        self.yellow_bg = img_bg[109:112, 370:373]
        self.blue_bg = img_bg[115:118, 515:518]
        self.images = []
        
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
        # TODO: Update capture points inside the image. Could lead to better results.
        if (self.img_check is not None):
            self.green_check = self.img_check[109:113, 77:81]
            self.red_check = self.img_check[111:114, 224:227]
            self.yellow_check = self.img_check[109:112, 370:373]
            self.blue_check = self.img_check[115:118, 515:518]
            
    def set_background(self):
        self.capture()
        self.green_bg = self.img_check[109:113, 77:81]
        self.red_bg = self.img_check[111:114, 224:227]
        self.yellow_bg = self.img_check[109:112, 370:373]
        self.blue_bg = self.img_check[115:118, 515:518]
    
    def set_times(self):
        self.green_strum = current_time()
        self.red_strum = current_time()
        self.yellow_strum = current_time()
        self.blue_strum = current_time()
        self.orange_strum = current_time()
    
    def background_subtraction(self):
        self.green_diff = cv2.subtract(np.asarray(self.green_check), np.asarray(self.green_bg)) + cv2.subtract(np.asarray(self.green_bg), np.asarray(self.green_check))
        self.green_diff[abs(self.green_diff) < 20.0] = 0
        
        self.red_diff = cv2.subtract(np.asarray(self.red_check), np.asarray(self.red_bg)) + cv2.subtract(np.asarray(self.red_bg), np.asarray(self.red_check))
        self.red_diff[abs(self.red_diff) < 58.0] = 0
        
        self.yellow_diff = cv2.subtract(np.asarray(self.yellow_check), np.asarray(self.yellow_bg)) + cv2.subtract(np.asarray(self.yellow_bg), np.asarray(self.yellow_check))
        self.yellow_diff[abs(self.yellow_diff) < 21.0] = 0
        
        self.blue_diff = cv2.subtract(np.asarray(self.blue_check), np.asarray(self.blue_bg)) + cv2.subtract(np.asarray(self.blue_bg), np.asarray(self.blue_check))
        self.blue_diff[abs(self.blue_diff) < 20.0] = 0
    
    def save_background(self):
        # hasattr makes sure this function does not throw an exception on program exit, otherwise the thread stays open.
        if hasattr(self, 'green_diff'):
            print(str(np.sum(self.green_bg)) + " GREEN bg")
            print(str(np.sum(self.red_bg)) + " RED bg")
            print(str(np.sum(self.yellow_bg)) + " YELLOW bg")
            print(str(np.sum(self.blue_bg)) + " BLUE bg")
            # print(str(np.sum(self.green_bg)) + " GREEN bg")
    
    def save_image(self):
        self.images.append(self.img_check)
            
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
        i = 0
        self.capture()
        self.set_area()
        self.set_times()
        while self.program_running:
            while self.running:
                self.capture()
                self.notes = []
                if (self.img_check is None):
                    continue
                else:
                    start = current_time()
                    self.set_area()
                    self.background_subtraction()
                    # if (np.sum(self.green_diff)>0):
                    #     print(np.sum(self.green_diff))
                    if(np.sum(self.green_diff) > 200 and current_time() - self.green_strum > 25):
                        # print(str(np.sum(self.green_diff)) + " STRUM")
                        # print(str(current_time() - self.green_strum) +" STRUMMED TIME")
                        self.save_image()
                        self.green_strum = current_time()
                        self.notes.append('a')
                        print(current_time() - start)
                    if(np.sum(self.red_diff) > 500 and current_time() - self.red_strum > 25):
                        # print(str(current_time() - self.red_strum) +" STRUMMED TIME")
                        self.red_strum = current_time()
                        # print(str(np.sum(self.red_diff)) + " STRUM")
                        self.notes.append('s')
                        # print(current_time() - start)
                        
                    # if(np.sum(self.yellow_diff) > 0):
                    #     print(np.sum(self.yellow_diff))
                    #     key_press.press('d')
                    #     key_press.tap(Key.down)
                    #     key_press.release('d')
                    #     print(current_time() - start)
                    # print(current_time() - start)
                    
                    if (len(self.notes) > 0):
                        self.release_all()
                        self.strum()
            time.sleep(0.01) 
                # notes = []
                # if(np.sum(self.green_diff)<=250 and np.sum(self.red_diff)<=200):
                #     continue
                # if(np.sum(self.green_diff)>250):
                #     print('Green:   ' +str(np.sum(self.green_diff)))
                #     notes.append('a')
                # if(np.sum(self.red_diff)>200):
                #     print('Red:   ' +str(np.sum(self.red_diff)))
                #     notes.append('s')
                # # if(np.sum(yellow_diff)>0):
                # #     notes.append('d')
                # # if(np.sum(blue_diff)>0):
                # #     notes.append('f')
                # if(np.sum(self.green_diff)>280 or np.sum(self.red_diff)>200):
                #     #  or np.sum(yellow_diff)>0 or np.sum(blue_diff)>0
                    
                #     # print('Green: '+str(np.sum(self.green_diff)))
                #     # print('Red: '+str(np.sum(self.red_diff)))
                #     # print('Yellow: ' +str(np.sum(yellow_diff)))
                #     if(currentTime() - last_time > 20):
                #         last_time = currentTime()
                #         # i+=1
                #         # lolworkpls = np.sum(self.red_diff)
                #         # cv2.imwrite('Strum{i}_{lolworkpls}.png'.format(i=i,lolworkpls=lolworkpls), img)
                #         releaseAll()
                #         strum(notes)

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
        # cv2.imwrite('test_image.png', np.array(ImageGrab.grab(bbox=capture_area)))
        y = 0
        for x in play_thread.images:
            # self.green_check = self.img_check[109:113, 77:81]
            # self.red_check = self.img_check[111:114, 224:227]
            # self.yellow_check = self.img_check[109:112, 370:373]
            # self.blue_check = self.img_check[115:118, 515:518]
            cv2.rectangle(np.array(x), (76, 108), (82,114), (255,0,0), 1)
            cv2.rectangle(np.array(x), (223, 110), (228,115), (255,0,0), 1)
            cv2.rectangle(np.array(x), (369, 108), (374,113), (255,0,0), 1)
            cv2.rectangle(np.array(x), (514, 114), (519,119), (255,0,0), 1)
            # cv2.rectangle(np.array(x), (76, 108), (82,114), (255,0,0), 1)
            cv2.imwrite('screenshot_img_{}.png'.format(y), np.array(x))
            y+=1
        play_thread.save_background()
        play_thread.release_all()
        play_thread.exit()
        listener.stop()

with Listener(on_press=on_press) as listener:
    listener.join()