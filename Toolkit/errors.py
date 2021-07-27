class OutOfService(Exception):
    def __init__(self,Note:str=""):
        pass
class InternalError(Exception):
    def __init__(self,Note:str=""):
        pass
class NothingFoundError(Exception):
    def __init__(self,Note:str=""):
        pass
class DummyError(Exception):
    def __init__(self,Note:str=""):
        pass