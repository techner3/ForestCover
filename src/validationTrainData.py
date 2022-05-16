import os
from src.customLogger import LoggingObject
from src.utils.config import read_params
from src.Data_ingestion.dataIngestion import ingestion
from src.Training_rawData_validation.trainDataValidation import trainDataValidationClass

class trainDataValidation:

    """This is a component for training data validation"""
    
    def __init__(self):

        self.logger = LoggingObject()
        self.config = read_params("params.yaml")
        self.validateDataObj=trainDataValidationClass()
        self.ingestionDB=ingestion()

    def validateTrainData(self,dir_path):

        self.batch_dir_path=dir_path
        file=open(os.path.join(self.config["logging"]["training"]["dir"],self.config["logging"]["training"]["data_validation"]),"a+")
        self.logger.log(file,"Validation of Training data started")
        
        try:
            dateStampLength, timeStampLength, NumberofColumns=self.validateDataObj.getvaluesfromSchema(file)
            file=open(os.path.join(self.config["logging"]["training"]["dir"],self.config["logging"]["training"]["data_validation"]),"a+")
            regex=self.validateDataObj.regexCreations()
            self.validateDataObj.validateFiles(regex=regex,dateStampLength=dateStampLength,timeStampLength=timeStampLength,NumberofColumns=NumberofColumns,batch_dir_path=self.batch_dir_path,file=file)
            file=open(os.path.join(self.config["logging"]["training"]["dir"],self.config["logging"]["training"]["data_validation"]),"a+")
            self.logger.log(file,"Validation of file completed")
            self.validateDataObj.validateMissingValuesWholeColumn(file)
            file=open(os.path.join(self.config["logging"]["training"]["dir"],self.config["logging"]["training"]["data_validation"]),"a+")
            self.logger.log(file,"Validation of missing values for whole column completed")
            self.logger.log(file,"Training data Validation Completed")
            self.data= self.ingestionDB.trainDataIngestion(file)
            self.ingestionDB.ingestionDB(file=file,tableName="forestCover_train",path=self.config["db"]["train"],dbName="train",data=self.data)
            
            file=open(os.path.join(self.config["logging"]["training"]["dir"],self.config["logging"]["training"]["data_validation"]),"a+")
            self.logger.log(file,"Training data obtained")
            file.close()

        except Exception as e:
            file=open(os.path.join(self.config["logging"]["training"]["dir"],self.config["logging"]["training"]["data_validation"]),"a+")
            self.logger.log(file,'Exception Occured while Validating training data. Exception message:  {e}')
            file.close()
            raise e

if __name__ == "__main__":
    obj=trainDataValidation()
    path="data_given/train"
    obj.validateTrainData(path)
