import os
import pandas as pd
from pycaret.classification import *
from src.customLogger import LoggingObject
from src.utils.config import read_params
from src.ModelOperations.modelOps import modelOperations

class predictClass:

    """This is a custom class for prediction"""

    def __init__(self):

        self.config=read_params("params.yaml")
        self.logger=LoggingObject()
        self.modelops=modelOperations()

    def predictForACluster(self,data,clusterNo,file):
         
        self.file=file
        self.data=data
        self.clusterNo=clusterNo
        file=open(os.path.join(self.config["logging"]["prediction"]["dir"],self.config["logging"]["prediction"]["predict"]),'a+')
        
        try:
            self.model=self.modelops.load_modelcaret(dir_path=os.path.join(self.config["models"]["dir"],f"Cluster{self.clusterNo}"),model_name=self.config["models"]["modelName"],file=file)
            result=self.model.predict(data)
            self.logger.log(self.file,f'Prediction for  Cluster{clusterNo} completed successfully')
            return result
            
        except Exception as e:
            file=open(os.path.join(self.config["logging"]["prediction"]["dir"],self.config["logging"]["prediction"]["predict"]),'a+')
            self.logger.log(self.file,f'Exception Occured while predicting. Exception message:  {e}')
            raise e  

    def predictData(self,data):

        self.no=data['Cluster'].unique()
        self.df=pd.DataFrame(columns=data.drop(labels=["Cluster"],axis=1).columns)
        self.list=[]
        file=open(os.path.join(self.config["logging"]["prediction"]["dir"],self.config["logging"]["prediction"]["predict"]),'a+')
        self.logger.log(file,'Prediction of Data Started')

        try:
            for i in self.no:
                cluster_data= data[data['Cluster']==i]
                cluster_data = cluster_data.drop(['Cluster'],axis=1)
                result=self.predictForACluster(cluster_data,i,file)
                self.df=self.df.append(cluster_data)
                for i in result :
                    self.list.append(i)
            self.df["class"]=self.list
            self.df["class"] = self.df["class"].map(
            { 0:"Lodgepole_Pine",  1: "Spruce_Fir",  2: "Douglas_fir",3: "Krummholz", 4: "Ponderosa_Pine", 5: "Aspen",
             6: "Cottonwood_Willow"})
            self.logger.log(file,'Prediction of Data completed')
            self.file.close()
            return self.df

        except Exception as e:
            file=open(os.path.join(self.config["logging"]["prediction"]["dir"],self.config["logging"]["prediction"]["predict"]),'a+')
            self.logger.log(file,f'Exception Occured while predicting. Exception message:  {e}')
            file.close()
            raise e  
    
     
