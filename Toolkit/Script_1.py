from .Base import *
class userData:
    def getUserObject(username:str):
        c=dict(ttapi.get_user("Bellapoarch"))
        return c
    def getDesc(obj:dict):
        e = userData.getseoProps(obj).get("metaParams").get("description")
        return e
    def getKeywords(obj:dict):
        e=userData.getseoProps(obj).get("metaParams").get("keywords")
        for i in e.split(","):
            yield i
    def getName(obj:dict):
        e = userData.getseoProps(obj).get("metaParams").get("name")
        return e
    def getseoProps(obj: dict):
        return obj.get("seoProps")
    def getUniqueID(obj:dict):
        obj.get("uniqueId")
    def getItems(obj:dict):
        return str(obj.items())