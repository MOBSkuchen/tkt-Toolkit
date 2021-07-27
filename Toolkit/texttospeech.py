from gtts import gTTS
import os
from playsound import playsound
def tts(text:str,axc:str,lng:str,u_dir:str):
    gTTS(text, "com" + axc, lng).save(f"{u_dir}/tmpSound.mp3")
    playsound(f"{u_dir}tmpSound.mp3")
    os.remove(f"{u_dir}tmpSound.mp3")