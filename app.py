import numpy as np
import time
import cv2
import dxcam
import threading
from pynput.keyboard import Key, Controller, Listener, KeyCode

camera = dxcam.create()
key_press = Controller()
capture_area = (650,850,1325,970)
start_stop_key = KeyCode(char='t')
stop_key = KeyCode(char='y')
# White lines would be picked up with the saturation too high on lower. This shouldn't cause a note issue as their saturation is higher.
GN_LOWER = np.array([50, 133, 80])
GN_UPPER = np.array([72, 255, 255])
# Red star notes would sometimes miss, therefore I lowered the value to increase match chance of red.
R_LOWER = np.array([0, 100, 60])
R_UPPER = np.array([10, 255, 255])

YE_LOWER = np.array([20, 100, 100])
YE_UPPER = np.array([40, 255, 255])
# Blue and orange are unique, the note color and the hold note line are not the exact same color so the line can be completely erased.
BL_LOWER = np.array([100, 100, 100])
BL_UPPER = np.array([104, 255, 255])
# Orange saturation would sometimes catch the thick white line. This shouldn't cause a note issue as their saturation is higher.
OR_LOWER = np.array([19, 178, 100])
OR_UPPER = np.array([21, 255, 255])

PUR_LOWER = np.array([98, 100, 100])
PUR_UPPER = np.array([145, 255, 255])

STRUM_TIME = 41

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
        self.pur_lower = PUR_LOWER
        self.pur_upper = PUR_UPPER
        
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
        self.capture()
        # Converts RGB to HSV because DXcam currently captures in RGB
        converted = cv2.cvtColor(self.img_check, cv2.COLOR_RGB2HSV)
        
        gn_mask_bg = cv2.inRange(converted, self.gn_lower, self.gn_upper)
        r_mask_bg =  cv2.inRange(converted, self.r_lower, self.r_upper)
        ye_mask_bg = cv2.inRange(converted, self.ye_lower, self.ye_upper)
        bl_mask_bg = cv2.inRange(converted, self.bl_lower, self.bl_upper)
        or_mask_bg = cv2.inRange(converted, self.or_lower, self.or_upper)
        pur_mask_bg = cv2.inRange(converted, self.pur_lower, self.pur_upper)
        # Green needs to be 2 higher due to star notes very rarely not hitting the box, thus missing the note.
        self.gn_bg = gn_mask_bg[54:90, 77:95]
        self.gn_bg_t = gn_mask_bg[52:56, 10:70]
        # Red's second tracker needs to be higher because of star notes.
        self.r_bg = r_mask_bg[56:90, 213:227]
        self.r_bg_t = r_mask_bg[49:56, 140:210]
        # Yellow needed to be 2 higher in order to have at least some number when checking if other notes were present.
        self.ye_bg = ye_mask_bg[54:72, 345:372]
        self.ye_bg_t = ye_mask_bg[52:56, 280:340]
        
        self.bl_bg = bl_mask_bg[56:67, 387:500]
        self.bl_bg_t = bl_mask_bg[52:56, 400:480]
        
        self.or_bg = or_mask_bg[54:72, 530:643]
        self.or_bg_t = or_mask_bg[52:56, 540:620]
        
        self.pur_bg = pur_mask_bg[54:72, 530:643]
        self.pur_bg_t = gn_mask_bg[54:72, 77:95]
        
    def set_area(self):
        if (self.img_check is not None):
            # Converts RGB to HSV because DXcam currently captures in RGB
            converted = cv2.cvtColor(self.img_check, cv2.COLOR_RGB2HSV)
            
            self.gn_mask = cv2.inRange(converted, self.gn_lower, self.gn_upper)
            self.r_mask =  cv2.inRange(converted, self.r_lower, self.r_upper)
            self.ye_mask = cv2.inRange(converted, self.ye_lower, self.ye_upper)
            self.bl_mask = cv2.inRange(converted, self.bl_lower, self.bl_upper)
            self.or_mask = cv2.inRange(converted, self.or_lower, self.or_upper)
            self.pur_mask = cv2.inRange(converted, self.pur_lower, self.pur_upper)
        
            # self.test_mask = cv2.inRange(converted, self.t_lower, self.t_upper)
            
            # Green needs to be 2 higher due to star notes very rarely not hitting the box, thus missing the note.
            self.gn_chk = self.gn_mask[54:90, 77:95]
            self.gn_chk_t = self.gn_mask[52:56, 10:70]
            # Red's second tracker needs to be higher because of star notes.
            self.r_chk = self.r_mask[56:90, 213:227]
            self.r_chk_t = self.r_mask[49:56, 140:210]
            # Yellow needed to be 2 higher in order to have at least some number when checking if other notes were present.
            self.ye_chk = self.ye_mask[54:72, 345:372]
            self.ye_chk_t = self.ye_mask[52:56, 280:340]
            
            self.bl_chk = self.bl_mask[56:67, 387:500]
            self.bl_chk_t = self.bl_mask[52:56, 400:480]
            
            self.or_chk = self.or_mask[54:72, 530:643]
            self.or_chk_t = self.or_mask[52:56, 540:620]
            
            self.pur_chk = self.pur_mask[54:72, 530:643]
            self.pur_chk_t = self.pur_mask[54:72, 77:95]
            
    def set_times(self):
        self.green_strum = current_time()
        self.red_strum = current_time()
        self.yellow_strum = current_time()
        self.blue_strum = current_time()
        self.orange_strum = current_time()
        self.purple_strum = current_time()
    
    def background_subtraction(self):
        self.gn_df = cv2.subtract(np.asarray(self.gn_chk), np.asarray(self.gn_bg)) + cv2.subtract(np.asarray(self.gn_bg), np.asarray(self.gn_chk))
        self.gn_df_t = cv2.subtract(np.asarray(self.gn_chk_t), np.asarray(self.gn_bg_t)) + cv2.subtract(np.asarray(self.gn_bg_t), np.asarray(self.gn_chk_t))
        self.r_df = cv2.subtract(np.asarray(self.r_chk), np.asarray(self.r_bg)) + cv2.subtract(np.asarray(self.r_bg), np.asarray(self.r_chk))
        self.r_df_t = cv2.subtract(np.asarray(self.r_chk_t), np.asarray(self.r_bg_t)) + cv2.subtract(np.asarray(self.r_bg_t), np.asarray(self.r_chk_t))
        self.ye_df = cv2.subtract(np.asarray(self.ye_chk), np.asarray(self.ye_bg)) + cv2.subtract(np.asarray(self.ye_bg), np.asarray(self.ye_chk))
        self.ye_df_t = cv2.subtract(np.asarray(self.ye_chk_t), np.asarray(self.ye_bg_t)) + cv2.subtract(np.asarray(self.ye_bg_t), np.asarray(self.ye_chk_t))
        self.bl_df = cv2.subtract(np.asarray(self.bl_chk), np.asarray(self.bl_bg)) + cv2.subtract(np.asarray(self.bl_bg), np.asarray(self.bl_chk))
        self.bl_df_t = cv2.subtract(np.asarray(self.bl_chk_t), np.asarray(self.bl_bg_t)) + cv2.subtract(np.asarray(self.bl_bg_t), np.asarray(self.bl_chk_t))
        self.or_df = cv2.subtract(np.asarray(self.or_chk), np.asarray(self.or_bg)) + cv2.subtract(np.asarray(self.or_bg), np.asarray(self.or_chk))
        self.or_df_t = cv2.subtract(np.asarray(self.or_chk_t), np.asarray(self.or_bg_t)) + cv2.subtract(np.asarray(self.or_bg_t), np.asarray(self.or_chk_t))
        self.pur_df = cv2.subtract(np.asarray(self.pur_chk), np.asarray(self.pur_bg)) + cv2.subtract(np.asarray(self.pur_bg), np.asarray(self.pur_chk))
        self.pur_df_t = cv2.subtract(np.asarray(self.pur_chk_t), np.asarray(self.pur_bg_t)) + cv2.subtract(np.asarray(self.pur_bg_t), np.asarray(self.pur_chk_t))
        
    def save_image(self):
        self.images.append({"image": self.img_check, 
                            "green": np.sum(self.gn_df), "red": np.sum(self.r_df), "yellow": np.sum(self.ye_df), "blue": np.sum(self.bl_df), "orange": np.sum(self.or_df),
                            "green_t": np.sum(self.gn_df_t), "red_t": np.sum(self.r_df_t), "yellow_t": np.sum(self.ye_df_t), "blue_t": np.sum(self.bl_df_t), "orange_t": np.sum(self.or_df_t),
                            "played": self.played})
        
    def strum(self):
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
        
    def check_colors(self):
        if(np.sum(self.pur_df) > 100 and np.sum(self.pur_df_t) > 100 and current_time() - self.purple_strum > STRUM_TIME):
            self.purple_strum = current_time()
            # NOTE: Blue will strum the purple when it is a star note.
            self.blue_strum = current_time()
            self.played = True
            self.notes.append('p')
        if((np.sum(self.gn_df) > 200 or np.sum(self.gn_df_t) > 200) and current_time() - self.green_strum > STRUM_TIME):
            self.green_strum = current_time()
            self.played = True
            self.notes.append('a')
        if((np.sum(self.r_df) > 200 or np.sum(self.r_df_t) > 200) and current_time() - self.red_strum > STRUM_TIME):
            self.red_strum = current_time()
            self.played = True
            self.notes.append('s')
        if((np.sum(self.ye_df) > 200 or np.sum(self.ye_df_t) > 200)  and current_time() - self.yellow_strum > STRUM_TIME):
            self.yellow_strum = current_time()
            self.played = True
            self.notes.append('d')
        if((np.sum(self.bl_df) > 34000 or np.sum(self.bl_df_t) > 200) and current_time() - self.blue_strum > STRUM_TIME):
            self.blue_strum = current_time()
            self.played = True
            self.notes.append('f')   
        if((np.sum(self.or_df) > 200 or np.sum(self.or_df_t) > 200) and current_time() - self.orange_strum > STRUM_TIME):
            self.orange_strum = current_time()
            self.played = True
            self.notes.append('g')
            
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
                # NOTE: dxcam will return None if the image it takes would be the exact same image as the previous image. Therefore, this check is necessary.
                if (self.img_check is None):
                    continue
                else:
                    self.set_area()
                    self.background_subtraction()
                    
                    # NOTE: Purple must come first. The purple bar when it is a 'star note' is within the range of blue. 
                    # NOTE: The addition of the blue strum timeout fixes firing on the next frame. 
                    if(np.sum(self.pur_df) > 100 and current_time() - self.purple_strum > STRUM_TIME):
                        # print(str(current_time() - self.purple_strum) + " purple strum")    
                        self.check_colors()
                        
                    elif(np.sum(self.gn_df) > 1600 and current_time() - self.green_strum > STRUM_TIME):
                        # print(str(current_time() - self.green_strum) + " green strum")
                        self.check_colors()
                        
                    elif(np.sum(self.r_df) > 1500 and current_time() - self.red_strum > STRUM_TIME):
                        # print(str(current_time() - self.red_strum) + " red strum")
                        self.check_colors()
                                  
                    elif(np.sum(self.ye_df) > 1500 and current_time() - self.yellow_strum > STRUM_TIME):
                        # print(str(current_time() - self.yellow_strum) + " yellow strum")
                        self.check_colors()
                            
                    elif(np.sum(self.bl_df) > 1500 and current_time() - self.blue_strum > STRUM_TIME):
                        # print(str(current_time() - self.blue_strum) + " blue strum")
                        self.check_colors()
                            
                    # Current highest orange that is not a note is 1530
                    elif(np.sum(self.or_df) > 1600 and current_time() - self.orange_strum > STRUM_TIME):
                        # print(str(current_time() - self.orange_strum) + " orange strum")
                        self.check_colors()
                    
                    if (len(self.notes) > 0):
                        # self.save_image()
                        self.release_all()
                        self.strum()
                        
                    # NOTE: Leaving this commented for future debugging. I was too lazy to figure out best practices for debugging like this.
                    # elif(np.sum(self.pur_df) > 100):
                    #     print(np.sum(self.pur_df))
                    #     print(np.sum(self.pur_df_t))
                    # elif(np.sum(self.gn_df_t) > 0):
                    #     self.img_check = self.gn_mask
                    #     self.save_image()
                    # elif(np.sum(self.r_df_t) > 0):
                    #     self.img_check = self.r_mask
                    #     self.save_image()
                    # elif(np.sum(self.ye_df_t) > 0): 
                    #     # self.img_check = self.ye_mask
                    #     self.save_image()
                    # elif(np.sum(self.bl_df_t) > 0 or np.sum(self.bl_df) > 0 ): 
                    #     self.img_check = self.bl_mask
                    #     self.save_image()
                    # elif(np.sum(self.or_df_t) > 0):
                    #     # self.img_check = self.or_mask
                    #     self.save_image()
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
            
            # try:
            #     play_thread.r_low.sort()
            #     print('red low: ' + str(play_thread.r_low[0]))
            #     play_thread.r_low2.sort(reverse=True)
            #     print('red low 2: ' + str(play_thread.r_low2[0]))
            # except:
            #     print('No red.')

            # NOTE: Only useful for saving images for debugging purposes. 
            for x in play_thread.images:
                cv2.rectangle(x['image'], (76, 53), (96,91), (255,0,0), 1)
                cv2.rectangle(x['image'], (212, 55), (228,91), (255,0,0), 1)
                cv2.rectangle(x['image'], (344, 53), (373,73), (255,0,0), 1)
                cv2.rectangle(x['image'], (386, 55), (501,68), (255,0,0), 1)
                cv2.rectangle(x['image'], (529, 55), (644,68), (255,0,0), 1)
                
                cv2.rectangle(x['image'], (9, 51), (71,57), (255,0,0), 1)
                cv2.rectangle(x['image'], (139, 48), (211,57), (255,0,0), 1)
                cv2.rectangle(x['image'], (279, 51), (341,57), (255,0,0), 1)
                cv2.rectangle(x['image'], (399, 51), (481,57), (255,0,0), 1)
                cv2.rectangle(x['image'], (539, 51), (621,57), (255,0,0), 1)
                
                cv2.imwrite('imgs\img_{}_g{}_r{}_y{}_b{}_o{}_gt{}_rt{}_yt{}_bt{}_ot{}_{}.png'.format(y, 
                                                                                        x['green'], x['red'], x['yellow'], x['blue'], x['orange'],
                                                                                        x['green_t'], x['red_t'], x['yellow_t'], x['blue_t'], x['orange_t'],
                                                                                        x['played']), cv2.cvtColor(x['image'], cv2.COLOR_BGR2RGB))
                y+=1
            play_thread.images = []
            print('Bot Stopped.')
        else:
            print('Bot Running...')
            play_thread.set_background()
            play_thread.release_all()
            play_thread.start_playing()
    elif key == stop_key:
        play_thread.release_all()
        play_thread.exit()
        listener.stop()
        
with Listener(on_press=on_press) as listener: 
    listener.join()

# def main():
    
# NOTE: Should work but doesn't. Will look for fix when I finish the program.
# if __name__ == "main":
#     main()