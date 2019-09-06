
from database.MySql import MySql

class Database(MySql):
    DATABASE_NAME="browder"
    TABLE_NAME="files"
    #Columns define
    PATH="path"
    MD5="md5"
    INSERT_TIME="insertTime"
    SIZE="size"
    MIME="mime"
    NOTE="note"

    def __init__(self):
        result=super().connectDatabase('localhost','root','luckmerlin')
        super().createTable(self.DATABASE_NAME,self.TABLE_NAME,True,#Create table if not exist
        "("+self.PATH+" varchar(200) primary key not null,"+
        self.MD5+" varchar(40),"+
        self.INSERT_TIME+" long,"+
        self.SIZE+" long,"+
        self.MIME+" varchar(10),"+
        self.NOTE+" varchar(10))")

    def insertPathOnDatabase(self,paths):
        succeed=-1
        if None==paths:
            print("Can't insert path on database,Paths is NONE.")
            return succeed
        length=len(paths) if isinstance(paths,tuple) else -1
        if (length<=0):
            print("Can't insert path on database,Paths must package in not empty tuple data type.",length,paths)
            return succeed
        cursor=super().selectDatabaseTableCursor(self.DATABASE_NAME,self.TABLE_NAME)
        if None==cursor:
            print("Can't insert path on database,Cursor is NONE.")
            return succeed
        print("Inserting path on database.",length)
        succeed=0 
        for child in paths:
            if None==child or not isinstance(child,dict):
                print("Skip insert path on database,Not package in dict type.",child)
                continue
            path=child[self.PATH] if self.PATH in child else None
            md5=child[self.MD5] if self.MD5 in child else None
            size=child[self.SIZE] if self.SIZE in child else None
            mime=child[self.MIME] if self.MIME in child else None
            insertTime=child[self.INSERT_TIME] if self.INSERT_TIME in child else None
            note=child[self.NOTE] if self.NOTE in child else None
            import time
            insertTime=int(time.time()*1000) if None==insertTime or insertTime<0 else insertTime
            note=note if None!=note else ""
            if (path==None or md5==None or size<-2 or mime==None) :#Chck necessary parm if exist    
                print("Skip insert path on database,Necessary parm not exist.",mime,size,md5,path,child)
                continue
            print(mime,size,md5,path,insertTime,child)
            if cursor.execute("insert into "+self.TABLE_NAME+"("+
                self.PATH+","+
                self.MD5+","+
                self.SIZE+","+
                self.MIME+","+
                self.INSERT_TIME+","+
                self.NOTE+") values ("+
                "'"+path+"',"+md5+","+str(size)+","+mime+","+str(insertTime)+","+note
                +")"):
                succeed+=1
                print("cha ru  cheng gong ",path)
            else:
                print("shibai ",path) 
        super().commit()
        cursor.close()
        print("Finish insert path on database.",succeed,length)
        return succeed
        
    def isPathExistOnDatabase(self,path):
        if (None==path) or (not super().isExistTables(self.DATABASE_NAME,self.TABLE_NAME)):#Not exist if none table
            return False
        cursor=super().selectDatabaseTableCursor(self.DATABASE_NAME,self.TABLE_NAME) if None!=path else None
        if None==cursor:
            print("Can' know if exist path in database,Cursor is NONE.",path)
            return False
        count=cursor.execute("select * from "+self.TABLE_NAME+" where "+self.PATH+"="+"'"+path+"'")
        cursor.close()
        return count>0

    def deletePathFromDatabase(self,paths,log=False):
        deleted=-1 #Reset result
        paths=(paths,) if isinstance(paths,str) else paths 
        length=len(paths) if None!=paths and isinstance(paths,tuple) else -1
        if length<=0: 
            print("Not need delete path from database,path list is EMPTY.",length)
            return deleted
        cursor=super().selectDatabaseTableCursor(self.DATABASE_NAME,self.TABLE_NAME)
        if None==cursor:
            print("Can't delete path from database,Cursor is NONE.",length)
            return deleted
        deleted=0 #Set zero
        for path in paths:
            path=path[self.PATH] if None!=path and isinstance(path,dict) and  (self.PATH in path) else path
            child=((getattr(path,self.PATH)if hasattr(path,self.PATH) else None) if not isinstance(path,str) else path) if None!=path else None 
            if None==child:
                print("SKip delete path from database,NONE path attr exist.",path)
                continue #Continue next
            if cursor.execute("delete from "+self.TABLE_NAME+" where "+self.PATH+"='"+child+"'"):
                deleted+=1
                print(path,deleted)
                if log:
                    print("Delete path from database.",child)
        if log:
            print("Finish delete path(s) from database.",deleted,length)
        super().commit()
        cursor.close()
        return deleted

    def movePathOnDatabase(self,src,path):
        pass







