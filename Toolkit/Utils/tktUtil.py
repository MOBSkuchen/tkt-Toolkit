import multiprocessing,time,socket
from dataclasses import dataclass

class using:
    def create_process(target,args):
        p = multiprocessing.Process(target=target,args=args)
        return p
    def start_process(Process):
        global _mp_tkt_process
        Process.start()
        _mp_tkt_process=Process
# Q is the class for storing the variables used
class Q:
    urlSafeChars=".","\\","(",")","{","[","|","]","}","^",">","<"
class util:
    def calc(calc):
        exec(f'global __COMP_CALC_END__\n__COMP_CALC_END__=({calc})')
        return __COMP_CALC_END__
    def getip(S=""):
        return socket.gethostbyname(socket.gethostname())
    def do_for(n_seconds:int,func):
        t_end = time.time() + n_seconds
        while time.time() < t_end:func()
    def is_URLsafe(string:str,allowSub:bool=False):
        for i in Q.urlSafeChars:
            if i in string:return False
        if not allowSub:
            if "/" in string:return False
        return True
    def make_URLsafe(string:str,allowSub:bool=False,replaceChar:str="-"):
        e=string
        for i in Q.urlSafeChars:
            erg=e.replace(i, replaceChar)
            e=erg
        if not allowSub:e=e.replace("/",replaceChar)
        return e
    class Processing:
        @dataclass
        class tkt_process:
            process_object: multiprocessing.Process
            timeout: int
        def start(target, args=("",)):
            P = using.create_process(target, args)
            using.start_process(P)
        def close(S=""):
            _mp_tkt_process.join()