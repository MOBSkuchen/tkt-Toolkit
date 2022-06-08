import cv2
import numpy as np
from PIL import Image


class IMG:
    def __init__(self, img, PIL=False):
        """
        Various different image utility functions for
        image manipulations.
        :param img:
        Opencv-Python image or pillow image
        :param PIL:
        If image is pillow or not
        """
        if PIL:
            self._img = self._pil_2_cv2(img)
            self._img_pil = img
        else:
            self._img = img
            self._img_pil = self._cv2_2_pil(self._img)

    def from_file(self, file: str):
        img = cv2.imread(file)
        self.change(img)

    def grab(self, *, PIL: bool = False):
        if PIL:
            return self._img_pil
        return self._img

    def gamma(self, gamma=1.0):
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
        return cv2.LUT(self._img, table)

    def blur(self, *, ks=(10, 10)):
        # (10,10) is enough for a light blur
        # (30,30) is a strong blur
        return cv2.blur(self._img, ks)

    def show(self, *, self_end=True):
        cv2.imshow(f"Image View", self._img)
        if self_end: cv2.waitKey(0)

    def remove_noise(self, references: list[np.ndarray] = None):
        if references is None:
            references = []
        references.append(self._img)
        index = len(references) - 1
        return cv2.fastNlMeansDenoisingMulti(references, index, 3, None, 4, 7, 21)

    def change(self, img, *, PIL=False):
        if PIL:
            self._img = self._pil_2_cv2(img)
            self._img_pil = img
        else:
            self._img = img
            self._img_pil = self._cv2_2_pil(self._img)

    def _pil_2_cv2(self, img):
        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    def _cv2_2_pil(self, img):
        return Image.fromarray(img)
