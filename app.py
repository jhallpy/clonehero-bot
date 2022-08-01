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
            self.green_check = self.img_check[109:113, 77:81]
            self.red_check = self.img_check[109:113, 224:228]
            self.yellow_check = self.img_check[109:113, 370:374]
            self.blue_check = self.img_check[109:113, 515:519]
        
            self.green_ar_chk = self.img_check[83:87, 30:34]
            self.red_ar_chk = self.img_check[83:87, 168:172]
            self.yellow_ar_chk = self.img_check[83:87, 308:312]
            self.blue_ar_chk = self.img_check[83:87, 444:448]
            
    def set_background(self):
        self.capture()
        self.green_bg = self.img_check[109:113, 77:81]
        self.red_bg = self.img_check[109:113, 224:228]
        self.yellow_bg = self.img_check[109:113, 370:374]
        self.blue_bg = self.img_check[109:113, 515:519]
        
        self.green_ar = self.img_check[83:87, 30:34]
        self.red_ar = self.img_check[83:87, 168:172]
        self.yellow_ar = self.img_check[83:87, 308:312]
        self.blue_ar = self.img_check[83:87, 444:448]
    
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
        
        # Orange at some point.
        
        self.green_diff_two = cv2.subtract(np.asarray(self.green_ar_chk), np.asarray(self.green_ar)) + cv2.subtract(np.asarray(self.green_ar), np.asarray(self.green_ar_chk))
        self.green_diff[abs(self.green_diff) < 20.0] = 0
        
        self.red_diff_two = cv2.subtract(np.asarray(self.red_ar_chk), np.asarray(self.red_ar)) + cv2.subtract(np.asarray(self.red_ar), np.asarray(self.red_ar_chk))
        self.red_diff[abs(self.red_diff) < 20.0] = 0
        
        self.yellow_diff_two = cv2.subtract(np.asarray(self.yellow_ar_chk), np.asarray(self.yellow_ar)) + cv2.subtract(np.asarray(self.yellow_ar), np.asarray(self.yellow_ar_chk))
        self.yellow_diff[abs(self.yellow_diff) < 20.0] = 0
        
        self.blue_diff_two = cv2.subtract(np.asarray(self.blue_ar_chk), np.asarray(self.blue_ar)) + cv2.subtract(np.asarray(self.blue_ar), np.asarray(self.blue_ar_chk))
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
        self.images.append({"image": self.img_check, "green": self.green_diff, "red": self.red_diff, "yellow": self.yellow_diff, "blue": self.blue_diff})
            
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
        
    # TODO: Too tired to think this function through right now
    # def check_second_background(self):
    #     if(np.sum(self.red_diff_two) > 0 or np.sum(self.yellow_diff_two) > 0 or np.sum(self.blue_diff_two) > 0):
    #         if(np.sum(self.red_diff_two)>100):
    #             print(str(np.sum(self.red_diff_two)) +" secondary red")
    #             self.notes.append('s')
    #             self.red_strum = current_time()
    #         if(np.sum(self.yellow_diff_two)>100):
    #             print(str(np.sum(self.red_diff_two)) +" secondary red")
    #             self.notes.append('s')
    #             self.red_strum = current_time()
    #         if(np.sum(self.blue_diff_two)>100):
    #             print(str(np.sum(self.red_diff_two)) +" secondary red")
    #             self.notes.append('s')
    #             self.red_strum = current_time()
    #         # if(np.sum()>0):
    #         #     print()    

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
                    start = current_time()
                    self.set_area()
                    self.background_subtraction()
                    if(np.sum(self.green_diff) > 200 and np.sum(self.green_diff_two) > 100 and current_time() - self.green_strum > 26):
                        # print(str(current_time() - self.green_strum) + " green strum")
                        self.notes.append('a')
                        self.green_strum = current_time()
                        # print(current_time() - start)
                        if(np.sum(self.red_diff_two) > 0 or np.sum(self.yellow_diff_two) > 0 or np.sum(self.blue_diff_two) > 0):
                            if(np.sum(self.red_diff_two)>100):
                                # print(str(np.sum(self.red_diff_two)) +" secondary red")
                                self.red_strum = current_time()
                                self.notes.append('s')
                                self.red_strum = current_time()
                            if(np.sum(self.yellow_diff_two)>100):
                                # print(str(np.sum(self.yellow_diff_two)) +" secondary yellow")
                                self.yellow_strum = current_time()
                                self.notes.append('d')
                                self.red_strum = current_time()
                            if(np.sum(self.blue_diff_two)>100):
                                # print(str(np.sum(self.blue_diff_two)) +" secondary blue")
                                self.blue_strum = current_time()
                                self.notes.append('f')
                                self.red_strum = current_time()
                            # if(np.sum()>0):
                            #     print()    
                            
                    elif(np.sum(self.red_diff) > 0 and np.sum(self.red_diff_two) > 100 and current_time() - self.red_strum > 26):
                        # print(str(current_time() - self.red_strum) +" red strum")
                        self.red_strum = current_time()
                        self.notes.append('s')
                        if(np.sum(self.green_diff_two) > 0 or np.sum(self.yellow_diff_two) > 0 or np.sum(self.blue_diff_two) > 0):
                            if(np.sum(self.green_diff_two)>100):
                                # print(str(np.sum(self.green_diff_two)) +" secondary green")
                                self.green_strum = current_time()
                                self.notes.append('a')
                                self.red_strum = current_time()
                            if(np.sum(self.yellow_diff_two)>100):
                                # print(str(np.sum(self.yellow_diff_two)) +" secondary yellow")
                                self.yellow_strum = current_time()
                                self.notes.append('d')
                                self.red_strum = current_time()
                            if(np.sum(self.blue_diff_two)>100):
                                # print(str(np.sum(self.blue_diff_two)) +" secondary blue")
                                self.blue_strum = current_time()
                                self.notes.append('f')
                                self.red_strum = current_time()
                            # if(np.sum()>0):
                            #     print()
                        # print(current_time() - start)
                        
                    elif(np.sum(self.yellow_diff) > 0 and np.sum(self.yellow_diff_two) > 100 and current_time() - self.yellow_strum > 26):
                        # print(str(current_time() - self.yellow_strum) + " yellow strum")
                        self.yellow_strum = current_time()
                        self.notes.append('d')
                        if(np.sum(self.green_diff_two) > 0 or np.sum(self.yellow_diff_two) > 0 or np.sum(self.blue_diff_two) > 0):
                            if(np.sum(self.green_diff_two)>100):
                                # print(str(np.sum(self.green_diff_two)) +" secondary green")
                                self.green_strum = current_time()
                                self.notes.append('a')
                                self.red_strum = current_time()
                            if(np.sum(self.red_diff_two)>100):
                                # print(str(np.sum(self.red_diff_two)) +" secondary red")
                                self.red_strum = current_time()
                                self.notes.append('s')
                                self.red_strum = current_time()
                            if(np.sum(self.blue_diff_two)>100):
                                # print(str(np.sum(self.blue_diff_two)) +" secondary blue")
                                self.blue_strum = current_time()
                                self.notes.append('f')
                                self.red_strum = current_time()
                            # if(np.sum()>0):
                            #     print()
                        # print(current_time() - start)   
                    elif(np.sum(self.blue_diff) > 50 and np.sum(self.blue_diff_two) > 100 and current_time() - self.blue_strum > 26):
                        # print(str(current_time() - self.blue_strum) + " blue strum")
                        self.blue_strum = current_time()
                        self.notes.append('f')
                        if(np.sum(self.green_diff_two) > 0 or np.sum(self.yellow_diff_two) > 0 or np.sum(self.red_diff_two) > 0):
                            if(np.sum(self.green_diff_two)>100):
                                # print(str(np.sum(self.green_diff_two)) +" secondary green")
                                self.green_strum = current_time()
                                self.notes.append('a')
                                self.red_strum = current_time()
                            if(np.sum(self.red_diff_two)>100):
                                # print(str(np.sum(self.red_diff_two)) +" secondary red")
                                self.red_strum = current_time()
                                self.notes.append('s')
                                self.red_strum = current_time()
                            if(np.sum(self.yellow_diff_two)>100):
                                # print(str(np.sum(self.yellow_diff_two)) +" secondary yellow")
                                self.yellow_strum = current_time()
                                self.notes.append('d')
                                self.red_strum = current_time()
                            # if(np.sum()>0):
                            #     print()
                        # print(current_time() - start)   
                    if (len(self.notes) > 0):
                        print(self.notes)
                        print(str(i)+ " STRUM LINE \n ___________________________")
                        i+=1
                        self.release_all()
                        self.strum()
                        # self.save_image()
                        print(current_time() - start)
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
        cv2.imwrite('test_image.png', cv2.cvtColor(np.asarray(ImageGrab.grab(bbox=capture_area)), cv2.COLOR_RGB2BGR))
        y = 1
        # print(play_thread.images)
        for x in play_thread.images:
            cv2.rectangle(x['image'], (76, 108), (82,114), (255,0,0), 1)
            cv2.rectangle(x['image'], (223, 108), (229,114), (0,255,0), 1)
            cv2.rectangle(x['image'], (369, 108), (375,114), (255,0,0), 1)
            cv2.rectangle(x['image'], (514, 108), (520,114), (255,0,0), 1)
            # cv2.rectangle(x, (76, 108), (82,114), (255,0,0), 1)
            cv2.imwrite('img_{}_g{}_r{}_y{}_b{}.png'.format(y,np.sum(x['green']),np.sum(x['red']),np.sum(x['yellow']),np.sum(x['blue'])), cv2.cvtColor(x['image'], cv2.COLOR_RGB2BGR))
            y+=1
        # play_thread.save_background()
        play_thread.release_all()
        play_thread.exit()
        listener.stop()
        
with Listener(on_press=on_press) as listener: 
    listener.join()
 
# def main():
    
    
# if __name__ == "main":
#     main()