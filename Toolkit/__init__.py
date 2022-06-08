from ._glue import mTkt as tkt, Audio2Text
from ._collib import HEX, RGB, _colors as colors
from .image import IMG as imgU
from ._pionier import MultiImg, OneImg, SameImg, ImgObjRec

__TRACKING_ENABLED__ = True
__DEBUG_ENABLED__ = True
if __TRACKING_ENABLED__:
    if __DEBUG_ENABLED__:
        print(
            """
Tracking was enabled, it uses the following modules:
- opencv-python
- opencv-contrib-python
- mediapipe
- pyzbar
- pytesseract
- numpy
- imutils
"""
        )
    from . import tracking, audio, parse

    Tracking = tracking
AudioFormatting = audio.Format
AudioPlayer = audio.Player