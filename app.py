import numpy as np
import time
import cv2
import dxcam
import threading
from pynput.keyboard import Key, Controller, Listener, KeyCode
from PIL import ImageGrab
from sys import getsizeof

camera = dxcam.create()
key_press = Controller()
capture_area = (650,850,1325,970)
start_stop_key = KeyCode(char='t')
stop_key = KeyCode(char='y')

GN_LOWER = np.array([50, 100, 80])
GN_UPPER = np.array([72, 255, 255])
R_LOWER = np.array([0, 100, 100])
R_UPPER = np.array([10, 255, 255])
YE_LOWER = np.array([20, 100, 100])
YE_UPPER = np.array([40, 255, 255])
BL_LOWER = np.array([100, 100, 100])
BL_UPPER = np.array([120, 255, 255])
OR_LOWER = np.array([])
OR_UPPER = np.array([])

class PlayRedux(threading.Thread):
    def __init__(self):
        super(PlayRedux, self).__init__()
        self.background_img = cv2.imread('background.png')
        self.running = False
        self.program_running = True
        self.capture_area = capture_area
        self.images = []
        
        self.gn_lower = GN_LOWER
        self.gn_upper = GN_UPPER
        self.r_lower = R_LOWER
        self.r_upper = R_UPPER
        self.ye_lower = YE_LOWER
        self.ye_upper = YE_UPPER
        self.bl_lower = BL_LOWER
        self.bl_upper = BL_UPPER
        self.or_lower = OR_LOWER
        self.or_upper = OR_UPPER
        
    def start_playing(self):
        self.running = True
        
    def stop_playing(self):
        self.running = False
     
    def exit(self):
        self.stop_playing()
        self.program_running = False
                
    def capture(self):
        self.img_check = camera.grab(self.capture_area)

    def set_background(self):
        # Converts RGB to HSV because DXcam currently captures in RGB
        converted = cv2.cvtColor(self.background_img, cv2.COLOR_RGB2HSV)
        
        gn_mask_bg = cv2.inRange(converted, self.gn_lower, self.gn_upper)
        r_mask_bg = cv2.inRange(converted, self.r_lower, self.r_upper)
        ye_mask_bg = cv2.inRange(converted, self.ye_lower, self.ye_upper)
        bl_mask_bg = cv2.inRange(converted, self.bl_lower, self.bl_upper)
        # or_mask_bg = cv2.inRange(converted, self.or_lower, self.or_upper)
        # Green needs to be 2 higher due to star notes very rarely not hitting the box, thus missing the note.
        self.gn_bg = gn_mask_bg[54:72, 77:95]
        self.gn_bg_t = gn_mask_bg[52:56, 48:52]
        
        self.r_bg = r_mask_bg[56:72, 208:227]
        self.r_bg_t = r_mask_bg[52:56, 179:183]
        # Yellow needed to be 2 higher in order to have at least some number when checking if other notes were present.
        self.ye_bg = ye_mask_bg[54:72, 345:372]
        self.ye_bg_t = ye_mask_bg[52:56, 310:314]
        
        self.bl_bg = bl_mask_bg[56:72, 474:500]
        self.bl_bg_t = bl_mask_bg[52:56, 435:439]
        
    def set_area(self):
        if (self.img_check is not None):
            # Converts RGB to HSV because DXcam currently captures in RGB
            converted = cv2.cvtColor(self.img_check, cv2.COLOR_RGB2HSV)
            
            self.gn_mask = cv2.inRange(converted, self.gn_lower, self.gn_upper)
            self.r_mask = cv2.inRange(converted, self.r_lower, self.r_upper)
            self.ye_mask = cv2.inRange(converted, self.ye_lower, self.ye_upper)
            self.bl_mask = cv2.inRange(converted, self.bl_lower, self.bl_upper)
            
            # Green needs to be 2 higher due to star notes very rarely not hitting the box, thus missing the note.
            self.gn_chk = self.gn_mask[54:72, 77:95]
            self.gn_chk_t = self.gn_mask[52:56, 48:52]
            
            self.r_chk = self.r_mask[56:72, 208:227]
            self.r_chk_t = self.r_mask[52:56, 179:183]
            
            # Yellow needed to be 2 higher in order to have at least some number when checking if other notes were present.
            self.ye_chk = self.ye_mask[54:72, 345:372]
            self.ye_chk_t = self.ye_mask[52:56, 310:314]
            
            self.bl_chk = self.bl_mask[56:72, 474:500]
            self.bl_chk_t = self.bl_mask[52:56, 435:439]
            
    def set_times(self):
        self.green_strum = current_time()
        self.red_strum = current_time()
        self.yellow_strum = current_time()
        self.blue_strum = current_time()
        self.orange_strum = current_time()
    
    def background_subtraction(self):
        self.gn_df = cv2.subtract(np.asarray(self.gn_chk), np.asarray(self.gn_bg)) + cv2.subtract(np.asarray(self.gn_bg), np.asarray(self.gn_chk))
        self.gn_df_t = cv2.subtract(np.asarray(self.gn_chk_t), np.asarray(self.gn_bg_t)) + cv2.subtract(np.asarray(self.gn_bg_t), np.asarray(self.gn_chk_t))
        self.r_df = cv2.subtract(np.asarray(self.r_chk), np.asarray(self.r_bg)) + cv2.subtract(np.asarray(self.r_bg), np.asarray(self.r_chk))
        self.r_df_t = cv2.subtract(np.asarray(self.r_chk_t), np.asarray(self.r_bg_t)) + cv2.subtract(np.asarray(self.r_bg_t), np.asarray(self.r_chk_t))
        self.ye_df = cv2.subtract(np.asarray(self.ye_chk), np.asarray(self.ye_bg)) + cv2.subtract(np.asarray(self.ye_bg), np.asarray(self.ye_chk))
        self.ye_df_t = cv2.subtract(np.asarray(self.ye_chk_t), np.asarray(self.ye_bg_t)) + cv2.subtract(np.asarray(self.ye_bg_t), np.asarray(self.ye_chk_t))
        self.bl_df = cv2.subtract(np.asarray(self.bl_chk), np.asarray(self.bl_bg)) + cv2.subtract(np.asarray(self.bl_bg), np.asarray(self.bl_chk))
        self.bl_df_t = cv2.subtract(np.asarray(self.bl_chk_t), np.asarray(self.bl_bg_t)) + cv2.subtract(np.asarray(self.bl_bg_t), np.asarray(self.bl_chk_t))
        # self.or_df = cv2.subtract(np.asarray(self.or_chk), np.asarray(self.or_bg)) + cv2.subtract(np.asarray(self.or_bg), np.asarray(self.or_chk))
        
    def save_image(self):
        self.images.append({"image": self.img_check, 
                            "green": np.sum(self.gn_df), "red": np.sum(self.r_df), "yellow": np.sum(self.ye_df), "blue": np.sum(self.bl_df),
                            "green_t": np.sum(self.gn_df_t), "red_t": np.sum(self.r_df_t), "yellow_t": np.sum(self.ye_df_t), "blue_t": np.sum(self.bl_df_t),
                            "played": self.played})
     
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
        while self.program_running:
            while self.running:
                self.capture()
                self.notes = []
                self.played = False
                start = current_time()
                # dxcam will return None if the image it takes would be the exact same image as the previous image. Therefore, this check is necessary.
                if (self.img_check is None):
                    continue
                else:
                    self.set_area()
                    self.background_subtraction()
                    # print(np.sum(self.r_df))
                        
                    if(np.sum(self.gn_df) > 300 and current_time() - self.green_strum > 38):
                        print(str(current_time() - self.green_strum) + " green strum")
                        self.green_strum = current_time()
                        self.played = True
                        self.img_check = self.gn_mask
                        self.notes.append('a')
                        if((np.sum(self.r_df) > 200 or np.sum(self.r_df_t) > 200) and current_time() - self.red_strum > 38):
                            self.red_strum = current_time()
                            self.played = True
                            self.notes.append('s')
                        if((np.sum(self.ye_df) > 200 or np.sum(self.ye_df_t) > 200)  and current_time() - self.yellow_strum > 38):
                            self.yellow_strum = current_time()
                            self.played = True
                            self.notes.append('d')
                        if((np.sum(self.bl_df) > 200 or np.sum(self.bl_df_t) > 200) and current_time() - self.blue_strum > 38):
                            self.blue_strum = current_time()
                            self.played = True
                            self.notes.append('f')   
                            
                    elif(np.sum(self.r_df) > 3000 and current_time() - self.red_strum > 38):
                        print(str(current_time() - self.red_strum) + " red strum")
                        self.red_strum = current_time()
                        self.played = True
                        self.notes.append('s')
                        # self.img_check = self.r_mask
                        if((np.sum(self.gn_df) > 200 or np.sum(self.gn_df_t) > 200) and current_time() - self.green_strum > 38):
                            self.green_strum = current_time()
                            self.played = True
                            self.notes.append('a')
                        if((np.sum(self.ye_df) > 200 or np.sum(self.ye_df_t) > 200) and current_time() - self.yellow_strum > 38):
                            self.yellow_strum = current_time()
                            self.played = True
                            self.notes.append('d')
                        if((np.sum(self.bl_df) > 200 or np.sum(self.bl_df_t) > 200) and current_time() - self.blue_strum > 38):
                            self.blue_strum = current_time()
                            self.played = True
                            self.notes.append('f')   
                               
                    elif(np.sum(self.ye_df) > 1500 and current_time() - self.yellow_strum > 38):
                        print(str(current_time() - self.yellow_strum) + " yellow strum")
                        self.yellow_strum = current_time()
                        self.played = True
                        self.notes.append('d')
                        # self.img_check = self.ye_mask
                        if((np.sum(self.gn_df) > 200 or np.sum(self.gn_df_t) > 200) and current_time() - self.green_strum > 38):
                            self.green_strum = current_time()
                            self.played = True
                            self.notes.append('a')
                        if((np.sum(self.r_df) > 200 or np.sum(self.r_df_t) > 200) and current_time() - self.red_strum > 38):
                            self.red_strum = current_time()
                            self.played = True
                            self.notes.append('s')
                        if((np.sum(self.bl_df) > 200 or np.sum(self.bl_df_t) > 200) and current_time() - self.blue_strum > 38):
                            self.blue_strum = current_time()
                            self.played = True
                            self.notes.append('f') 
                    
                    elif(np.sum(self.bl_df) > 1500 and current_time() - self.blue_strum > 38):
                        print(str(current_time() - self.blue_strum) + " blue strum")
                        self.blue_strum = current_time()
                        self.played = True
                        self.notes.append('f')
                        # self.img_check = self.bl_mask
                        if((np.sum(self.gn_df) > 200 or np.sum(self.gn_df_t) > 200) and current_time() - self.green_strum > 38):
                            self.green_strum = current_time()
                            self.played = True
                            self.notes.append('a')
                        if((np.sum(self.r_df) > 200 or np.sum(self.r_df_t) > 200) and current_time() - self.red_strum > 38):
                            self.red_strum = current_time()
                            self.played = True
                            self.notes.append('s')
                        if((np.sum(self.ye_df) > 200 or np.sum(self.ye_df_t) > 200) and current_time() - self.yellow_strum > 38):
                            self.yellow_strum = current_time()
                            self.played = True
                            self.notes.append('d')
                         
                    if (len(self.notes) > 0):
                        self.save_image()
                        self.release_all()
                        self.strum()
                    elif(np.sum(self.gn_df_t) > 0): # or np.sum(self.r_df_t) > 0 or np.sum(self.ye_df_t) > 0 or np.sum(self.bl_df_t) > 0):
                        self.img_check = self.gn_mask
                        self.save_image()
                    # print(current_time() - start)
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
            for x in play_thread.images:
                cv2.rectangle(x['image'], (76, 53), (96,73), (255,0,0), 1)
                cv2.rectangle(x['image'], (207, 55), (228,73), (255,0,0), 1)
                cv2.rectangle(x['image'], (344, 53), (373,73), (255,0,0), 1)
                cv2.rectangle(x['image'], (473, 55), (501,73), (255,0,0), 1)
                
                cv2.rectangle(x['image'], (47, 51), (53,57), (255,0,0), 1)
                cv2.rectangle(x['image'], (178, 51), (184,57), (255,0,0), 1)
                cv2.rectangle(x['image'], (309, 51), (315,57), (255,0,0), 1)
                cv2.rectangle(x['image'], (434, 51), (440,57), (255,0,0), 1)
                
                cv2.imwrite('img_{}_g{}_r{}_y{}_b{}_gt{}_rt{}_yt{}_bt{}_{}.png'.format(y, 
                                                                                        x['green'], x['red'], x['yellow'], x['blue'], 
                                                                                        x['green_t'], x['red_t'], x['yellow_t'], x['blue_t'], 
                                                                                        x['played']), cv2.cvtColor(x['image'], cv2.COLOR_BGR2RGB))
                y+=1
            play_thread.images = []
        else:
            play_thread.set_background()
            play_thread.release_all()
            play_thread.start_playing()
    elif key == stop_key:
        # cv2.imwrite('test_image.png', cv2.cvtColor(np.asarray(ImageGrab.grab(bbox=capture_area)), cv2.COLOR_RGB2BGR))
        # y=1
        # for x in play_thread.images:
        #     cv2.rectangle(x['image'], (78, 55), (96,73), (255,0,0), 1)
        #     cv2.rectangle(x['image'], (207, 55), (228,73), (255,0,0), 1)
        #     cv2.rectangle(x['image'], (338, 53), (373,73), (255,0,0), 1)
        #     cv2.rectangle(x['image'], (473, 55), (501,73), (255,0,0), 1)
        #     cv2.imwrite('img_{}_g{}_r{}_y{}_b{}_{}.png'.format(y, x['green'], x['red'], x['yellow'], x['blue'], x['played']), cv2.cvtColor(x['image'], cv2.COLOR_BGR2RGB))
        #     y+=1
        play_thread.release_all()
        play_thread.exit()
        listener.stop()
        
with Listener(on_press=on_press) as listener: 
    listener.join()
 
# def main():
    
    
# if __name__ == "main":
#     main()