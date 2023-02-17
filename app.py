import numpy as np
import time
import cv2
import dxcam
import threading
from background_subtraction import BackgroundSubtraction
from collections import deque
from pynput.keyboard import Key, Controller, Listener, KeyCode

camera = dxcam.create()
key_press = Controller()
capture_area = (595, 925, 1325, 987)
start_stop_key = KeyCode(char="t")
stop_key = KeyCode(char="y")

# (hMin = 76 , sMin = 0, vMin = 0), (hMax = 179 , sMax = 25, vMax = 234)
# NOTE: Test numbers:
# (hMin = 76 , sMin = 0, vMin = 0), (hMax = 179 , sMax = 36, vMax = 240)
# (hMin = 76 , sMin = 0, vMin = 166), (hMax = 179 , sMax = 25, vMax = 240)

W_LOWER = np.array([76, 0, 166])
W_UPPER = np.array([179, 25, 240])

# (hMin = 27 , sMin = 145, vMin = 0), (hMax = 32 , sMax = 255, vMax = 255)
S_LOWER = np.array([27, 145, 0])
S_UPPER = np.array([32, 255, 255])

# (hMin = 131 , sMin = 97, vMin = 90), (hMax = 179 , sMax = 255, vMax = 252)
P_LOWER = np.array([131, 97, 90])
P_UPPER = np.array([179, 255, 252])

STRUM_TIME = 12


class PlayRedux(threading.Thread):
    def __init__(self):
        super(PlayRedux, self).__init__()
        # NOTE: THis is loading as RGB and I don't know why.
        self.background_img = cv2.imread("background.png")
        cv2.imwrite("load_bg_test.png", self.background_img)
        self.running = False
        self.program_running = True
        self.capture_area = capture_area
        self.images = deque()

        self.green_time = []
        self.red_time = []
        self.yellow_time = []
        self.blue_time = []
        self.orange_time = []
        self.purple_time = []

        self.green_diff = []
        self.red_diff = []
        self.yellow_diff = []
        self.blue_diff = []
        self.orange_diff = []
        self.purple_diff = []

        self.w_lower = W_LOWER
        self.w_upper = W_UPPER
        self.s_lower = S_LOWER
        self.s_upper = S_UPPER
        self.p_lower = P_LOWER
        self.p_upper = P_UPPER

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
        # TODO: Either convert this back to background image
        # or look into how to make this work for other resolutions.
        # self.capture()

        converted = cv2.cvtColor(self.background_img, cv2.COLOR_RGB2HSV)
        mask_bg = cv2.inRange(converted, self.w_lower, self.w_upper)
        star_bg = cv2.inRange(converted, self.s_lower, self.s_upper)
        pur_mask_bg = cv2.inRange(converted, self.p_lower, self.p_upper)

        self.gn_bg = mask_bg[35:56, 30:95]
        self.rd_bg = mask_bg[35:56, 180:250]
        self.ye_bg = mask_bg[35:56, 320:400]
        self.bl_bg = mask_bg[35:56, 480:540]
        self.or_bg = mask_bg[35:56, 625:700]

        self.gn_bg_st = star_bg[35:56, 30:95]
        self.rd_bg_st = star_bg[35:56, 180:250]
        self.ye_bg_st = star_bg[35:56, 320:400]
        self.bl_bg_st = star_bg[35:56, 480:540]
        self.or_bg_st = star_bg[35:56, 625:700]

        cv2.imwrite("background_mask.png", mask_bg)
        cv2.imwrite("background_star_mask.png", star_bg)

        self.pur_bg = pur_mask_bg[10:20, 50:100]

        self.bs = BackgroundSubtraction(
            self.gn_bg_st,
            self.rd_bg_st,
            self.ye_bg_st,
            self.bl_bg_st,
            self.or_bg_st,
            self.gn_bg,
            self.rd_bg,
            self.ye_bg,
            self.bl_bg,
            self.or_bg,
            self.pur_bg,
        )

    def set_area(self):
        if self.img_check is not None:
            # NOTE: Leaving the note below for reasons.
            # DXcam should capture in RGB but somewhere in here
            # it's converted to BGR so.. BGR2HSV is needed instead.
            # Converts RGB to HSV because DXcam currently captures in RGB
            converted = cv2.cvtColor(self.img_check, cv2.COLOR_BGR2HSV)
            cv2.imwrite("testing.png", converted)

            self.mask = cv2.inRange(converted, self.w_lower, self.w_upper)
            self.star_mask = cv2.inRange(converted, self.s_lower, self.s_upper)
            self.pur_mask = cv2.inRange(converted, self.p_lower, self.p_upper)

            self.gn_chk = self.mask[35:56, 30:95]
            self.rd_chk = self.mask[35:56, 180:250]
            self.ye_chk = self.mask[35:56, 320:400]
            self.bl_chk = self.mask[35:56, 480:540]
            self.or_chk = self.mask[35:56, 625:700]

            self.gn_chk_st = self.star_mask[35:56, 30:95]
            self.rd_chk_st = self.star_mask[35:56, 180:250]
            self.ye_chk_st = self.star_mask[35:56, 320:400]
            self.bl_chk_st = self.star_mask[35:56, 480:540]
            self.or_chk_st = self.star_mask[35:56, 625:700]
            # cv2.imwrite('testing_yellow.png', self.ye_chk_st)
            self.pur_chk = self.pur_mask[10:20, 50:100]

    def set_times(self):
        self.green_strum = current_time()
        self.red_strum = current_time()
        self.yellow_strum = current_time()
        self.blue_strum = current_time()
        self.orange_strum = current_time()
        self.purple_strum = current_time()

    def background_subtraction(self):
        diff_list = self.bs.run_subtraction_in_parallel(
            self.gn_chk_st,
            self.rd_chk_st,
            self.ye_chk_st,
            self.bl_chk_st,
            self.or_chk_st,
            self.gn_chk,
            self.rd_chk,
            self.ye_chk,
            self.bl_chk,
            self.or_chk,
            self.pur_chk,
        )
        print(diff_list)
        self.gn_df = diff_list[0]
        self.rd_df = diff_list[1]
        self.ye_df = diff_list[2]
        self.bl_df = diff_list[3]
        self.or_df = diff_list[4]

        self.gn_st_df = diff_list[5]
        self.rd_st_df = diff_list[6]
        self.ye_st_df = diff_list[7]
        self.bl_st_df = diff_list[8]
        self.or_st_df = diff_list[9]

        self.pur_df = diff_list[10]

    def save_image(self):
        self.images.append(
            {
                "image": self.img_check,
                "green": np.sum(self.gn_df),
                "red": np.sum(self.rd_df),
                "yellow": np.sum(self.ye_df),
                "blue": np.sum(self.bl_df),
                "orange": np.sum(self.or_df),
                "purple": np.sum(self.pur_df),
                "green_t": np.sum(self.gn_st_df),
                "red_t": np.sum(self.rd_st_df),
                "yellow_t": np.sum(self.ye_st_df),
                "blue_t": np.sum(self.bl_st_df),
                "orange_t": np.sum(self.or_st_df),
                "puprle": np.sum(self.pur_df),
                "notes": self.notes,
            }
        )

    def strum(self):
        for x in self.notes:
            if str(x) == "p":
                continue
            else:
                key_press.press(str(x))
        key_press.tap(Key.down)

    def release_all(self):
        key_press.release("a")
        key_press.release("s")
        key_press.release("d")
        key_press.release("f")
        key_press.release("g")

    def check_colors(self):
        if (
            np.sum(self.pur_df) > 100
            and current_time() - self.purple_strum > STRUM_TIME
        ):
            self.purple_time.append(current_time() - self.purple_strum)
            (
                self.purple_strum,
                self.green_strum,
                self.red_strum,
                self.yellow_strum,
                self.blue_strum,
                self.orange_strum,
            ) = (current_time() - 4,) * 6

            self.played = True
            self.notes.append("p")
        if (
            np.sum(self.gn_df) > 60000 or np.sum(self.gn_st_df) > 70000
        ) and current_time() - self.green_strum > STRUM_TIME:
            self.green_time.append(current_time() - self.green_strum)
            self.green_strum = current_time()
            self.played = True
            self.notes.append("a")
        if (
            np.sum(self.rd_df) > 60000 or np.sum(self.rd_st_df) > 70000
        ) and current_time() - self.red_strum > STRUM_TIME:
            self.red_time.append(current_time() - self.red_strum)
            self.red_strum = current_time()
            self.played = True
            self.notes.append("s")
        if (
            np.sum(self.ye_df) > 60000 or np.sum(self.ye_st_df) > 70000
        ) and current_time() - self.yellow_strum > STRUM_TIME:
            self.yellow_time.append(current_time() - self.yellow_strum)
            self.yellow_strum = current_time()
            self.played = True
            self.notes.append("d")
        if (
            np.sum(self.bl_df) > 60000 or np.sum(self.bl_st_df) > 70000
        ) and current_time() - self.blue_strum > STRUM_TIME:
            self.blue_time.append(current_time() - self.blue_strum)
            self.blue_strum = current_time()
            self.played = True
            self.notes.append("f")
        if (
            np.sum(self.or_df) > 60000 or np.sum(self.or_st_df) > 70000
        ) and current_time() - self.orange_strum > STRUM_TIME:
            self.orange_time.append(current_time() - self.orange_strum)
            self.orange_strum = current_time()
            self.played = True
            self.notes.append("g")

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

                # NOTE: dxcam will return None if the image it takes would be
                # the exact same image as the previous image. Therefore,
                # this check is necessary.
                if self.img_check is None:
                    continue

                else:
                    self.set_area()
                    self.background_subtraction()
                    # self.save_image()

                    if (
                        np.sum(self.pur_df) > 1000
                        and current_time() - self.purple_strum > STRUM_TIME
                    ):
                        self.check_colors()

                    elif (
                        np.sum(self.gn_df) > 60000 or np.sum(self.gn_st_df) > 70000
                    ) and current_time() - self.green_strum > STRUM_TIME:
                        self.check_colors()

                    elif (
                        np.sum(self.rd_df) > 60000 or np.sum(self.rd_st_df) > 70000
                    ) and current_time() - self.red_strum > STRUM_TIME:
                        self.check_colors()

                    elif (
                        np.sum(self.ye_df) > 60000 or np.sum(self.ye_st_df) > 70000
                    ) and current_time() - self.yellow_strum > STRUM_TIME:
                        self.check_colors()

                    elif (
                        np.sum(self.bl_df) > 60000 or np.sum(self.bl_st_df) > 70000
                    ) and current_time() - self.blue_strum > STRUM_TIME:
                        self.check_colors()

                    elif (
                        np.sum(self.or_df) > 60000 or np.sum(self.or_st_df) > 70000
                    ) and current_time() - self.orange_strum > STRUM_TIME:
                        self.check_colors()

                    if np.sum(self.gn_df) > 20000:
                        self.save_image()
                    elif np.sum(self.rd_df) > 20000:
                        self.save_image()
                    elif np.sum(self.ye_df) > 20000:
                        self.save_image()
                    elif np.sum(self.bl_df) > 20000:
                        self.save_image()
                    elif np.sum(self.or_df) > 20000:
                        self.save_image()
                    elif np.sum(self.pur_df) > 20000:
                        self.save_image()

                    if self.notes:
                        # self.save_image()
                        self.release_all()
                        self.strum()

                try:
                    if 1000 / (current_time() - start) < 200:
                        print("FPS:", 1000 / (current_time() - start))
                except ZeroDivisionError:
                    continue

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
            key_press.tap(Key.enter)
            cv2.destroyAllWindows()

            y = 1

            try:
                if len(play_thread.green_time) > 0:
                    play_thread.green_time.sort()
                    print(str(play_thread.green_time[0]) + "\t Green Time")
                if len(play_thread.red_time) > 0:
                    play_thread.red_time.sort()
                    print(str(play_thread.red_time[0]) + "\t Red Time")
                if len(play_thread.yellow_time) > 0:
                    play_thread.yellow_time.sort()
                    print(str(play_thread.yellow_time[0]) + "\t Yellow Time")
                if len(play_thread.blue_time) > 0:
                    play_thread.blue_time.sort()
                    print(str(play_thread.blue_time[0]) + "\t Blue Time")
                if len(play_thread.orange_time) > 0:
                    play_thread.orange_time.sort()
                    print(str(play_thread.orange_time[0]) + "\t Orange Time")
                if len(play_thread.purple_time) > 0:
                    play_thread.purple_time.sort()
                    print(str(play_thread.purple_time[0]) + "\t Purple Time")

                # if(len(play_thread.green_diff) > 0):
                #     play_thread.green_diff.sort(reverse=True)
                #     print(str(play_thread.green_diff[0]) + '\t Green Max')
                # if(len(play_thread.red_diff) > 0):
                #     play_thread.red_diff.sort(reverse=True)
                #     print(str(play_thread.red_diff[0]) + '\t Red Max')
                # if(len(play_thread.yellow_diff) > 0):
                #     play_thread.yellow_diff.sort(reverse=True)
                #     print(str(play_thread.yellow_diff[0]) + '\t Yellow Max')
                # if(len(play_thread.blue_diff) > 0):
                #     play_thread.blue_diff.sort(reverse=True)
                #     print(str(play_thread.blue_diff[0]) + '\t Blue Max')
                # if(len(play_thread.orange_diff) > 0):
                #     play_thread.orange_diff.sort(reverse=True)
                #     print(str(play_thread.orange_diff[0]) + '\t Orange Max')
                # if(len(play_thread.purple_diff) > 0):
                #     play_thread.purple_diff.sort(reverse=True)
                #     print(str(play_thread.purple_diff[0]) + '\t Purple Max')
            except Exception as e:
                print("There has been an error:", e)

            # NOTE: Only useful for saving images for debugging purposes.

            # Converts doubly-linked list to a list.
            play_thread.images = list(play_thread.images)

            for x in play_thread.images:
                # self.gn_bg = gn_mask_bg[35:56, 30:95]
                # self.r_bg = r_mask_bg[35:56, 180:250]
                # self.ye_bg = ye_mask_bg[35:56, 320:400]
                # self.bl_bg = bl_mask_bg[35:56, 480:540]
                # self.or_bg = or_mask_bg[35:56, 625:700]

                # # self.pur_bg = pur_mask_bg[35:56, 10:60]
                cv2.rectangle(x["image"], (29, 36), (96, 57), (255, 0, 0), 1)
                cv2.rectangle(x["image"], (179, 36), (251, 57), (255, 0, 0), 1)
                cv2.rectangle(x["image"], (319, 36), (401, 57), (255, 0, 0), 1)
                cv2.rectangle(x["image"], (479, 36), (541, 57), (255, 0, 0), 1)
                cv2.rectangle(x["image"], (624, 36), (701, 57), (255, 0, 0), 1)

                cv2.imwrite(
                    "data/images/img_{}_g{}_r{}_y{}_b{}_o{}_p{}_gt{}_rt{}_yt{}"
                    "_bt{}_ot{}_{}"
                    ".png".format(
                        y,
                        x["green"],
                        x["red"],
                        x["yellow"],
                        x["blue"],
                        x["orange"],
                        x["purple"],
                        x["green_t"],
                        x["red_t"],
                        x["yellow_t"],
                        x["blue_t"],
                        x["orange_t"],
                        x["notes"],
                    ),
                    cv2.cvtColor(x["image"], cv2.COLOR_BGR2RGB),
                )

                # cv2.imwrite(
                #     "data/images/img_{}_g{}_r{}_y{}_b{}_o{}_MASKED"
                #     ".png".format(
                #         y,
                #         x["green"],
                #         x["red"],
                #         x["yellow"],
                #         x["blue"],
                #         x["orange"],
                #     ),
                #     # x['image'])
                #     cv2.inRange(
                #         cv2.cvtColor(x["image"], cv2.COLOR_BGR2HSV),
                #         play_thread.w_lower,
                #         play_thread.w_upper,
                #     ),
                # )

                y += 1
            play_thread.images = []
            print("Bot Stopped.")
        else:
            print("Bot Running...")
            play_thread.set_background()
            play_thread.release_all()
            play_thread.start_playing()
    elif key == stop_key:
        play_thread.release_all()
        play_thread.exit()
        cv2.destroyAllWindows()
        print("Exiting...")
        listener.stop()


with Listener(on_press=on_press) as listener:
    listener.join()

# def main():

# NOTE: Should work but doesn't. Will look for fix when I finish the program.
# if __name__ == "main":
#     main()
