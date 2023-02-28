import numpy as np
import time
import cv2
import dxcam
import threading
import empty_file as ef

# TODO: Add a second capture in the same area but smaller. This should solve the problem of notes not disappearing correctly in the game.
# TODO: Add a GUI with PyQt for ease of use.


# from background_subtraction import BackgroundSubtraction
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
# (hMin = 76 , sMin = 0, vMin = 78), (hMax = 179 , sMax = 25, vMax = 240)
# (hMin = 91 , sMin = 0, vMin = 78), (hMax = 179 , sMax = 24, vMax = 250)

W_LOWER = np.array([76, 0, 0])
W_UPPER = np.array([179, 25, 240])

# (hMin = 27 , sMin = 145, vMin = 0), (hMax = 32 , sMax = 255, vMax = 255)
S_LOWER = np.array([27, 145, 0])
S_UPPER = np.array([32, 255, 255])

# (hMin = 131 , sMin = 97, vMin = 90), (hMax = 179 , sMax = 255, vMax = 252)
# NOTE: Test values
# (hMin = 131 , sMin = 20, vMin = 159), (hMax = 179 , sMax = 255, vMax = 252)
# (hMin = 131 , sMin = 20, vMin = 145), (hMax = 179 , sMax = 255, vMax = 255)
P_LOWER = np.array([131, 20, 145])
P_UPPER = np.array([179, 255, 252])

STRUM_TIME = 6

# Yellow
# (hMin = 84 , sMin = 170, vMin = 0), (hMax = 93 , sMax = 255, vMax = 255)


class PlayRedux(threading.Thread):
    def __init__(self):
        super(PlayRedux, self).__init__()
        # NOTE: THis is loading as RGB and I don't know why.
        ef.clear_file()
        # ef.clear_trash()
        print("Trash cleared.")

        self.background_img = cv2.imread("background.png")
        cv2.imwrite("load_bg_test.png", self.background_img)
        self.running = False
        self.program_running = True
        self.capture_area = capture_area
        self.images = deque(maxlen=250)

        self.green_time = []
        self.red_time = []
        self.yellow_time = []
        self.blue_time = []
        self.orange_time = []
        self.purple_time = []

        self.w_lower = W_LOWER
        self.w_upper = W_UPPER
        self.s_lower = S_LOWER
        self.s_upper = S_UPPER
        self.p_lower = P_LOWER
        self.p_upper = P_UPPER
        print("Loaded...")

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

        self.gn_bg = mask_bg[54:58, 30:95]
        self.rd_bg = mask_bg[54:58, 180:250]
        self.ye_bg = mask_bg[54:58, 320:400]
        self.bl_bg = mask_bg[54:58, 480:540]
        self.or_bg = mask_bg[54:58, 625:700]

        self.gn_bg_two = mask_bg[47:54, 108:112]
        self.rd_bg_two = mask_bg[47:54, 259:263]
        self.ye_bg_two = mask_bg[47:54, 411:415]
        self.bl_bg_two = mask_bg[47:54, 468:472]
        self.or_bg_two = mask_bg[47:54, 615:619]

        self.gn_bg_st = star_bg[54:58, 30:95]
        self.rd_bg_st = star_bg[54:58, 180:250]
        self.ye_bg_st = star_bg[54:58, 320:400]
        self.bl_bg_st = star_bg[54:58, 480:540]
        self.or_bg_st = star_bg[54:58, 625:700]

        self.gn_bg_st_two = star_bg[50:54, 30:95]
        self.rd_bg_st_two = star_bg[50:54, 180:250]
        self.ye_bg_st_two = star_bg[50:54, 320:400]
        self.bl_bg_st_two = star_bg[50:54, 480:540]
        self.or_bg_st_two = star_bg[50:54, 625:700]

        self.pur_bg = pur_mask_bg[10:20, 50:100]
        self.pur_bg_two = pur_mask_bg[10:20, 190:225]

    def set_area(self):
        if self.img_check is not None:
            # NOTE: Leaving the note below for reasons.
            # DXcam should capture in RGB but somewhere in here
            # it's converted to BGR so.. BGR2HSV is needed instead.
            # Converts RGB to HSV because DXcam currently captures in RGB
            converted = cv2.cvtColor(self.img_check, cv2.COLOR_BGR2HSV)

            self.mask = cv2.inRange(converted, self.w_lower, self.w_upper)
            self.star_mask = cv2.inRange(converted, self.s_lower, self.s_upper)
            self.pur_mask = cv2.inRange(converted, self.p_lower, self.p_upper)

            self.gn_chk = self.mask[54:58, 30:95]
            self.rd_chk = self.mask[54:58, 180:250]
            self.ye_chk = self.mask[54:58, 320:400]
            self.bl_chk = self.mask[54:58, 480:540]
            self.or_chk = self.mask[54:58, 625:700]

            self.gn_chk_two = self.mask[47:54, 108:112]
            self.rd_chk_two = self.mask[47:54, 259:263]
            self.ye_chk_two = self.mask[47:54, 411:415]
            self.bl_chk_two = self.mask[47:54, 468:472]
            self.or_chk_two = self.mask[47:54, 615:619]

            self.gn_chk_st = self.star_mask[54:58, 30:95]
            self.rd_chk_st = self.star_mask[54:58, 180:250]
            self.ye_chk_st = self.star_mask[54:58, 320:400]
            self.bl_chk_st = self.star_mask[54:58, 480:540]
            self.or_chk_st = self.star_mask[54:58, 625:700]

            self.gn_chk_st_two = self.star_mask[50:54, 30:95]
            self.rd_chk_st_two = self.star_mask[50:54, 180:250]
            self.ye_chk_st_two = self.star_mask[50:54, 320:400]
            self.bl_chk_st_two = self.star_mask[50:54, 480:540]
            self.or_chk_st_two = self.star_mask[50:54, 625:700]

            self.pur_chk = self.pur_mask[10:20, 50:100]
            self.pur_chk_two = self.pur_mask[10:20, 190:225]

    def set_times(self):
        self.green_strum = current_time()
        self.red_strum = current_time()
        self.yellow_strum = current_time()
        self.blue_strum = current_time()
        self.orange_strum = current_time()
        self.purple_strum = current_time()

    def background_subtraction(self):
        self.gn_df = np.sum(cv2.absdiff(self.gn_bg, self.gn_chk))
        self.rd_df = np.sum(cv2.absdiff(self.rd_bg, self.rd_chk))
        self.ye_df = np.sum(cv2.absdiff(self.ye_bg, self.ye_chk))
        self.bl_df = np.sum(cv2.absdiff(self.bl_bg, self.bl_chk))
        self.or_df = np.sum(cv2.absdiff(self.or_bg, self.or_chk))

        self.gn_df_two = np.sum(cv2.absdiff(self.gn_bg_two, self.gn_chk_two))
        self.rd_df_two = np.sum(cv2.absdiff(self.rd_bg_two, self.rd_chk_two))
        self.ye_df_two = np.sum(cv2.absdiff(self.ye_bg_two, self.ye_chk_two))
        self.bl_df_two = np.sum(cv2.absdiff(self.bl_bg_two, self.bl_chk_two))
        self.or_df_two = np.sum(cv2.absdiff(self.or_bg_two, self.or_chk_two))

        self.gn_st_df = np.sum(cv2.absdiff(self.gn_bg_st, self.gn_chk_st))
        self.rd_st_df = np.sum(cv2.absdiff(self.rd_bg_st, self.rd_chk_st))
        self.ye_st_df = np.sum(cv2.absdiff(self.ye_bg_st, self.ye_chk_st))
        self.bl_st_df = np.sum(cv2.absdiff(self.bl_bg_st, self.bl_chk_st))
        self.or_st_df = np.sum(cv2.absdiff(self.or_bg_st, self.or_chk_st))

        self.gn_st_df_two = np.sum(cv2.absdiff(self.gn_bg_st_two, self.gn_chk_st_two))
        self.rd_st_df_two = np.sum(cv2.absdiff(self.rd_bg_st_two, self.rd_chk_st_two))
        self.ye_st_df_two = np.sum(cv2.absdiff(self.ye_bg_st_two, self.ye_chk_st_two))
        self.bl_st_df_two = np.sum(cv2.absdiff(self.bl_bg_st_two, self.bl_chk_st_two))
        self.or_st_df_two = np.sum(cv2.absdiff(self.or_bg_st_two, self.or_chk_st_two))

        self.pur_df = np.sum(cv2.absdiff(self.pur_bg, self.pur_chk))
        self.pur_df_two = np.sum(cv2.absdiff(self.pur_bg_two, self.pur_chk_two))

    def save_image(self):
        self.images.append(
            {
                "image": self.img_check,
                "green": self.gn_df,
                "red": self.rd_df,
                "yellow": self.ye_df,
                "blue": self.bl_df,
                "orange": self.or_df,
                "purple": [self.pur_df, self.pur_df_two],
                "green_t": self.gn_st_df,
                "red_t": self.rd_st_df,
                "yellow_t": self.ye_st_df,
                "blue_t": self.bl_st_df,
                "orange_t": self.or_st_df,
                "new": [
                    self.gn_df_two,
                    self.rd_df_two,
                    self.ye_df_two,
                    self.bl_df_two,
                    self.or_df_two,
                    "star",
                    self.gn_st_df_two,
                    self.rd_st_df_two,
                    self.ye_st_df_two,
                    self.bl_st_df_two,
                    self.or_st_df_two,
                ],
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
        avoid_purple = current_time() - self.purple_strum + 4 > STRUM_TIME
        if (
            self.pur_df > 100 or self.pur_df_two > 300
        ) and current_time() - self.purple_strum > STRUM_TIME + 10:
            self.purple_time.append(current_time() - self.purple_strum)
            self.purple_strum = current_time()
            self.notes.append("p")
        elif (
            self.gn_st_df > 1000
            or self.rd_st_df > 1000
            or self.ye_st_df > 1000
            or self.bl_st_df > 1000
            or self.or_st_df > 1000
        ):
            if (
                (self.gn_st_df > 1000 or self.gn_st_df_two > 1000)
                and current_time() - self.green_strum > STRUM_TIME + 2
                and avoid_purple
            ):
                self.green_time.append(current_time() - self.green_strum)
                self.green_strum = current_time()
                self.notes.append("a")
            if (
                (self.rd_st_df > 1000 or self.rd_st_df_two > 1000)
                and current_time() - self.red_strum > STRUM_TIME + 2
                and avoid_purple
            ):
                self.red_time.append(current_time() - self.red_strum)
                self.red_strum = current_time()
                self.notes.append("s")
            if (
                (self.ye_st_df > 1000 or self.ye_st_df_two > 1000)
                and current_time() - self.yellow_strum > STRUM_TIME + 2
                and avoid_purple
            ):
                self.yellow_time.append(current_time() - self.yellow_strum)
                self.yellow_strum = current_time()
                self.notes.append("d")
            # NOTE: Blue star is similar to regular blue. Higher number should avoid some issues with matching.
            if (
                (self.bl_st_df > 1000 or self.bl_st_df_two > 9000)
                and current_time() - self.blue_strum > STRUM_TIME + 2
                and avoid_purple
            ):
                self.blue_time.append(current_time() - self.blue_strum)
                self.blue_strum = current_time()
                self.notes.append("f")
            if (
                (self.or_st_df > 1000 or self.or_st_df_two > 1000)
                and current_time() - self.orange_strum > STRUM_TIME + 2
                and avoid_purple
            ):
                self.orange_time.append(current_time() - self.orange_strum)
                self.orange_strum = current_time()
                self.notes.append("g")
        else:
            if (
                ((self.gn_df > 1000 and self.gn_df_two > 1000) or self.gn_df_two > 100)
                and current_time() - self.green_strum > STRUM_TIME
                and avoid_purple
            ):
                self.green_time.append(current_time() - self.green_strum)
                self.green_strum = current_time()
                self.notes.append("a")
            if (
                ((self.rd_df > 1000 and self.rd_df_two > 1000) or self.rd_df_two > 0)
                and current_time() - self.red_strum > STRUM_TIME
                and avoid_purple
            ):
                self.red_time.append(current_time() - self.red_strum)
                self.red_strum = current_time()
                self.notes.append("s")
            if (
                ((self.ye_df > 1000 and self.ye_df_two > 1000) or self.ye_df_two > 0)
                and current_time() - self.yellow_strum > STRUM_TIME
                and avoid_purple
            ):
                self.yellow_time.append(current_time() - self.yellow_strum)
                self.yellow_strum = current_time()
                self.notes.append("d")
            if (
                ((self.bl_df > 1000 and self.bl_df_two > 1000) or self.bl_df_two > 0)
                and current_time() - self.blue_strum > STRUM_TIME
                and avoid_purple
            ):
                self.blue_time.append(current_time() - self.blue_strum)
                self.blue_strum = current_time()
                self.notes.append("f")
            if (
                ((self.or_df > 1000 and self.or_df_two > 1000) or self.or_df_two > 0)
                and current_time() - self.orange_strum > STRUM_TIME
                and avoid_purple
            ):
                self.orange_time.append(current_time() - self.orange_strum)
                self.orange_strum = current_time()
                self.notes.append("g")

    def run(self):
        self.capture()
        self.set_area()
        self.set_times()
        while self.program_running:
            while self.running:
                start = current_time()
                self.capture()
                # NOTE: dxcam will return None if the image it takes would be
                # the exact same image as the previous image.
                if self.img_check is None:
                    continue
                else:
                    self.notes = []
                    self.set_area()
                    self.background_subtraction()
                    self.save_image()
                    if (
                        self.pur_df > 100
                        or self.pur_df_two > 100
                        and current_time() - self.purple_strum > STRUM_TIME
                    ):
                        self.check_colors()

                    elif (
                        self.gn_df > 1000 or self.gn_st_df > 1000
                    ) and current_time() - self.green_strum > STRUM_TIME:
                        self.check_colors()

                    elif (
                        self.rd_df > 1000 or self.rd_st_df > 1000
                    ) and current_time() - self.red_strum > STRUM_TIME:
                        self.check_colors()

                    elif (
                        self.ye_df > 1000 or self.ye_st_df > 1000
                    ) and current_time() - self.yellow_strum > STRUM_TIME:
                        self.check_colors()

                    elif (
                        self.bl_df > 1000 or self.bl_st_df > 1000
                    ) and current_time() - self.blue_strum > STRUM_TIME:
                        self.check_colors()

                    elif (
                        self.or_df > 1000 or self.or_st_df > 1000
                    ) and current_time() - self.orange_strum > STRUM_TIME:
                        self.check_colors()

                    if self.notes:
                        self.release_all()
                        self.strum()

                try:
                    if 1000 / (current_time() - start) < 144:
                        print("FPS:", 1000 / (current_time() - start))
                except ZeroDivisionError:
                    pass

            time.sleep(0.01)


def current_time():
    return int(round(time.time() * 1000))


def on_press(key):
    if key == start_stop_key:
        if play_thread.running:
            play_thread.release_all()
            play_thread.release_all()
            play_thread.release_all()
            play_thread.stop_playing()
            key_press.tap(Key.enter)

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
            except Exception as e:
                print("There has been an error:", e)

            # NOTE: Only useful for saving images for debugging purposes.
            # Converts doubly-linked list to a list.
            save = list(play_thread.images)

            for x in save:
                cv2.rectangle(x["image"], (50, 10), (100, 20), (255, 0, 0), 1)
                cv2.rectangle(x["image"], (190, 10), (225, 20), (255, 0, 0), 1)

                cv2.rectangle(x["image"], (29, 55), (96, 59), (255, 0, 0), 1)
                cv2.rectangle(x["image"], (179, 55), (251, 59), (255, 0, 0), 1)
                cv2.rectangle(x["image"], (319, 55), (401, 59), (255, 0, 0), 1)
                cv2.rectangle(x["image"], (479, 55), (541, 59), (255, 0, 0), 1)
                cv2.rectangle(x["image"], (624, 55), (701, 59), (255, 0, 0), 1)

                cv2.rectangle(x["image"], (108, 47), (112, 54), (255, 0, 0), 1)
                cv2.rectangle(x["image"], (259, 47), (263, 54), (255, 0, 0), 1)
                cv2.rectangle(x["image"], (411, 47), (415, 54), (255, 0, 0), 1)
                cv2.rectangle(x["image"], (468, 47), (472, 54), (255, 0, 0), 1)
                cv2.rectangle(x["image"], (615, 47), (619, 54), (255, 0, 0), 1)

                cv2.imwrite(
                    "data/images/img_{}_g{}_r{}_y{}_b{}_o{}_p{}_gt{}_rt{}_yt{}"
                    "_bt{}_ot{}_{}_new{}"
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
                        x["new"],
                    ),
                    cv2.cvtColor(x["image"], cv2.COLOR_BGR2RGB),
                )
                y += 1
            print("Bot Stopped.")
        else:
            print("Bot Running...")
            play_thread.set_background()
            play_thread.release_all()
            ef.clear_file()
            print("Trash cleared.")
            play_thread.start_playing()
    elif key == stop_key:
        play_thread.release_all()
        play_thread.exit()
        cv2.destroyAllWindows()
        print("Exiting...")
        listener.stop()


if __name__ == "__main__":
    play_thread = PlayRedux()
    play_thread.start()
    with Listener(on_press=on_press) as listener:
        listener.join()
