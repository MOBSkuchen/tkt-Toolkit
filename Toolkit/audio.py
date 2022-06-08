from pydub import AudioSegment
from .errors import *
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

class Player:
    def __init__(self):
        """
        Uses pygame to mainly play music.
        All functionalities should be self explaining.
        """
        global pygame
        import pygame
        pygame.init()
        pygame.mixer.init()
        self._music = pygame.mixer.music
        self._loaded_file = None
    def play(self,file:str,*,auto_format:bool=True,loops:int=0,start:float=0.0,fade:int=0):
        self.loadIn(file,auto_format)
        self._music.play(loops,start,fade)
        self.volume(0.5)
    def rewind(self):
        self._music.rewind()
    def stop(self):
        self._music.stop()
    def loadIn(self,file:str,auto_format):
        self._loaded_file = file
        if auto_format:
            nfn, t = (str(self._loaded_file).split('.', self._loaded_file.count('.')))
            f = Format(self._loaded_file)
            f.export(nfn + ".mp3")
            self._loaded_file = nfn + ".mp3"
        try:
            self._music.load(self._loaded_file)
        except pygame.error:
            raise FormatError("The Format of the File must be 'mp3'. Use 'auto_format' to automatically make it an 'mp3' file.")
    def volume(self,vol:float):
        self._music.set_volume(vol)
    def get_pos(self):
        return int(self._music.get_pos())
    def pause(self):
        self._music.pause()
    def fade(self,fade:int):
        self._music.fadeout(fade)
    def queueUp(self,file):
        self._music.queue(file)
    def loadOut(self):
        self._music.unload()
    def get_volume(self):
        return self._music.get_volume()
    def busy(self):
        return self._music.get_busy()
    def set_volume(self,volume:int):
        """
        :param volume: Milliseconds
        """
        self._music.set_volume(volume)
    def set_pos(self,pos:float):
        self._music.set_pos(int(str(pos)))
    def resume(self):
        self._music.unpause()
    def _collect(self):
        return {
            'volume' : self.get_volume(),
            'file' : self._loaded_file,
            'position' : self.get_pos()
        }
    def __str__(self):
        return str(self._collect())
    def __len__(self):
        return int(self.get_pos())

class Format:
    def __init__(self,file:str,*,format:str=None):
        """
        Mainly formats audio, using AudioSegment from pydub.
        :param file:
        This is were the Audio is taken from
        :param format:
        The format that the file should be in, leave blank
        if the requested format is the same as the existing
        format.
        """
        self._file = file
        self._audio = AudioSegment.from_file(file, format=format)
    def export(self,filename:str,*,format:str="mp3"):
        self._audio.export(filename,format)
    def reverse(self):
        self._audio.reverse()
    def empty(self):
        self._audio.empty()
    def load_file(self,file:str,*,format:str=None):
        self._file = file
        self._audio = AudioSegment.from_file(file, format=format)
    def __str__(self):
        return str(self._file)
    def __len__(self):
        return len(self.__str__())