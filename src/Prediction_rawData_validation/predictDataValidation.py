import os 
import shutil 
import pandas as pd
import re
import json
from src.customLogger import LoggingObject
from src.utils.config import read_params

class predictDataValidationClass:

    """This is a custom class for prediction data validation"""

    def __init__(self):

        self.config=read_params('params.yaml')
        self.schema_path=os.path.join(self.config["schema"]["dir"],self.config["schema"]["prediction"])
        self.logger=LoggingObject()

    def getvaluesfromSchema(self,file):

        self.file=file
        try:
            with open(self.schema_path, 'r') as f:
                dic = json.load(f)
                f.close()
            dateStampLength = dic['LengthOfDateStampInFile']
            timeStampLength = dic['LengthOfTimeStampInFile']
            NumberofColumns = dic['NumberofColumns']
            message =f"LengthOfDateStampInFile:{dateStampLength}  LengthOfTimeStampInFile:{timeStampLength}  NumberofColumns:{NumberofColumns}"
            self.logger.log(self.file,message)
            self.file.close()
            return dateStampLength, timeStampLength, NumberofColumns

        except ValueError:
            self.logger.log(self.file,f"getvaluesfromSchema : ValueError:Value not found inside schema_prediction.json")
            self.file.close()
            raise ValueError

        except KeyError:
            self.logger.log(self.file,f"getvaluesfromSchema : KeyError:Key value error incorrect key passed")
            self.file.close()
            raise KeyError

        except Exception as e:
            self.logger.log(self.file, f"getvaluesfromSchema : {str(e)}")
            self.file.close()
            raise e

    def regexCreations(self):

        regex = "['forest_cover']+['\_'']+[\d_]+[\d]+\.csv"
        return regex

    def createGoodBadrawDataDirectory(self,file):

        self.file=file
        try:
            path = os.path.join(self.config["directories"]["validatedFiles"]["prediction"], self.config["directories"]["rawGood"])
            os.makedirs(path,exist_ok=True)
            path = os.path.join(self.config["directories"]["validatedFiles"]["prediction"], self.config["directories"]["rawBad"])
            os.makedirs(path,exist_ok=True)
            self.logger.log(self.file,f"CreateGoodBadrawDataDirectory : Good and Bad Directories created")

        except OSError as ex:
            self.logger.log(self.file,f"CreateGoodBadrawDataDirectory : Error while creating Directory {ex}")
            raise OSError

    def deleteGoodBadrawDataDirectory(self,file):

        self.file=file
        try:
            main_dir=self.config["directories"]["validatedFiles"]["prediction"]
            sub_dir=self.config["directories"]["rawGood"]
            if sub_dir in os.listdir(main_dir):
                path = os.path.join(main_dir, sub_dir)
                shutil.rmtree(path)
            main_dir=self.config["directories"]["validatedFiles"]["prediction"]
            sub_dir=self.config["directories"]["rawBad"]
            if sub_dir in os.listdir(main_dir):
                path = os.path.join(main_dir, sub_dir)
                shutil.rmtree(path)
            self.logger.log(self.file,f"Good and Bad Directories Deleted")

        except OSError as ex:
            self.logger.log(self.file,f"Error while deleting Directory {ex}")
            raise OSError
    
    def validateFiles(self,regex,timeStampLength,dateStampLength,NumberofColumns, batch_dir_path,file):

        self.file=file
        self.deleteGoodBadrawDataDirectory(file)
        self.createGoodBadrawDataDirectory(file)
        self.batch_directory_path = batch_dir_path
        self.goodFiledir=os.path.join(self.config["directories"]["validatedFiles"]["prediction"], self.config["directories"]["rawGood"])
        self.badFiledir=os.path.join(self.config["directories"]["validatedFiles"]["prediction"], self.config["directories"]["rawBad"])
        batch_files= [f for f in os.listdir(self.batch_directory_path)]
        
        try:
            for filename in batch_files:
                if (re.match(regex, filename)):
                    splitAtDot = re.split('.csv', filename)
                    splitAtDot = (re.split('_', splitAtDot[0]))
                    if len(splitAtDot[2]) == dateStampLength:
                        if len(splitAtDot[3]) == timeStampLength:
                            csv = pd.read_csv(os.path.join(self.batch_directory_path,filename))
                            if csv.shape[1]==NumberofColumns:
                                shutil.copy(os.path.join(self.batch_directory_path, filename), self.goodFiledir)
                                self.logger.log(self.file,f"Valid File name!! File moved to GoodRaw Folder :: {filename}")
                            else:
                                shutil.copy(os.path.join(self.batch_directory_path, filename), self.badFiledir)
                                self.logger.log(self.file,f"Number of Columns Mismatch!! File moved to Bad Raw Folder :: {filename}")
                        else:
                            shutil.copy(os.path.join(self.batch_directory_path, filename), self.badFiledir)
                            self.logger.log(self.file,f"Time Stamp Length Mismtach!! File moved to Bad Raw Folder :: {filename}")
                    else:
                        shutil.copy(os.path.join(self.batch_directory_path, filename), self.badFiledir)
                        self.logger.log(self.file,f"Date Stamp Length Mismtach!! File moved to Bad Raw Folder :: {filename}")
                else:
                    shutil.copy(os.path.join(self.batch_directory_path, filename), self.badFiledir)
                    self.logger.log(self.file, f"Invalid File Name!! File moved to Bad Raw Folder :: {filename}")

            self.file.close()

        except OSError as ex:
            self.logger.log(self.file,f"validateFileName : Error while moving the file {ex}")
            self.file.close()
            raise OSError

        except Exception as e:
            self.logger.log(self.file, f"validateFileName : Error occured while validating FileName {e}")
            self.file.close()
            raise e

    def validateMissingValuesWholeColumn(self,file):

        self.file=file
        try:
            self.goodFiledir=os.path.join(self.config["directories"]["validatedFiles"]["prediction"], self.config["directories"]["rawGood"])
            self.badFiledir=os.path.join(self.config["directories"]["validatedFiles"]["prediction"], self.config["directories"]["rawBad"])
            self.logger.log(self.file,"Missing Values Validation Started for rawGoodFiles")

            for filename in os.listdir(self.goodFiledir):
                csv = pd.read_csv(os.path.join(self.goodFiledir ,filename))
                count = 0
                for columns in csv:
                    if (len(csv[columns]) - csv[columns].count()) == len(csv[columns]):
                        count+=1
                        shutil.move(os.path.join(self.goodFiledir + filename),self.badFiledir)
                        self.logger.log(self.file,f"Invalid Column Length for the file!! File moved to Bad Raw Folder :: {filename}")
                        break
            self.file.close()
        
        except OSError as ex:
            self.logger.log(self.file,f"validateMissingValuesWholeColumn : Error while moving the file {ex}")
            self.file.close()
            raise OSError

        except Exception as e:
            self.logger.log(self.file, f"validateMissingValuesWholeColumn : Error occured while validating FileName {e}")
            self.file.close()
            raise e
    
    def validateData(self,NumberofColumns,data):
        
        try:
            csv = data
            if csv.shape[1]==NumberofColumns:
                return True
            else:
                return False
                                
        except Exception as e:
            raise e
    
    def validateMissingValuesWholeColumnData(self,data):

        try:
            csv = data
            count = 0
            for columns in csv:
                if (len(csv[columns]) - csv[columns].count()) == len(csv[columns]):
                    count+=1
                    break
            if count==0:
                return True
            else: 
                return False
        
        except Exception as e:
            raise e


