import os
from src.customLogger import LoggingObject
from src.utils.config import read_params
from src.Data_ingestion.dataIngestion import ingestion
from src.Prediction_rawData_validation.predictDataValidation import predictDataValidationClass

class predictDataValidation:

    def __init__(self):

        self.logger = LoggingObject()
        self.ingestionLocally=ingestion()
        self.validateDataObj=predictDataValidationClass()
        self.config = read_params("params.yaml")

    def validatePredictDataBatch(self,dir_path):

        self.batch_dir_path=dir_path
        file=open(os.path.join(self.config["logging"]["prediction"]["dir"],self.config["logging"]["prediction"]["data_validation"]),"a+")
        self.logger.log(file,"Validation of Prediction data started")
        
        try:
            dateStampLength, timeStampLength, NumberofColumns=self.validateDataObj.getvaluesfromSchema(file)
            file=open(os.path.join(self.config["logging"]["prediction"]["dir"],self.config["logging"]["prediction"]["data_validation"]),"a+")
            regex=self.validateDataObj.regexCreations()
            self.validateDataObj.validateFiles(regex=regex,dateStampLength=dateStampLength,timeStampLength=timeStampLength,NumberofColumns=NumberofColumns,batch_dir_path=self.batch_dir_path,file=file)
            file=open(os.path.join(self.config["logging"]["prediction"]["dir"],self.config["logging"]["prediction"]["data_validation"]),"a+")
            self.logger.log(file,"Validation of file completed")
            self.validateDataObj.validateMissingValuesWholeColumn(file)
            file=open(os.path.join(self.config["logging"]["prediction"]["dir"],self.config["logging"]["prediction"]["data_validation"]),"a+")
            self.logger.log(file,"Validation of missing values for whole column completed")
            self.logger.log(file,"Prediction data Validation Completed")
            self.data=self.ingestionLocally.ingestionPredictDB(file,tableName="forestCover_predict",path=self.config["db"]["predict"],dbName="predict")
            file=open(os.path.join(self.config["logging"]["prediction"]["dir"],self.config["logging"]["prediction"]["data_validation"]),"a+")
            self.logger.log(file,"Prediction data obtained")
            file.close()
            return self.data

        except Exception as e:
            file=open(os.path.join(self.config["logging"]["prediction"]["dir"],self.config["logging"]["prediction"]["data_validation"]),"a+")
            self.logger.log(file,'Exception Occured while Validating Prediction data. Exception message:  {e}')
            file.close()
            raise e

    def validatePredictData(self, data):

        file=open(os.path.join(self.config["logging"]["prediction"]["dir"],self.config["logging"]["prediction"]["data_validation"]),"a+")
        
        try:
            dateStampLength, timeStampLength, NumberofColumns=self.validateDataObj.getvaluesfromSchema(file)
            file=open(os.path.join(self.config["logging"]["prediction"]["dir"],self.config["logging"]["prediction"]["data_validation"]),"a+")
            bool=self.validateDataObj.validateData(data=data,NumberofColumns=NumberofColumns)
            if bool:
                bool1=self.validateDataObj.validateMissingValuesWholeColumnData(data)
                if bool1:
                    self.logger.log(file,"Validation of data completed")
                    file.close()
                    return True
                else: 
                    self.logger.log(file,"Missing Values for a whole Column")
                    file.close()
                    return False
            else:
                self.logger.log(file, "Mismatch Number of columns")
                file.close()
                return False

        except Exception as e:
            self.logger.log(file, f"Exception occured while validating Data : {e}")
            file.close()
            raise e