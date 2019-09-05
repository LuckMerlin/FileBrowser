
import pymysql

class MySql:
    sqlConnect=None

    def __init__(self):
        result=self.connectDatabase('localhost','root','luckmerlin')
        print(" open database.",result)
    
    def insertOnDatabase(self,path):
        if None==path or None==self.sqlConnect:
            print("Can't insert path into database.",self.sqlConnect,path)
        database=self.createTable("files","ddd",True,"(id varchar(10),name varchar(10))")
        print(str(database))
        #print(str(cursor.execute("show databases")))
        pass

    def deleteOnDatabase(OnDatabaseself,path):
        pass

    def moveOnDatabase(self,src,path):
        pass
    

    def createDatabase(self,dbName,recreate=False):
     if not self.isDatabaseConnected():
         print("Can't create database ",dbName,"Host not connected.")
         return False #Interrupt later codes
     if None==dbName or None==self.sqlConnect:
            print("Can't create database.dbName=",dbName,self.sqlConnect)
            return #Interrupt later codes
     database=self.isExistDatabase(dbName)
     if database and (not recreate):#If already exist this name database
        return False #Interrupt later codes
     if database and (not self.dropDatabase(dbName)):
        print("Can't create database ",dbName," Failed drop existed.",database)
        return False #Interrupt later codes
     print("Creating database "+dbName)   
     cursor=self.sqlConnect.cursor()
     return self.isExistDatabase(dbName) if cursor.execute("create database "+dbName) else False
    

    def isExistDatabase(self,dbName=None):
        if not self.isDatabaseConnected():
            print("Can't know if exise database ",dbName,"Host not connected.")
        return False #Interrupt later codes
        if None==dbName:
            print("Can't find database.dbName=",dbName)
            return
        cursor=self.sqlConnect.cursor() if None!=self.sqlConnect else None
        if None==cursor:
            print("Can't find database ",dbName,".cursor=",cursor)
            return
        result=cursor.execute("show databases")
        databases=cursor.fetchall() if None!=result else None
        cursor.close()#Close cursor
        for child in databases:#Find target database
            for name in child:
                if None!=name and name==dbName:
                    return True
        return False

    def dropDatabase(self,dbName):
        if not self.isDatabaseConnected():
            print("Can't drop database ",dbName,"Host not connected.")
            return False #Interrupt later codes   
        if None==dbName:
            print("Can't drop database.dbName=",dbName)
            return
        cursor=self.sqlConnect.cursor() if None!=self.sqlConnect else None
        if None==cursor:
            print("Can't drop database ",dbName,"cursor=",cursor)
            return
        print("Dropping database",dbName)
        cursor.execute("drop database "+dbName)
        self.sqlConnect.commit()
        cursor.close()#Close cursor
        return not self.isExistDatabase(dbName)
    
    def isExistTables(self,dbName,tabName):
        if not self.isDatabaseConnected():
            print("Can't know if exist table ",tabName,"Host not connected.")
            return False #Interrupt later codes   
        if self.isExistDatabase(dbName):
            self.sqlConnect.select_db(dbName)
            cursor=self.getCursor()
            exist=False
            if None!=cursor:
                cursor.execute("show tables")
                tables=cursor.fetchall()
                cursor.close()   
                for table in tables:
                    for child in table:
                        if None!=child and child==tabName:
                            return True
        return False
    
    def dropTable(self,dbName,tabName):
        if not self.isDatabaseConnected():
            print("Can't drop table ",dbName,"Host not connected.")
            return False #Interrupt later codes   
        if (self.isExistTables(dbName,tabName) if None!=dbName and None!=tabName else False):
            self.sqlConnect.select_db(dbName)
            cursor=self.getCursor()
            if None!=cursor:
                print("Deleting database table ",tabName,dbName)
                cursor.execute("drop table "+tabName)
                cursor.close()#Close cursor
                return not self.isExistTables(dbName,tabName)
        return False        


    def createTable(self,dbName,tabName,recreate=False,args=None):
        if not self.isDatabaseConnected():
            print("Can't create table ",tabName,"Host not connected.")
            return False #Interrupt later codes   
        if None==args or None==dbName or None==tabName:
            print("Can't create database table ",tabName,dbName,args)
            return #Interrupt later codes
        if self.isExistDatabase(dbName) or self.createDatabase(dbName,False):
            exist=self.isExistTables(dbName,tabName) 
            if exist and (not recreate) :
                #print()
                return False
            if exist and not (self.dropTable(dbName,tabName)):
                print("Can't create database table ",tabName,"Delete exist failed.")
                return False #Interrupt later codes
            cursor=self.getCursor()
            if None!=cursor:
                print("Creating database table ",tabName,"within",dbName)
                cursor.execute('create table '+tabName+' '+args)
                cursor.close() #Close cursor
                return True
        return False
    

    def getCursor(self):
        if None==self.sqlConnect:
            print("Can't get database cursor.dbName=",dbName)
            return
        return self.sqlConnect.cursor() if None!=self.sqlConnect else None

    def isDatabaseConnected(self):
        return None!=self.sqlConnect

    def connectDatabase(self,host=None,user=None,passwd=None,port=3306,charset="utf8"):
        if self.isDatabaseConnected():
            print("Not need connect database again which already connected.")
            return #Interrupt later codes
        if (None==host or None==user or None==port or None==charset):
            print("Can't connect database host ",host,port,user,charset)
        print("Connecting database host ",host,port,"as user ",user,charset)
       # try:
            # print("HDEEEEEEE",host,user,passwd,charset,port)
            #pymysql.con
        self.sqlConnect=pymysql.connect(host,user,passwd,charset,port)
        return None!=self.sqlConnect
        #except Exception as e:
        #    print(e)
         #   print("Failed to connect database host ",host,port,user)
        # return False   

    def disconnect(self):
        if None!=self.sqlConnect:
            print("Now close database.")
            self.sqlConnect.close()#Close cursorconnect
            self.sqlConnect=None   
            return True
        return False

    def __del__(self):
        if self.isDatabaseConnected():#Try auto disconnect database while __del__
            self.disconnect()
            


