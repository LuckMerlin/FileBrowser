
'''
Created on Sep 3, 2019

@author: luckmerlin
'''
import pyinotify
from file.FileLoader import FileLoader
import os

class FileMonitor(FileLoader):  
    class OnFileModify(pyinotify.ProcessEvent):
            EVENT_DELETE,EVENT_LOAD,EVENT_MOVE,EVENT_MOVE_CHILD=2017,2018,2019,2020
            
            def process_default(self,event):
                file=event.pathname if event!=None else None
                if None==file:
                    print("Invalid file modified ",event)
                    return
                #print(event)
                mask=event.mask
                if mask&pyinotify.IN_CLOSE_WRITE:
                    self.loadFile(file)
                    self.notifyFileModifyEvent(self.EVENT_LOAD,file)
                    # print("Modifyed&&&&&&&&&&&&&&7 ",file)
                elif mask&pyinotify.IN_CREATE:
                    self.loadFile(file)
                    self.notifyFileModifyEvent(self.EVENT_LOAD,file)
                    # print("Create&&&&&&&&&&&&&&7 ",file)
                elif mask&pyinotify.IN_MOVED_FROM or mask&pyinotify.IN_DELETE:
                    # print("dd ",mask&pyinotify.IN_MOVE_SELF,mask&pyinotify.IN_DELETE)
                    self.deleteFile(file)
                    if not event.dir:#If file or link,need to notify delete event 
                        self.notifyFileModifyEvent(self.EVENT_DELETE,file)
                    # print("Delete&&&&&&&&&&&&&&7 ",file)
                elif mask&pyinotify.IN_MOVED_TO:
                    srcPath=event.src_pathname if hasattr(event,"src_pathname") else None
                    self.moveFile(srcPath,file)
                    self.notifyFileModifyEvent(self.EVENT_MOVE,srcPath,file)
        
            def deleteFile(self,path):
                
                print("Delete ",path)
        
            def loadFile(self,path,oldPath=None):
                print("Load ",path)
            
            def moveFile(self,src,path):
                if  None!=path:
                    print("Move ",src,path)
                    if os.path.isfile(path) or os.path.islink(path): 
                        self.loadFile(path,src)#Must load file before exec delete for save performs
                        self.deleteFile(src)
                    elif os.path.isdir(path):
                        # for child in os.listdir(path):
                        print("xinzeng move ,",path)
                            
                    else:
                        print("Unknow type file moved ",src,path)        
        
            def notifyFileModifyEvent(self,eventId,src,target=None):
                pass    
    
    ####################################################
    def startObserver(self,path=None):
        if path==None:
            print("Can't start file modify observer is NONE",path)
            return None
        elif not os.path.exists(path):
            print("Can't start file modify observer,Path not exist ",path)
            return None
        print("Starting file modify observer ",path)
        mask =pyinotify.ALL_EVENTS ##pyinotify.IN_DELETE_SELF  IN_DELETE | pyinotify.IN_CREATE IN_ATTRIB IN_CLOSE_WRITE 
        manager=pyinotify.WatchManager()
        modifyHandler=FileMonitor.OnFileModify()
        notifier=pyinotify.Notifier(manager,modifyHandler) 
        manager.add_watch(path,mask,modifyHandler,True,True)
        print("Started file modify observer ",path)
        #test 
        print(super().isPathExistOnDatabase("/ddd"))
        super().loadFiles("/volume1/Public")
#         super().insertPathOnDatabase((
#             {"path":"/volume1/Public/Lin/test.php","md5":"wuyue","size":2019,"mime":"jpg"},
#             {"path":"/volume1/Public/Lin/test2.php","md5":"wuyue2","size":2020,"mime":"mp3"},
#             {"path":"/volume1/Public/Lin/pan.xml","md5":"wuyue3","size":2021,"mime":"xml"},
#             {"path":"/volume1/Public/Lin/pan.mp3","md5":"wuyue4","size":2022,"mime":"mp3"},
#             ))
#         super().deletePathFromDatabase(("/home/LuckMerlin/Desktop/Test",{"path":"/sdfdfa/sdfasd.lpi"}),True)
#         super().movePathOnDatabase(" /volume1/Public/Lin   ","/volume1/Public/Video",False)
        notifier.loop()

    def stopObserver(self):
        pass