'''
Created on 2019年8月21日
@author: LuckMerlin
'''
from browser import BaseFile
import os
# import filetype
# from filetype import Type 

class FileParser(BaseFile.BaseFile):
    def __init__(self):
            pass    
    
    def getDirectoryFiles(self,path=None):
        return os.listdir(path) if (path != None and os.path.exists(path) and os.access(path,os.R_OK) and os.path.isdir(path)) else [path]
        
        
#     def getFileType(self,path=None):
#         if path!=None and os.access(path,os.R_OK):
#             if os.path.isfile(path):
#                 value=filetype.guess(path)
#                 return value if value !=None else Type(None,filetype.guess_extension(path))


