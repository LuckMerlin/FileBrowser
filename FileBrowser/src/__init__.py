# from os import stat
# ##from browser import FileParser
from file import FileMeta
from file import FileMonitor
#from media import MediaMeta
# #from browser.file import FileMonitor
import os
# import shutil
# import zipfile
# import platform
# import sys
# import datetime  
##import threading
#     print("\n".join(['%s:%s' %  item for item in ddd.__dict__.items()]))
if __name__=="__main__":
    monitor=FileMonitor.FileMonitor()
    monitor.startObserver("/volume1/Public");  
#     monitor.startObserver("/home/LuckMerlin/Desktop/Test");  
    # print(FileMeta.FileMeta("/dd/2.jpg").getName(True))
#     print(FileMeta.FileMeta("./2.jpg").getMd5())