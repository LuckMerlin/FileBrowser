'''
Created on Sep 8, 2019

@author: luckmerlin
'''

from database.Database import Database
import os
from queue import Queue

class FileLoader(Database):
    queue=Queue(-1)
    
    def __init__(self):
        super().__init__()
        
    def loadFiles(self,path,iterate=False):
        exist=os.path.exists(path) if None!=path else None
        if None==exist or not exist:
            print("Can't not load files,Path not exist.",path)
            return False
        
        
        