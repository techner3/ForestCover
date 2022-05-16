import os
import json
from src.customLogger import LoggingObject
from src.utils.config import read_params
from src.customException import noValue
from src.ModelOperations.modelOps import modelOperations
from src.PredictionData_transformation.predictDataTransform import preprocessPredictData

class preproceesingPredictDataclass:

    """This is a custom class for preprocessing Prediction data"""

    def __init__(self):

        self.logger = LoggingObject()
        self.config = read_params('params.yaml')
        self.schema_path=os.path.join(self.config["schema"]["dir"],self.config["schema"]["dropFile"])
        self.modelops=modelOperations()
        self.preprocessObj=preprocessPredictData()
    
    def preprocess(self,data):

        file= open(os.path.join(self.config["logging"]["prediction"]["dir"],self.config["logging"]["prediction"]["preprocess"]),"a+")
        self.logger.log(file,"Preproccesing of prediction data started")
        self.data=data

        try:
            with open(self.schema_path+'.json', 'r') as f:
                dic = json.load(f)
                f.close()
            dropList=dic["Columns"]
            self.data=self.data.drop(labels=dropList,axis=1)
            boolean=self.preprocessObj.is_null_present(self.data,file)
            file= open(os.path.join(self.config["logging"]["prediction"]["dir"],self.config["logging"]["prediction"]["preprocess"]),"a+")
            if boolean==True:
                self.logger.log(file,"Null Values present")
                self.data=self.data.dropna()
                self.logger.log(file,"Dropped rows with null values")
                if self.data.shape[0] == 0:
                    raise noValue
            else: 
                self.logger.log(file,"No Null Values found in columns")
            self.kmeans=self.modelops.load_model(dir_path=self.config["models"]["dir"],model_name=self.config["models"]["clustering"],file=file)
            self.clusterNo=self.kmeans.predict(self.data)
            self.logger.log(file,"Cluster No predicted successfully")
            self.X=self.preprocessObj.scaleData(data=self.data,file=file)
            file= open(os.path.join(self.config["logging"]["prediction"]["dir"],self.config["logging"]["prediction"]["preprocess"]),"a+")
            self.logger.log(file,"Scaling of prediction data has been completed successfully")
            file.close()
            self.X['Cluster']=self.clusterNo
            return self.X

        except noValue as e:
            file= open(os.path.join(self.config["logging"]["training"]["dir"],self.config["logging"]["training"]["preprocess"]),"a+")
            self.logger.log(file,'Exception Occured while preprocessing prediction data. Exception message:  {e}')
            file.close()
            raise e
        
        except Exception as e:
            file= open(os.path.join(self.config["logging"]["training"]["dir"],self.config["logging"]["training"]["preprocess"]),"a+")
            self.logger.log(file,'Exception Occured while preprocessing predicition data. Exception message:  {e}')
            file.close()
            raise e

    
            
        

