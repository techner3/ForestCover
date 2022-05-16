import os
import pandas as pd 
import numpy as np
from src.ModelOperations.modelOps import modelOperations
from src.customLogger import LoggingObject
from src.utils.config import read_params

class preprocessPredictData:

    """This is a custom class for preprocessing prediction data"""

    def __init__(self):

        self.logger = LoggingObject()
        self.config = read_params('params.yaml')
    
    
    def scaleData(self,data,file):

        self.file=file
        self.modelOps=modelOperations()
        num_data = data[
            ["elevation", "aspect", "slope", "horizontal_distance_to_hydrology", "Vertical_Distance_To_Hydrology",
             "Horizontal_Distance_To_Roadways", "Horizontal_Distance_To_Fire_Points"]]
        cat_data = data.drop(
            ["elevation", "aspect", "slope", "horizontal_distance_to_hydrology", "Vertical_Distance_To_Hydrology",
             "Horizontal_Distance_To_Roadways", "Horizontal_Distance_To_Fire_Points"], axis=1)
        scalar=self.modelOps.load_model(dir_path=self.config["models"]["dir"],model_name=self.config["models"]["scalar"],file=self.file)
        scaled_data = scalar.transform(num_data)
        num_data = pd.DataFrame(scaled_data, columns=num_data.columns,index=num_data.index)
        final_data = pd.concat([num_data, cat_data], axis=1)
        return final_data

    def is_null_present(self,data,file):
        
        self.file=file
        self.logger.log(self.file, 'Entered the is_null_present method of the Preprocessor class')
        self.null_present = False

        try:
            self.null_counts=data.isna().sum()
            for i in self.null_counts:
                if i>0:
                    self.null_present=True
                    break
            if(self.null_present):
                dataframe_with_null = pd.DataFrame()
                dataframe_with_null['columns'] = data.columns
                dataframe_with_null['missing values count'] = np.asarray(data.isna().sum())
                dataframe_with_null.to_csv(os.path.join(self.config["nullValues"]["dir"],self.config["nullValues"]["file"])) 
            self.logger.log(self.file,'Finding missing values is a success.Data written to the null values file. Exited the is_null_present method of the Preprocessor class')
            self.file.close()
            return self.null_present

        except Exception as e:
            self.logger.log(self.file,f'Exception occured in is_null_present method of the Preprocessor class. Exception message:  {e}' )
            self.logger.log(self.file,'Finding missing values failed. Exited the is_null_present method of the Preprocessor class')
            self.file.close()
            raise e
