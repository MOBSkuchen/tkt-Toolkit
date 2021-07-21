__title__ = 'tkt-Toolkit'
__author__ = 'Suprime'
__license__ = 'MIT'
__copyright__ = 'Copyright 2020-2021 Suprime'
__version__ = '1.4.0'

__tkt_OUS_ex__ = True
from termcolor import colored
from Toolkit.Utils import weather,texttospeech,Youtube,Crypto,tktUtil
from Toolkit.Utils.errors import InternalError,OutOfService
from Toolkit.Translation import translator
from Toolkit.Voice.SpeechRecongition import recon
from Toolkit.Tiktok import Script_2,Script_1,Base

class TikTok:
    """
    Uses functionalities from the TikTokApi
    package and makes them more user friendly.
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
        recon.recon_from_mic(show_msg)
    def from_Wav_File(wav_file: str, show_msg: bool = True):
        open(wav_file)
        recon.recon_from_file(wav_file, show_msg)
    def list_Microphones(detailed: bool = True):
        for EE in recon.get_mics(detailed): yield EE

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
    def getIP(self=''):
        """
        Gets the users IP using the python
        built-in socket package.
        """
        return getip.getip()
    def weather(city:str,open_weather_map_api_key:str):
        """
        Gets the weather from openweathermap.org,
        uses the standard free to use api.
        """
        weather.weather(city,open_weather_map_api_key)
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
        translator.Translate(Text,Dest,From)
tkt=Toolkit