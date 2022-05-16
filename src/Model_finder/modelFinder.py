from pycaret.classification import *
import os
from src.customLogger import LoggingObject
from src.utils.config import read_params
from src.ModelOperations.modelOps import modelOperations

class findBestModel:

    """This is a custom class to find the best model through experimentation"""

    def __init__(self):

        self.config=read_params("params.yaml")
        self.logger=LoggingObject()
        self.modelops=modelOperations()


    def findBestModelforCluster(self,exp_name,data,target,clusterNo,file):

        self.file=file
        self.logger.log(file,f"Setting up an experiment to find the best model")

        try:
            self.experiment = setup(data, target = target,experiment_name = exp_name,log_experiment = True,silent = True,log_plots = True)
            self.model = compare_models(n_select = 1)
            self.logger.log(self.file,f"Found the best model for Cluster {clusterNo}")
            self.tuned_model = tune_model(self.model)
            self.logger.log(self.file,f"Tuning the best model for Cluster {clusterNo}")
            self.finalized_model = finalize_model(self.tuned_model)
            self.logger.log(self.file,f"Finalizing the best model for Cluster {clusterNo}")
            self.modelops.save_modelcaret(model=self.finalized_model,dir_path=os.path.join(self.config["models"]["dir"],f"Cluster{clusterNo}"),model_name=self.config["models"]["modelName"],file=file)
            self.modelops.save_modelParams(params=str(self.finalized_model.get_params()),dir_path=os.path.join(self.config["models"]["dir"],f"Cluster{clusterNo}"),model_name=self.config["models"]["modelName"],file=self.file)
            self.file.close()

        except Exception as e:
            self.logger.log(self.file,f"Failed to find the bestmodel for Cluster {clusterNo}")
            self.logger.log(self.file,f"Exited from the function findBestModelforCluster")
            self.file.close()
            raise e
    

