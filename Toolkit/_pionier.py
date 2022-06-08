import cv2, random
from .parse import MultiImg, SameImg, OneImg
from typing import Union


class ImgObjRec:
    def __init__(self, img, bbox, update_img: Union[MultiImg, SameImg, OneImg]):
        self._img = img
        if type(update_img) == SameImg:
            self._update_img = self._img
        else:
            self._update_img = update_img
        self._bbox = bbox
        self._tracker = cv2.TrackerKCF_create()
        self._tracker_init()
        self._tracker_ground_test()

    def _tracker_init(self):
        self._tracker.init(self._img, self._bbox)

    def _tracker_ground_test(self):
        for img in self._update_img:
            suc, bbox = self._tracker.update(img)
            if suc:
                if bbox == self._bbox:
                    print('BBOX FOUND')
                else:
                    print('BBOX NOT FOUND')

    def update(self, img):
        result = self._tracker.update(img)
        return result


class BBOX:
    def __init__(self, bbox: tuple):
        self._bbox = bbox
        self._x, self._y, self._w, self._h = self._bbox
        self._calc_center()
        self._quadwise()
        self._bigger()

    def _quadwise(self):
        """
        |-------------------|
        |    q1   |  q2     |
        |         |         |
        |-------------------|
        |   q3    |   q4    |
        |         |         |
        |-------------------|
        """
        self._q1 = (self._x, self._y, int(self._w / 2), int(self._h / 2))
        self._q2 = (self._mid_x, self._y, int(self._w / 2), int(self._h / 2))
        self._q3 = (self._x, self._mid_y, int(self._w / 2), int(self._h / 2))
        self._q4 = (self._mid_x, self._mid_y, int(self._w / 2), int(self._h / 2))
        self._quad = [self._q1, self._q2, self._q3, self._q4]

    def _bigger(self):
        """
        |----|-------------------|
        |    |                   |
        |    |-------------------|
        |    |         |         |
        |    |         |         |
        |    |-------------------|
        |    |         |         |
        |    |         |         |
        |----|-------------------|
        """
        self._s1 = (self._x - random.randint(20, 40), self._y - random.randint(10, 30), self._w, self._h)
        self._s2 = (self._x, self._y, self._w + random.randint(20, 45), self._h + random.randint(10, 30))
        self._rand = [self._s1, self._s2]

    def _calc_center(self):
        self._mid_x = int(self._w / 2) + self._x
        self._mid_y = int(self._h / 2) + self._y
        self._center = (self._mid_x, self._mid_y)

    @staticmethod
    def draw(img, bbox: tuple, color: tuple = (0, 255, 0)):
        x, y, w, h = bbox
        return cv2.rectangle(img, (x, y), ((x + w), (y + h)), color, 3)

    def __str__(self):
        return str(self._bbox)


class ObjectronCollected:
    def __init__(self, collected: list):
        self._col = collected
        if self._check_empty(): self._col = self._gen_make(len(self._col))

    def _gen_make(self, leng: int):
        g = []
        for i in range(leng):
            g.append(BBOX((0, 0, 0, 0)))
        return g

    def _check_empty(self):
        for i in self._col:
            suc, bbox, point = i
            if suc:
                return False
        return True

    def draw_all(self, img, color: tuple = (0, 255, 0)):
        for box in self._col: img = box.draw(img, box._bbox, color)
        return img

    def __iter__(self):
        for box in self._col: yield box


class Objectron:
    def __init__(self, bbox: BBOX, img, *, pionier=False):
        self._img = img
        self._bbox = bbox
        self._center = self._bbox._center
        self._use_new = pionier
        if self._use_new:
            self._quads = self._bbox._quad
            self._rands = self._bbox._rand
            self._rand_middle_offset = self._make_middle_from_sups(self._rands)
            self._quad_middle_offset = self._make_middle_from_sups(self._quads)
            self._multi_tracker_setup()
        self._tracker = self._tracker_setup(self._img, self._bbox._bbox)

    def _get_offset(self, c1: int, c2: int):
        if c1 > c2:
            c = c1 - c2
        else:
            c = c2 - c1
        return c

    def _make_middle_from_sups(self, report: list):
        center = self._center
        end = []
        for i in report:
            x, y, w, h = i
            ox, oy = (self._get_offset(x, center[0]), self._get_offset(y, center[1]))
            new = (ox, oy)
            end.append(new)
        return end

    def _multi_tracker_setup(self):
        f = []
        for box in self._quads:
            f.append(self._tracker_setup(self._img, box))
        for box in self._rands:
            f.append(self._tracker_setup(self._img, box))
        self._multi_trackers = f

    def _tracker_setup(self, img, bbox: tuple):
        tracker = cv2.TrackerKCF_create()
        tracker.init(img, bbox)
        return tracker

    def _raw_track(self, img):
        report = []
        if self._use_new:
            if self._multi_trackers == []:
                return []
            for tracker in self._multi_trackers:
                result = tracker.update(img)
                report.append(result)
        result = self._tracker.update(img)
        report.append(result)
        return report

    def _resolve_raw_tracking(self, report: list):
        if report == []:
            return ObjectronCollected([False, (0, 0), (0, 0)])
        if self._use_new:
            end = []
            points = self._reslove_middle_offset(report)
            c = -1
            for i in report:
                c += 1
                suc, bbox = i
                v = suc, bbox, points[c]
                end.append(v)
        return ObjectronCollected(end)

    def _reslove_middle_offset(self, report: list):
        if self._rand_middle_offset == None or self._quad_middle_offset == None:
            return []
        combo = self._quad_middle_offset + self._rand_middle_offset
        c = -1
        points = []
        for ent in report:
            try:
                c += 1
                _, ent = ent
                f = combo[c]
                x, y, w, h = ent
                new = (x + f[0], y + f[1])
                points.append(new)
            except IndexError:
                pass
        return points

    def track(self, img):
        return self._resolve_raw_tracking(self._raw_track(img))
