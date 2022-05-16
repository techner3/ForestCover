import os
import pandas as pd
from src.DBOperations.DBfileops import DBops
from src.customLogger import LoggingObject
from src.utils.config import read_params

class ingestion:

    """This is a custom class for ingestion of predict and train data"""

    def __init__(self):

        self.logger = LoggingObject()
        self.db=DBops()
        self.config = read_params("params.yaml")

    def trainDataIngestion(self,file):
        
        self.file=file
        self.logger.log(self.file, "Training Data Ingestion started locally")
        self.path=os.path.join(self.config["directories"]["validatedFiles"]["training"],self.config["directories"]["rawGood"])
        self.data=pd.DataFrame()

        try:
            for file in os.listdir(self.path):
                df=pd.read_csv(os.path.join(self.path,file))
                self.logger.log(self.file,f"{file} data retrieved")
                self.data=self.data.append(df)
            self.logger.log(self.file,"Training Data Ingestion locally completed")
            return self.data

        except Exception as e:
            self.logger.log(file,f'Exception Occured while training data ingestion. Exception message:  {e}')
            raise e
    
    def predictDataIngestion(self,file):
        
        self.file=file
        self.logger.log(self.file, "Prediction Data Ingestion started locally")
        self.path=os.path.join(self.config["directories"]["validatedFiles"]["prediction"],self.config["directories"]["rawGood"])
        self.data=pd.DataFrame()

        try:
            for file in os.listdir(self.path):
                df=pd.read_csv(os.path.join(self.path,file))
                self.logger.log(self.file,f"{file} data retrieved")
                self.data=self.append(df)
            self.logger.log(self.file,"Prediction Data Ingestion locally completed")
            return self.data

        except Exception as e:
            self.logger.log(file,f'Exception Occured while prediction data ingestion. Exception message:  {e}')
            raise e
    
    def ingestionDB(self,file,tableName,path,dbName,data):
        
        self.file=file
        self.data=data
        self.logger.log(file,"ingestionDB :: Train Data ingestion into DB started")
        
        try:
            self.db.insertDBdata(file=self.file,data=self.data,tableName=tableName,path=path,dbName=dbName)
            self.logger.log(file,"ingestionTrainDB :: Train Data ingestion into DB completed")

        except Exception as e:
            self.logger.log(file,f'ingestionDB :: Exception Occured while data ingestion in DB . Exception message:  {e}')
            raise e
    
    