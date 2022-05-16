import os
import json
from src.customLogger import LoggingObject
from src.utils.config import read_params
from src.Model_finder import clustering
from src.DBOperations.DBfileops import DBops
from src.Data_ingestion.dataIngestion import ingestion
from src.TrainingData_transformation.trainDataTransform import preprocessTrainData


class preproceesingTrainDataclass:

    """This is a custom class for preprocessing training data"""

    def __init__(self):

        self.logger = LoggingObject()
        self.ingestionDB=ingestion()
        self.clustering=clustering.findCluster()
        self.preprocessObj=preprocessTrainData()
        self.config = read_params('params.yaml')
    
    def preprocessBatch(self,data):

        file= open(os.path.join(self.config["logging"]["training"]["dir"],self.config["logging"]["training"]["preprocess"]),"a+")
        self.data=data
        self.logger.log(file,"Preproccesing of training data started")
        self.target='class'

        try:
            self.col_to_drop=self.preprocessObj.get_columns_with_zero_std_deviation(self.data,file,self.target)
            file= open(os.path.join(self.config["logging"]["training"]["dir"],self.config["logging"]["training"]["preprocess"]),"a+")
            if len(self.col_to_drop)!=0:
                path=os.path.join(self.config["schema"]["dir"],self.config["schema"]["dropFile"])
                with open(path+'.json','w') as f:
                    data={"Columns":self.col_to_drop}
                    json.dump(data, f)
                self.data=self.preprocessObj.remove_columns(data=self.data,columns=self.col_to_drop,file=file)
                file= open(os.path.join(self.config["logging"]["training"]["dir"],self.config["logging"]["training"]["preprocess"]),"a+")
                self.logger.log(file,"Dropped columns With Zero Standard Deviation")
            else: 
                self.logger.log(file,"No columns With Zero Standard Deviation")
            boolean=self.preprocessObj.is_null_present(self.data,file)
            file= open(os.path.join(self.config["logging"]["training"]["dir"],self.config["logging"]["training"]["preprocess"]),"a+")
            if boolean==True:
                self.data=self.preprocessObj.impute_missing_values(data=self.data,file=file)
                file= open(os.path.join(self.config["logging"]["training"]["dir"],self.config["logging"]["training"]["preprocess"]),"a+")
                self.logger.log(file,"Null Values filled")
            else: 
                self.logger.log(file,"No Null Values found in columns")
            self.data=self.preprocessObj.encodeCategoricalValues(data=self.data)
            self.logger.log(file,"Encoded categorical Values")
            self.X,self.y=self.preprocessObj.separate_label_feature(data=self.data,label_column_name=self.target,file=file)
            file= open(os.path.join(self.config["logging"]["training"]["dir"],self.config["logging"]["training"]["preprocess"]),"a+")
            self.X,self.y=self.preprocessObj.handleImbalanceDataset(X=self.X,y=self.y)
            self.logger.log(file,"Handled imbalance Dataset")
            file=open(os.path.join(self.config["logging"]["training"]["dir"],self.config["logging"]["training"]["preprocess"]),"a+")
            self.n_clusters=self.clustering.elbow_plot(data=self.X,file=file)
            file=open(os.path.join(self.config["logging"]["training"]["dir"],self.config["logging"]["training"]["preprocess"]),"a+")
            self.X=self.clustering.createClusters(noOfClusters=self.n_clusters,data=self.X,file=file)
            file=open(os.path.join(self.config["logging"]["training"]["dir"],self.config["logging"]["training"]["preprocess"]),"a+")
            self.logger.log(file,"Cluster Created successfully")
            self.X=self.preprocessObj.scaleData(data=self.X,file=file)
            self.X['class']=self.y
            
            file= open(os.path.join(self.config["logging"]["training"]["dir"],self.config["logging"]["training"]["preprocess"]),"a+")
            self.logger.log(file,"Scaling of training data has been completed successfully")
            self.ingestionDB.ingestionDB(file=file,tableName="forestCover_processedtrain",path=self.config["db"]["train"],dbName="processedtrain",data=self.X)
            self.logger.log(file,"Preproccesing of data completed")
            file.close()
        
        except Exception as e:
            file= open(os.path.join(self.config["logging"]["training"]["dir"],self.config["logging"]["training"]["preprocess"]),"a+")
            self.logger.log(file,'Exception Occured while preprocessing training data. Exception message:  {e}')
            file.close()
            raise e

    
if __name__=="__main__":
    db=DBops()
    obj=preproceesingTrainDataclass()
    config=obj.config
    file= open(os.path.join(config["logging"]["training"]["dir"],config["logging"]["training"]["preprocess"]),"a+")
    data=db.retrieveDBdata(file=file,tableName="forestCover_train",path=config["db"]["train"],dbName="train")
    file.close()
    obj.preprocessBatch(data)

