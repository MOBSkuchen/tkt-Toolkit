import time, socket, json, piexif.helper
from . import parse
import termcolor
import httpx
import speech_recognition as sr
from win32com.client import Dispatch
from googletrans import Translator

_r = sr.Recognizer()


class Audio2Text:
    """
    Requires Pyaudio that you have to install
    using 'pipwin install pyaudio'.
    Records or reads audio and transforms it to text.
    Can also list Microphones.
    """

    @staticmethod
    def get_mics():
        col = []
        for index, name in enumerate(sr.Microphone.list_microphone_names()): col.append((index, name))
        return col

    @staticmethod
    def get_from_file(wav_file: str, msg_on: bool = True):
        if msg_on: print(termcolor.colored(f'Converting {wav_file} in to text.', 'yellow'))
        with sr.AudioFile(wav_file) as source:
            audio_text = _r.listen(source)
            try:
                text = _r.recognize_google(audio_text)
                return text
            except Exception as ex:
                if msg_on: print(f'Got an error ({ex}), please try again')
                return None

    @staticmethod
    def get_from_mic(msg_on: bool = True):
        global _end_spr_tkt_END
        try:
            if msg_on: print(termcolor.colored(f'Converting MIC audio to text.', 'yellow'))
            with sr.Microphone() as source:
                aud_text = _r.listen(source)
                final_text = _r.recognize_google(aud_text)
                return final_text
        except Exception as ex:
            if msg_on:
                print(f'Got an error ({ex}), please try again')
            return None


class mTkt:
    def __init__(self):
        """
        The main function with all sorts of things.
        """
        pass

    def __str__(self):
        return "Greetings!"

    @staticmethod
    def Translate(text: str, dest, src: str = 'auto'):
        """
        Translates text into another language using
        the googletrans package.
        :param Text:
        The Text that is going to be translated.
        :param Dest:
        The destination language for the text.
        :param From:
        The language of the given text.
        Use 'auto' here to automatically recognize
        the language.
        :return:
        Returns 2 values:
        1 : Translated Text
        2 : Tuple:
            1 : Text Language
            2 : Translated Language
            3 : Text
        """
        translator = Translator()
        obj = translator.translate(text, dest, src)
        src_lng = obj.src
        dest_lng = obj.dest
        dest = obj.text
        src = text
        return dest, (src_lng, dest_lng, src)

    @staticmethod
    def del_all(dir: str):
        """
        Clears out all of the files in the folder and
        then delets them.
        :param dir:
        The target folder.
        :return:
        None
        """
        parse.using.del_files(dir, False)
        parse.using.del_folders(dir, False)
        return None

    @staticmethod
    def getip():
        """
        Gets the users IP using the python
        built-in socket package.
        """
        return socket.gethostbyname(socket.gethostname())

    @staticmethod
    def weather(city: str, key: str):
        """
        Gets the weather from 'openweathermap.org',
        uses the standard free to use api.
        :param city:
        The city that the weather is going
        to be from.
        :param key:
        The key for 'openweathermap.org'.
        :return:
        """
        api_key = key
        uul = ("https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + api_key)
        url = uul
        response = httpx.get(url).text
        data = json.loads(response)
        return data

    @staticmethod
    def do_for(n_seconds: int, func):
        """
        Runs the given function for the given amount of seconds.
        :param n_seconds:
        The seconds the function is run for.
        :param func:
        The function that is ran.
        :return:
        None
        """
        t_end = time.time() + n_seconds
        while time.time() < t_end: func()
        return None

    @staticmethod
    def read_metadata(filename: str):
        """
        Reads the metadata from an image file.
        :param filename:
        The file to be read.
        :return:
        The metadata in json format.
        """
        exif_dict = piexif.load(filename)
        user_comment = piexif.helper.UserComment.load(exif_dict["Exif"][piexif.ExifIFD.UserComment])
        return json.loads(user_comment)

    @staticmethod
    def write_metadata(filename: str, json_data: dict):
        """
        Writes metadata into an image file.
        :param filename:
        The image to be used.
        :param json_data:
        The data to be written.
        :return:
        None
        """
        exif_dict = piexif.load(filename)
        exif_dict["Exif"][piexif.ExifIFD.UserComment] = piexif.helper.UserComment.dump(
            json.dumps(json_data),
            encoding="unicode"
        )
        piexif.insert(
            piexif.dump(exif_dict),
            filename
        )
        return None

    @staticmethod
    def create_shortcut(target: str, output: str):
        """
        Creates a shortcut on windows.
        :param target:
        The file that the shortcut accesses.
        :param output:
        The output file.
        :return:
        None
        """
        path = output
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = target
        shortcut.WorkingDirectory = target
        shortcut.IconLocation = target
        shortcut.save()
        return None
