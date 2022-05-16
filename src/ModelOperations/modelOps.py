import pickle
import os 
import json
from pycaret.classification import *
from src.customLogger import LoggingObject
from src.utils.config import read_params

class modelOperations:

    """This is a custom class for saving and loading model"""

    def __init__(self,):

        self.logger = LoggingObject()
    
    def save_model(self,model,dir_path,model_name,file):

        self.file=file
        try:
            os.makedirs(os.path.join(dir_path,model_name.split('.sav')[0]),exist_ok=True)
            with open(dir_path+"/"+model_name.split('.sav')[0]+"/"+model_name,'wb') as f:
                pickle.dump(model, f)
            self.logger.log(self.file,f"Succesfully saved the model {model_name}")

        except Exception as e:
            self.logger.log(self.file,f'Exception occured while saving the model {e}')
            raise e
    
    def save_modelParams(self,params,dir_path,model_name,file):

        self.file=file
        try:
            name=model_name.split('.sav')[0]
            os.makedirs(os.path.join(dir_path,name),exist_ok=True)
            with open(dir_path+"/"+name+"/"+name+'.json','w') as f:
                parameters={"params":params}
                json.dump(parameters, f)
            self.logger.log(self.file,f"Succesfully saved the {model_name}'s params")

        except Exception as e:
            self.logger.log(self.file,f'Exception occured while saving the model Parameters {e}')
            raise e
    
    def load_model(self,dir_path,model_name,file):

        self.file=file
        name=model_name.split('.sav')[0]
        try:
            with open(dir_path+"/"+name+"/"+model_name,'rb') as f:
                self.logger.log(self.file,f"{name} model loaded succesfully")
                return pickle.load(f)

        except Exception as e:
            self.logger.log(self.file,f'Exception occured while loading model {e}')
            raise e
    
    def save_modelcaret(self,model,dir_path,model_name,file):

        self.file=file
        try:
            os.makedirs(dir_path,exist_ok = True)
            save_model(model, os.path.join(dir_path,model_name))
            self.logger.log(self.file,"Succesfully saved the model")

        except Exception as e:
            self.logger.log(self.file,f'Exception occured while saving the model {e}')
            raise e
    
    def load_modelcaret(self,dir_path,model_name,file):

        self.file=file
        try:
            model=load_model(os.path.join(dir_path,model_name))
            self.logger.log(self.file,"Succesfully loaded the model")
            return model

        except Exception as e:
            self.logger.log(self.file,f'Exception occured while loading model {e}')
            raise e