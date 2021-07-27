__title__ = 'tkt-Toolkit'
__author__ = 'Suprime'
__license__ = 'MIT'
__copyright__ = 'Copyright 2020-2021 Suprime'
__version__ = '1.5.1'

__tkt_OUS_ex__ = True
__ext_TTA__ = False

import time,socket,json
from . import Script_1,Script_2,Base,Crypto,SpeechRecongition,texttospeech,translator,Youtube,Discord_framework,parse
from .errors import *

class TikTok:
    """
    Uses functionalities from the TikTokApi
    package and makes them more user friendly.
    Does only work if you set __ext_TTA__ = False
    """
    Music = Script_2.music
    User = Script_1.userData
    Base = Base

class SpeechRecognition:
    """
    Requires Pyaudio that you have to install
    using 'pipwin install pyaudio'.
    Records or reads audio and transforms it to text.
    Can also list Microphones.
    """
    def from_Microphone(show_msg: bool = True):
        return SpeechRecongition.recon.recon_from_mic(show_msg)
    def from_Wav_File(wav_file: str, show_msg: bool = True):
        open(wav_file)
        return SpeechRecongition.recon.recon_from_file(wav_file, show_msg)
    def list_Microphones(detailed: bool = True):
        for EE in SpeechRecongition.recon.get_mics(detailed): yield EE

class Info:
    def __version__(self=""):return __version__
    def __copyright__(self=""):return __copyright__
    def __license__(self=""):return __license__
    def __author__(self=""):return __author__

class Toolkit:
    class Crypto:
        """
        Uses the cryptography package to
        encrypt/decrypt 'Text' with 'Key'
        !! Does not work !!
        """
        def encrypt(Text:str,Key:str):
            raise OutOfService
            return Crypto.using.encrypt(Text.encode(),Key.encode())
        def decrypt(Text:str,Key:str):
            raise OutOfService
            return Crypto.using.decrypt(Text.encode(),Key.encode())

    def getip(S=""):
        """
        Gets the users IP using the python
        built-in socket package.
        """
        return socket.gethostbyname(socket.gethostname())
    def texttospeech(Content:str, Lang:str, Axc:str="com",using_dir:str=''):
        """
        Creates a file in the 'using_dir' and
        plays it.
        """
        texttospeech.tts(Content,Axc,Lang,using_dir)
    def translate(Text:str,Dest,From='auto'):
        """
        Translate 'Text' from 'From' to 'Dest',
        set 'Dest' to "auto" if you don't know
        the language.
        """
        return translator.Translate(Text,Dest,From)

    def weather(city:str, key:str):
        """
        Gets the weather from openweathermap.org,
        uses the standard free to use api.
        """
        api_key = key
        uul = ("https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + api_key)
        url = uul
        response = parse.x.get(url).text
        data = json.loads(response)
        return data

    def get_color(rgb: tuple = None, hex: str = None):
        """
        Gets the color-data of one 'hex'/'rgb' color
        """
        if rgb == None and hex == None:
            raise ValueError('Not enough values.')
        elif not rgb == None and not hex == None:
            raise ValueError('Too many values.')
        elif not rgb == None and hex == None:
            R = 1
        elif rgb == None and not hex == None:
            R = 2

        if R == 1:
            req = parse.Q.build_main + parse.Q.build_rgb + str(rgb)
        elif R == 2:
            req = parse.Q.build_main + parse.Q.build_hex + str(hex.replace('#', '', 1))
        resp = (parse.x.get(req).text)
        return parse.using.pull_values(resp)

    def calc(calc):
        exec(f'global __COMP_CALC_END__\n__COMP_CALC_END__=({calc})')
        return __COMP_CALC_END__
    def getip(S=""):
        """
        Gets the users IP using the python
        built-in socket package.
        """
        return socket.gethostbyname(socket.gethostname())

    def do_for(n_seconds: int, func):
        """
        Runs 'func' for 'n_seconds'
        """
        t_end = time.time() + n_seconds
        while time.time() < t_end: func()

    def is_URLsafe(string: str, allowSub: bool = False):
        """
        Checks if 'string' is URL-safe, enable
        'allowSub' to not affect "/" characters.
        """
        for i in parse.Q.urlSafeChars:
            if i in string: return False
        if not allowSub:
            if "/" in string: return False
        return True

    def make_URLsafe(string: str, allowSub: bool = False, replaceChar: str = "-"):
        """
        Replaces the not URL-safe charachters in 'string' with
        'replaceChar', enable 'allowSub' to not affect "/" characters.
        """
        e = string
        for i in parse.Q.urlSafeChars:
            erg = e.replace(i, replaceChar)
            e = erg
        if not allowSub: e = e.replace("/", replaceChar)
        return e
tkt=Toolkit