import os
import pandas as pd 
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
from src.ModelOperations.modelOps import modelOperations
from src.customLogger import LoggingObject
from src.utils.config import read_params

class preprocessTrainData:

    """This is a custom class for preprocessing training data"""

    def __init__(self):

        self.logger = LoggingObject()
        self.config = read_params('params.yaml')
    
    def encodeCategoricalValues(self,data):
        
        data["class"] = data["class"].map(
            {"Lodgepole_Pine": 0, "Spruce_Fir": 1, "Douglas_fir": 2, "Krummholz": 3, "Ponderosa_Pine": 4, "Aspen": 5,
             "Cottonwood_Willow": 6})
        return data

    def handleImbalanceDataset(self,X,y):

        sample = SMOTE()
        X, y = sample.fit_resample(X, y)
        return X,y
    
    def scaleData(self,data,file):

        self.file=file
        self.modelOps=modelOperations()
        scalar = StandardScaler()
        num_data = data[
            ["elevation", "aspect", "slope", "horizontal_distance_to_hydrology", "Vertical_Distance_To_Hydrology",
             "Horizontal_Distance_To_Roadways", "Horizontal_Distance_To_Fire_Points"]]
        cat_data = data.drop(
            ["elevation", "aspect", "slope", "horizontal_distance_to_hydrology", "Vertical_Distance_To_Hydrology",
             "Horizontal_Distance_To_Roadways", "Horizontal_Distance_To_Fire_Points"], axis=1)
        scaled_data = scalar.fit_transform(num_data)
        self.modelOps.save_model(model=scalar,dir_path=self.config["models"]["dir"],model_name=self.config["models"]["scalar"],file=self.file)
        num_data = pd.DataFrame(scaled_data, columns=num_data.columns,index=num_data.index)
        final_data = pd.concat([num_data, cat_data], axis=1)
        return final_data

    def get_columns_with_zero_std_deviation(self,data,file,target):
        
        self.file=file
        self.logger.log(self.file, 'Entered the get_columns_with_zero_std_deviation method of the Preprocessor class')
        self.columns=data.drop([target],axis=1).columns
        self.data_n = data.describe()
        self.col_to_drop=[]

        try:
            for x in self.columns:
                if (self.data_n[x]['std'] == 0): 
                    self.col_to_drop.append(x)  
            self.logger.log(self.file, 'Column search for Standard Deviation of Zero Successful. Exited the get_columns_with_zero_std_deviation method of the Preprocessor class')
            self.file.close()
            return self.col_to_drop

        except Exception as e:
            self.logger.log(self.file,f'Exception occured in get_columns_with_zero_std_deviation method of the Preprocessor class. Exception message: {e}')
            self.logger.log(self.file, 'Column search for Standard Deviation of Zero Failed. Exited the get_columns_with_zero_std_deviation method of the Preprocessor class')
            self.file.close()
            raise e

    def remove_columns(self,data,columns,file):
        
        self.file=file
        self.logger.log(self.file, 'Entered the remove_columns method of the Preprocessor class')
        self.data=data
        self.columns=columns

        try:
            self.useful_data=data.drop(labels=self.columns, axis=1) 
            self.logger.log(self.file,'Column removal Successful.Exited the remove_columns method of the Preprocessor class')
            self.file.close()
            return self.useful_data

        except Exception as e:
            self.logger.log(self.file,f'Exception occured in remove_columns method of the Preprocessor class. Exception message: {e} ')
            self.logger.log(self.file,'Column removal Unsuccessful. Exited the remove_columns method of the Preprocessor class')
            self.file.close()
            raise e

    def separate_label_feature(self, data, label_column_name,file):
        
        self.file=file
        self.logger.log(self.file, 'Entered the separate_label_feature method of the Preprocessor class')
        
        try:
            self.X=data.drop(labels=[label_column_name],axis=1)
            self.Y=data[label_column_name] 
            self.logger.log(self.file,'Label Separation Successful. Exited the separate_label_feature method of the Preprocessor class')
            self.file.close()
            return self.X,self.Y

        except Exception as e:
            self.logger.log(self.file,'Exception occured in separate_label_feature method of the Preprocessor class. Exception message:  {e}')
            self.logger.log(self.file, 'Label Separation Unsuccessful. Exited the separate_label_feature method of the Preprocessor class')
            self.file.close()
            raise e

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

    def impute_missing_values(self, data,file):
       
        self.file=file
        self.logger.log(self.file, 'Entered the impute_missing_values method of the Preprocessor class')
        self.data= data

        try:
            imputer=KNNImputer(n_neighbors=3, weights='uniform',missing_values=np.nan)
            self.new_array=imputer.fit_transform(self.data) 
            self.new_data=pd.DataFrame(data=self.new_array, columns=self.data.columns)
            self.logger.log(self.file, 'Imputing missing values Successful. Exited the impute_missing_values method of the Preprocessor class')
            self.file.close()
            return self.new_data

        except Exception as e:
            self.logger.log(self.file,'Exception occured in impute_missing_values method of the Preprocessor class. Exception message:  {e}')
            self.logger.log(self.file,'Imputing missing values failed. Exited the impute_missing_values method of the Preprocessor class')
            self.file.close()
            raise e