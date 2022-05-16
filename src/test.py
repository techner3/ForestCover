from validationPredictData import predictDataValidation
import pandas as pd 
from utils.config import data_load
from Prediction_service.predict import predictClass
from preprocessingPredictData import preproceesingPredictDataclass


path_predict="C:/Users/Bala/Projects/ForestCover/testing/predict/forest_cover_28011990_120210.csv"
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
