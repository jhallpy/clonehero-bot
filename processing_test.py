import multiprocessing as mp
import cv2


class BackgroundSubtraction:
    def __init__(
        self,
        gns_bg,
        rds_bg,
        yes_bg,
        bls_bg,
        ors_bg,
        gn_bg,
        rd_bg,
        ye_bg,
        bl_bg,
        or_bg,
        pur_bg,
    ):
        self.gn_bg_st = gns_bg
        self.rd_bg_st = rds_bg
        self.ye_bg_st = yes_bg
        self.bl_bg_st = bls_bg
        self.or_bg_st = ors_bg

        self.gn_bg = gn_bg
        self.rd_bg = rd_bg
        self.ye_bg = ye_bg
        self.bl_bg = bl_bg
        self.or_bg = or_bg

        self.pur_bg = pur_bg

    def star_notes(self, gs, rs, ys, bs, ors):
        self.gn_st_df = cv2.absdiff(self.gn_bg_st, gs)
        self.rd_st_df = cv2.absdiff(self.rd_bg_st, rs)
        self.ye_st_df = cv2.absdiff(self.ye_bg_st, ys)
        self.bl_st_df = cv2.absdiff(self.bl_bg_st, bs)
        self.or_st_df = cv2.absdiff(self.or_bg_st, ors)

    def regular_notes(self, gn, rn, yn, bn, orn):
        self.gn_df = cv2.absdiff(self.gn_bg, gn)
        self.rd_df = cv2.absdiff(self.rd_bg, rn)
        self.ye_df = cv2.absdiff(self.ye_bg, yn)
        self.bl_df = cv2.absdiff(self.bl_bg, bn)
        self.or_df = cv2.absdiff(self.or_bg, orn)

    def purple_note(self, pur):
        self.pur_df = cv2.absdiff(self.pur_bg, pur)

    # def wrapper(function, value1, value2, value3, value4, value5):
    #     function(value1, value2, value3, value4, value5)

    def run_subtraction(self, gs, rs, ys, bs, ors, gn, rn, yn, bn, orn, pur):
        p1 = mp.Process(target=self.star_notes, args=(gs, rs, ys, bs, ors))
        p2 = mp.Process(target=self.regular_notes, args=(gn, rn, yn, bn, orn))
        p3 = mp.Process(target=self.purple_note, args=(pur))

        p1.start()
        p2.start()
        p3.start()

        p1.join()
        p2.join()
        p3.join()

    # def background_subtraction(self):
    # self.gn_df = cv2.absdiff(self.gn_bg, self.gn_chk)
    # self.rd_df = cv2.absdiff(self.rd_bg, self.rd_chk)
    # self.ye_df = cv2.absdiff(self.ye_bg, self.ye_chk)
    # self.bl_df = cv2.absdiff(self.bl_bg, self.bl_chk)
    # self.or_df = cv2.absdiff(self.or_bg, self.or_chk)

    # self.gn_st_df = cv2.absdiff(self.gn_bg_st, self.gn_chk_st)
    # self.rd_st_df = cv2.absdiff(self.rd_bg_st, self.rd_chk_st)
    # self.ye_st_df = cv2.absdiff(self.ye_bg_st, self.ye_chk_st)
    # self.bl_st_df = cv2.absdiff(self.bl_bg_st, self.bl_chk_st)
    # self.or_st_df = cv2.absdiff(self.or_bg_st, self.or_chk_st)

    # self.pur_df = cv2.absdiff(self.pur_bg, self.pur_chk)
