import multiprocessing,time,socket,httpx as x,json
from dataclasses import dataclass
class using:
    def create_process(target,args):
        p = multiprocessing.Process(target=target,args=args)
        return p
    def start_process(Process):
        global _mp_tkt_process
        Process.start()
        _mp_tkt_process=Process
    def pull_values(V:str):
        t,hex=V.split('{"value":"',1)
        hex,t=hex.split('","clean":"',1)
        t,rgb=V.split('"value":"rgb',1)
        rgb,t=rgb.split('"},"hsl":{"',1)
        t,hsl=V.split('"value":"hsl',1)
        hsl,t=hsl.split('"},"hsv":{"fraction"',1)
        t,hsv=V.split(',"value":"hsv',1)
        hsv,t=hsv.split('","h":',1)
        return (hex,rgb,hsl,hsv,V)
class Q:
    build_main = 'https://www.thecolorapi.com/'
    build_hex = 'id?hex='
    build_rgb = 'id?rgb=rgb'
    urlSafeChars=".","\\","(",")","{","[","|","]","}","^",">","<"