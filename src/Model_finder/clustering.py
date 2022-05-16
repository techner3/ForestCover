import os
import pandas as pd
from src.customLogger import LoggingObject
from src.utils.config import read_params
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from kneed import KneeLocator
from src.ModelOperations.modelOps import modelOperations

class findCluster:

    """This is a custom class to perform clustering"""

    def __init__(self):
        
        self.config=read_params('params.yaml')
        self.logger=LoggingObject()
        self.modelops=modelOperations()

    def elbow_plot(self,data,file):

        self.file=file
        self.logger.log(self.file, 'Entered the elbow_plot method of the KMeansClustering class')
        wcss=[]

        try:
            for i in range (1,11):
                kmeans=KMeans(n_clusters=i,init='k-means++',random_state=42) 
                kmeans.fit(data) 
                wcss.append(kmeans.inertia_)
            plt.plot(range(1,11),wcss) 
            plt.title('The Elbow Method')
            plt.xlabel('Number of clusters')
            plt.ylabel('WCSS')
            os.makedirs(self.config["plots"]["dir"],exist_ok=True)
            plt.savefig(os.path.join(self.config["plots"]["dir"],self.config["plots"]["kmeans"])) 
            self.kn = KneeLocator(range(1, 11), wcss, curve='convex', direction='decreasing')
            self.logger.log(self.file, f'The optimum number of clusters is: {self.kn.knee} . Exited the elbow_plot method of the KMeansClustering class')
            self.file.close()
            return self.kn.knee

        except Exception as e:
            self.logger.log(self.file,f'Exception occured in elbow_plot method of the KMeansClustering class. Exception message: {e}')
            self.logger.log(self.file,'Finding the number of clusters failed. Exited the elbow_plot method of the KMeansClustering class')
            self.file.close()
            raise e

    def createClusters(self,noOfClusters,data,file):

        self.file=file
        self.data=data
        self.logger.log(file, 'Entered the create_clusters method of the KMeansClustering class')

        try:
            self.kmeans = KMeans(n_clusters=noOfClusters, init='k-means++', random_state=42)
            self.y_kmeans=self.kmeans.fit_predict(self.data)
            self.modelops.save_model(model=self.kmeans,dir_path=self.config["models"]["dir"],model_name=self.config["models"]["clustering"],file=self.file)
            parameters=str(self.kmeans.get_params())
            self.modelops.save_modelParams(params=parameters,dir_path=self.config["models"]["dir"],model_name=self.config["models"]["clustering"],file=self.file)
            self.data['Cluster']=self.y_kmeans 
            self.logger.log(self.file, f'Succesfully created {self.kn.knee} clusters. Exited the create_clusters method of the KMeansClustering class')
            self.file.close()
            return self.data

        except Exception as e:
            self.logger.log(self.file,f'Exception occured in create_clusters method of the KMeansClustering class. Exception message: {e}')
            self.logger.log(self.file,'Fitting the data to clusters failed. Exited the create_clusters method of the KMeansClustering class')
            self.file.close()
            raise e