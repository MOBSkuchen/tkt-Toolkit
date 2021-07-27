from .Base import *
class music:
    def search(term:str):
        A=ttapi.search_for_music(term)
        return A