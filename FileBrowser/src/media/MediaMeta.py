'''
Created on 2019年8月28日

@author: Administrator
'''
from pymediainfo import MediaInfo
import os

class MediaMeta:
    __path=None
    
    def __init__(self,path):
        self.__path=path
              
    def getPath(self):
        return self.__path
    
    def getMimeTye(self,path=None):
        path=self.__path if None == path else path
        if os.path.exists(path) and MediaInfo.can_parse(path):
            pass
#             MediaInfo.parse(filename, library_file, cover_data, encoding_errors, parse_speed, text, full, legacy_stream_display)