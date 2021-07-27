from pytube import Playlist as ytPl, YouTube as yt
from errors import *
from youtubesearchpython import Search
class Youtube:
    def getPlaylistInfo(playlistUrl:str):
        obj=ytPl(playlistUrl)
        OBJ={"playlist_ID":obj.playlist_id,"playlist_title":obj.title,"playlist_url":obj.playlist_url,"playlist_owner_id":obj.owner_id,"playlist_owner":obj.owner,"playlist_owner_url":obj.owner_url,"sidebar_info":obj.sidebar_info,"playlist_length":obj.length,"playlist_views":obj.views,"playlist_videos":obj.videos,"playlist_video_urls":obj.video_urls,"playlist_last_updated":obj.last_updated,"playlist_initial_data":obj.initial_data,"playlist_html":obj.html}
        return OBJ
    def downloadVideo(videoUrl:str, mode="video_highest_resolution", output_path=""):
        tt=yt(videoUrl)
        if mode=="video_highest_resolution": tt.streams.get_highest_resolution().download(output_path)
        elif mode=="video_lowest_resolution": tt.streams.get_lowest_resolution(output_path)
        elif mode=="audio_only": tt.streams.get_audio_only().download(output_path)
        else: raise Exception("Unknown mode: "+mode)
    def getVideoInfo(videoUrl:str):
        obj=yt(videoUrl)
        return obj.vid_info
    def search(term:str,limit:int=0):
        allSearch = (Search(term, limit=limit))
        turn = dict(allSearch.result()).get('result')
        if not str(turn) == "{'result': []}":return turn
        else:raise NothingFoundError('Found no YouTube video for term : ' + term)