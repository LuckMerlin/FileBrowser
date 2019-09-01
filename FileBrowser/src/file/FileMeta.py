'''
Created on 2019年8月22日

@author: Administrator
'''
import os
import filetype
from filetype import Type 
import hashlib

class FileMeta:
    __readable=False
    
    __writeable=False
        
    __exist=False
    
    __file=False
            
    __size=-1
    
    __path=None
    
    __type=None
    
    __lastModifyTime=-1
    
    __md5=None
    
    def __init__(self,path):
        self.__path=path
        self.__size=self.getSize(path)
        self.__type=self.getFileType(path)
        self.__readable=self.isReadable(path)
        self.__writeable=self.isWriteable(path)
        self.__exist=self.isExist(path)
        self.__lastModifyTime=self.getLastModifyTime(path)
        self.__md5=self.getMd5(path)
        
    def getPath(self):
        return self.__path
        
    def isWriteable(self,path=None):
        return self.__writeable if  path == None else os.access(path,os.W_OK)
    
    def isReadable(self,path=None):
        return self.__readable if  path == None else os.access(path,os.R_OK)
                
    def isExist(self,path=None):
        return self.__exist if  path == None else os.access(path,os.F_OK)
        
    def getSize(self,path=None):
        return self.__size if path == None else (os.path.getsize(path) if self.isExist(path) else None)     
    
    def isFile(self,path=None):
        return self.__file if path == None else (os.path.isfile(path) if self.isExist(path) else False)   
      
    def getExtension(self,path=None,default=None):
        value=os.path.splitext(path) if None!=path else None;
        return value[1] if None!=value and len(value)==2 else default
        
    def getMime(self,path=None):
        value= self.__type if path ==None else self.getFileType(path)
        return value.__mime if None ==value else None
            
    def getLastModifyTime(self,path=None,default=0):
        return self.__lastModifyTime if path == None else (os.path.getmtime(path) if self.isExist(path) else default)
        
    def getName(self,extension=True,path=None,default=None):
        path=self.__path if None==path else path
        value=os.path.split(path) if None!=path else None
        extensionValue=value[1] if None!=value and len(value)==2 else None 
        if None != extensionValue : 
            mat=None if extension else self.getExtension(path,None)
            return extensionValue.replace(mat,"") if None!=mat else extensionValue
        return default
        
    def getParent(self,path=None,default=None):
            path=self.path if path==None else path
            value=os.path.split(path) if None ==path else None
            return value[0] if None!=value and len(value)==2 else default        
            
    def getMd5(self,path=None,default=None):
        if None ==path:
            return self.__md5
        elif self.isExist(path):
            file = open(path,'rb')
            md5 = hashlib.md5(file.read()).hexdigest()
            file.close()
            return md5 if None!=md5 else default
                
    def getFileType(self,path=None):
        if path==None:
            return self.__type
        elif (self.isExist(path) and self.isReadable(path)):
            if self.isFile(path):
                value=filetype.guess(path)
                return value if value !=None else Type(None,filetype.guess_extension(path))
            
            
            
