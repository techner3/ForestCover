import os
from src.Model_finder import modelFinder
from src.customLogger import LoggingObject
from src.DBOperations.DBfileops import DBops
from src.utils.config import read_params

class Model:

    """This is a custom class for training model"""

    def __init__(self):

        self.logger = LoggingObject()
        self.config = read_params("params.yaml")
        self.findModel=modelFinder.findBestModel()

    def fitData(self,data):
        
        self.data=data
        clusters=len(data['Cluster'].unique())
        file=open(os.path.join(self.config["logging"]["training"]["dir"],self.config["logging"]["training"]["train"]),"a+")
        self.logger.log(file,">>>>>>Training Started<<<<<<")
        
        try:
            for i in range(clusters):
                cluster_data=self.data[self.data["Cluster"]==i]
                cluster_data=cluster_data.drop(["Cluster"],axis=1)
                self.findModel.findBestModelforCluster(data=cluster_data,target="class",clusterNo=str(i),exp_name=f"Cluster_{str(i)}",file=file)
                file=open(os.path.join(self.config["logging"]["training"]["dir"],self.config["logging"]["training"]["train"]),"a+")
                self.logger.log(file,f"Best model found for cluster {i}")
            self.logger.log(file,">>>>>>Training Completed<<<<<<")
            file.close()

        except Exception as e:

            file=open(os.path.join(self.config["logging"]["training"]["dir"],self.config["logging"]["training"]["train"]),"a+")
            self.logger.log(file,f'Exception occured while saving the model {e}')
            file.close()
            raise e

if __name__ == '__main__':
    obj=Model()
    db=DBops()
    config=obj.config
    file=open(os.path.join(config["logging"]["training"]["dir"],config["logging"]["training"]["train"]),"a+")
    data=db.retrieveDBdata(file=file,tableName="forestCover_processedtrain",path=config["db"]["train"],dbName="processedtrain")
    file.close()
    obj.fitData(data)
        