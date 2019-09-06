
import pymysql

class MySql:
    sqlConnect=None
     
    def selectDatabase(self,dbName):
        if None==dbName :
            print("Can't select database",dbName)
            return False #Interrupt later codes
        if self.isDatabaseSelected(dbName):#If already selected
            return False 
        if (None==self.sqlConnect or (not self.isDatabaseConnected())):
            print("Can't select database,Host not connect",dbName,self.sqlConnect)
            return False #Interrupt later codes
        print("Select database ",dbName)
        self.sqlConnect.select_db(dbName)
        return self.isDatabaseSelected(dbName)
    
    def commit(self):
        if None!=self.sqlConnect:
            return self.sqlConnect.commit()
        return False

    def selectDatabaseTableCursor(self,dbName,tableName):
        if None==dbName or None==tableName:
            print("Can't select database table.",dbName,tableName)
            return None
        if  (not self.isDatabaseSelected(dbName)) and (not self.selectDatabase(dbName)):
            print("Can't select database table.Failed select database.",dbName,tableName)
            return None
        if None==self.sqlConnect:
            print("Can't select database table.Invalid connect.",dbName,tableName)
            return None
        if not self.isExistTables(dbName,tableName):
            print("Can't select database table.Table not exist.",dbName,tableName)
            return None
        return self.sqlConnect.cursor()

    def isDatabaseSelected(self,dbName):
        if None==dbName:
            print("Can't know if database selected,Host not connected.",dbName)
            return False
        if not self.isDatabaseConnected():#Must not selected while not connected
            return False
        if None==self.sqlConnect:
            print("Can't not know if selected database,Invalid connect.",dbName,self.sqlConnect)
            return False
        cursor=self.sqlConnect.cursor()
        if None!=cursor:
            cursor.execute("select database()")
            result=cursor.fetchall()
            cursor.close() #Close cursor
            return self.__isContains(result,dbName) 
        return False;

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
            return False #Interrupt later codes
        cursor=self.sqlConnect.cursor() if None!=self.sqlConnect else None
        if None==cursor:
            print("Can't find database ",dbName,".cursor=",cursor)
            return False #Interrupt later codes
        result=cursor.execute("show databases")
        databases=cursor.fetchall() if None!=result else None
        cursor.close()#Close cursor
        return self.__isContains(databases,dbName)

    def dropDatabase(self,dbName):
        if not self.isDatabaseConnected():
            print("Can't drop database ",dbName,"Host not connected.")
            return False #Interrupt later codes   
        if None==dbName:
            print("Can't drop database.dbName=",dbName)
            return False #Interrupt later codes 
        if not self.isExistDatabase(dbName):
            print("Not need drop database ",dbName)
            return False #Interrupt later codes  
        cursor=self.sqlConnect.cursor() if None!=self.sqlConnect else None
        if None==cursor:
            print("Can't drop database ",dbName,"cursor=",cursor)
            return False #Interrupt later codes 
        print("Dropping database",dbName)
        cursor.execute("drop database "+dbName)
        self.sqlConnect.commit()
        print("Succeed drop database",dbName)
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
                return self.__isContains(tables,tabName)
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
            return False #Interrupt later codes
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
            return False #Interrupt later codes
        if (None==host or None==user or None==port or None==charset):
            print("Can't connect database host ",host,port,user,charset)
        print("Connecting database host ",host,port,"as user ",user,charset)
        try:
            self.sqlConnect=pymysql.connect(host=host,port=port,user=user,passwd=passwd,charset=charset)
            return None!=self.sqlConnect
        except Exception as e:
            print("Failed connect database host ",e)
        return False

    def disconnect(self):
        if None!=self.sqlConnect:
            print("Now close database.")
            self.sqlConnect.close()#Close cursorconnect
            self.sqlConnect=None   
            return True
        return False

    def __isContains(self,values,target):
        if (None!=target and None!=values): 
            for value in values:
                for child in value:
                    if (None!=child and child==target):
                        return True
        return False    
        
        

    def __del__(self):
        if self.isDatabaseConnected():#Try auto disconnect database while __del__
            self.disconnect()
            


