from .errors import *

class RGB:
    def __init__(self,rgb:tuple):
        self._inner = rgb
        self._check_good()
        self._C = _colors()
    def _wrong(self):
        raise InvalidType('Tuple does not meet the rgb requirements')
    def _check_good(self):
        if not len(self._inner) == 3:self._wrong()
        r,g,b = self._inner
        if int(r) > 255:self._wrong()
        if int(g) > 255: self._wrong()
        if int(b) > 255: self._wrong()
    def __get__(self):
        return self._inner
    def __set__(self, value:tuple):
        self._inner = value
        self._check_good()
    def __hex__(self):
        return self.hex()
    def hex(self):
        c1, c2, c3 = self._C.rgb_to_hex(self._inner)
        return hex(int('0x' + c1 + c2 + c3,0))

class HEX:
    def __init__(self,hex:int):
        self._inner = int(hex,0)
        self._check_good()
        self._C = _colors()
    def _wrong(self):
        raise InvalidType('Int does not meet the hex requirements.')
    def _check_good(self):
        nh = str(hex(self._inner))
        if not len(nh) == 8:self._wrong()
    def __get__(self):
        return self._inner
    def __set__(self,value:int):
        self._inner = value
        self._check_good()
    def rgb(self):
        return self._C.hex_to_rgb(self._inner)
    def __rgb__(self):
        return self.rgb()

class _colors:
    """
    Color utilities for converting rgb->hex or hex->rgb.
    And for standard colors
    """
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    LIME = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    AQUA = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    SILVER = (192, 192, 192)
    GRAY = (128, 128, 128)
    MAROON = (128, 0, 0)
    OLIVE = (128, 128, 0)
    GREEN = (0, 128, 0)
    PURPLE = (128, 0, 128)
    TEAL = (0, 128, 128)
    NAVY = (0, 0, 128)
    def __init__(self):
        self._hc1 = {'A' : 10,'B' : 11,'C' : 12,'D' : 13,'E' : 14,'F' : 15}
        self._hc2 = {'10':'A','11':'B','12':'C','13':'D','14':'E','15':'F'}
    def standard(self,color:[RGB,HEX]):
        if type(color) == RGB:
            return color
        else:
            return color.rgb()
    def add_colors(self,color1:[RGB,HEX],color2:[RGB,HEX]):
        colorRGBA1,colorRGBA2 = self.standard(color1),self.standard(color2)
        #alpha = 255 - ((255 - colorRGBA1[3]) * (255 - colorRGBA2[3]) / 255)
        red = (colorRGBA1[0] * (255 - colorRGBA2[3]) + colorRGBA2[0] * colorRGBA2[3]) / 255
        green = (colorRGBA1[1] * (255 - colorRGBA2[3]) + colorRGBA2[1] * colorRGBA2[3]) / 255
        blue = (colorRGBA1[2] * (255 - colorRGBA2[3]) + colorRGBA2[2] * colorRGBA2[3]) / 255
        return (int(red), int(green), int(blue))
    def _split_hex(self,hex_:int):
        nh = str(hex(hex_))
        return nh[2],nh[3],nh[4],nh[5],nh[6],nh[7]
    def _pattern1(self,c1,c2):
        if not str(c1).isdigit():
            c1 = self._hc1.get(c1.upper())
        if not str(c2).isdigit():
            c2 = self._hc1.get(c2.upper())
        p = (int(c1) * 16) + int(c2)
        return p
    def _pattern2(self,n:int):
        if n == 0:return '00'
        x1,x2 = str(n / 16).split('.')
        if int(x1) > 9:c1 = self._hc2.get(str(x1))
        else:c1 = str(x1)
        if int(x2) == 0:c2 = '0'
        else:
            x2 = int(float('0.'+x2) * 16)
            if int(x2) > 9:c2 = self._hc2.get(str(x2))
            else:c2 = str(x2)
        return c1 + c2
    def hex_to_rgb(self,hex:int):
        A = self._split_hex(hex)
        r1, r2, g1, g2, b1, b2 = A
        return (self._pattern1(r1,r2),self._pattern1(g1,g2),self._pattern1(b1,b2))
    def rgb_to_hex(self,rgb:tuple):
        r,g,b = rgb[0],rgb[1],rgb[2]
        return (self._pattern2(r), self._pattern2(g), self._pattern2(b))