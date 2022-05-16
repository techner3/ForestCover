from src.validationPredictData import predictDataValidation
import pandas as pd 
from src.utils.config import data_load
from src.Prediction_service.predict import predictClass
from src.preprocessingPredictData import preproceesingPredictDataclass


path_predict="C:/Users/Bala/Projects/ForestCover/test_dir/forest_cover_28011990_120210.csv"
predictValid=predictDataValidation()
preprocessPredict=preproceesingPredictDataclass()
predict=predictClass()

#prediction
data=pd.read_csv(path_predict)
bool=predictValid.validatePredictData(data)
if bool:
    X=preprocessPredict.preprocess(data)
    result=predict.predictData(X)
    result.to_csv("test.csv")
else:
    print("validation failed")
print("done")
