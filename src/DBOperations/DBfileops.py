import os
import pandas as pd
from sqlalchemy import create_engine
from src.customLogger import LoggingObject
from src.utils.config import read_params

class DBops:

    """This is a custom class for databse operations"""

    def __init__(self):

        self.logger = LoggingObject()
        self.config = read_params("params.yaml")

    def makeConnection(self,file,path,dbName):

        self.file=file
        self.path=os.path.join(path,dbName)

        try:
            engine = create_engine(f'sqlite:///{self.path}.db', echo=False)
            conn= engine.connect()
            self.logger.log(self.file, f"makeConnection :: Established connection successfully for {dbName}")
            return conn

        except ConnectionError:
            self.logger.log(self.file, f"makeConnection :: Error while connecting to database: {ConnectionError}")
            raise ConnectionError
        
    

    def insertDBdata(self,file,data,tableName,path,dbName):

        self.file=file
        self.data=data
        self.conn= self.makeConnection(self.file,path,dbName)
        
        try: 
            self.data.to_sql(tableName, self.conn, if_exists='fail',index=False)
            self.logger.log(self.file,'insertDBdata :: DB created')
            self.conn.close()

        except Exception as e:
            self.logger.log(self.file, f"insertDBdata :: Error while inserting data into DB : {e}")
            self.conn.close()
            raise e
    
    def retrieveDBdata(self,file,tableName,path,dbName):
        
        self.file=file
        self.conn= self.makeConnection(self.file,path,dbName)
        
        try: 
            self.data=pd.read_sql_table(tableName, self.conn)
            self.logger.log(self.file,'retrieveDBdata :: Data retrieved from DB')
            self.conn.close()
            return self.data

        except Exception as e:
            self.logger.log(self.file, f"retrieveDBdata :: Error while retrieving  data from DB : {e}")
            self.conn.close()
            raise e


    
