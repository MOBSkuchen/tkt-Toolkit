import termcolor
import speech_recognition as sr
r = sr.Recognizer()
class using:
    def get_mics(comp:bool):
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            if comp ==True:FF = (f'Found microphone: ({name})[{index}]')
            else:FF = (index,name)
            yield FF
    def get_from_file(wav_file:str,msg_on:bool=True):
        if msg_on:print(termcolor.colored(f'Converting {wav_file} in to text.', 'yellow'))
        with sr.AudioFile(wav_file) as source:
            audio_text = r.listen(source)
            try:
                text = r.recognize_google(audio_text)
                return text
            except Exception as ex:
                b = ''
                if msg_on:b = f'Got an error ({ex}), please try again'
                return b
    def get_from_mic(msg_on:bool=True):
        global _end_spr_tkt_END
        try:
            if msg_on: print(termcolor.colored(f'Converting MIC audio to text.', 'yellow'))
            with sr.Microphone() as source:
                aud_text = r.listen(source)
                final_text = r.recognize_google(aud_text)
                b = final_text
        except Exception as ex:
            b = ''
            if msg_on: b = f'Got an error ({ex}), please try again'
        return b
class recon:
    def recon_from_mic(msg:bool=True):
        return using.get_from_mic(msg)
    def recon_from_file(file:str,msg:bool=True):
        return using.get_from_file(msg)
    def get_mics(detailed:bool=False):
        for E in using.get_mics(detailed):yield E