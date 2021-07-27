from googletrans import Translator

translator = Translator()
class using:
    def translation_cut(Text:str):
        Text = str(Text)
        i = str(str(Text.replace("Translated(src=", "")))
        o, u, c, d, e = i.split(",")
        p = str(c.replace(" text=", ""))
        p = p.replace("% &%", ",")
        return p
    def detect_lng(Text:str):
        f = str(translator.detect(Text))
        c = f.replace("Detected(lang=", "")
        g = c.replace(")", "")
        r = g.replace(", confidence=", "==")
        i, u = r.split("==")
        return i
    def translate(Text:str, Dest:str, From:str="auto"):
        Text = str(str(Text).replace(",", "%&%"))
        if From == "auto": lng = using.detect_lng(Text)
        else:lng = From
        uncut = translator.translate(Text, src=lng, dest=Dest)
        resp = using.translation_cut(uncut)
        return resp
def Translate(Text:str, Dest:str, From:str='auto'):
    return using.translate(Text,Dest.lower(),From.lower())