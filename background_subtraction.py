import concurrent.futures
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
        print("BG loaded.")
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
        star_notes = [
            self.gn_st_df,
            self.rd_st_df,
            self.ye_st_df,
            self.bl_st_df,
            self.or_st_df,
        ]
        return star_notes

    def regular_notes(self, gn, rn, yn, bn, orn):
        self.gn_df = cv2.absdiff(self.gn_bg, gn)
        self.rd_df = cv2.absdiff(self.rd_bg, rn)
        self.ye_df = cv2.absdiff(self.ye_bg, yn)
        self.bl_df = cv2.absdiff(self.bl_bg, bn)
        self.or_df = cv2.absdiff(self.or_bg, orn)
        reg_notes = [self.gn_df, self.rd_df, self.ye_df, self.bl_df, self.or_df]
        return reg_notes

    def purple_note(self, pur):
        self.pur_df = cv2.absdiff(self.pur_bg, pur)
        return self.pur_df

    def run_subtraction_in_parallel(
        self, gs, rs, ys, bs, ors, gn, rn, yn, bn, orn, pur
    ):
        results = []
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures1 = executor.submit(self.regular_notes, gn, rn, yn, bn, orn)
            futures2 = executor.submit(self.star_notes, gs, rs, ys, bs, ors)
            futures3 = executor.submit(self.purple_note, pur)
            # print(futures1.result())
            results = futures1.result() + futures2.result() + futures3.result()
            print(results)
            return results


if __name__ == "__main__":
    pass
