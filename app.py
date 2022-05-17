from flask import Flask, render_template, request, send_file
from flask_cors import  cross_origin
import os
import pandas as pd 
import numpy as np
from src.validationPredictData import predictDataValidation
from src.preprocessingPredictData import preproceesingPredictDataclass
from src.Prediction_service.predict import predictClass


webapp_root = "frontend"

template_dir = os.path.join(webapp_root, "templates")

app = Flask(__name__,template_folder=template_dir)

@app.route('/')
@cross_origin()
def home():
    return render_template('index.html')


@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRouteClient():
    try:
        if request.method == 'POST':
            if request.form is not None: 
                if ".csv" in request.form['filepath']: 
                    data = pd.read_csv(request.form['filepath'])
                    predictValid=predictDataValidation()
                    preprocessPredict=preproceesingPredictDataclass()
                    predict=predictClass()
                    bool=predictValid.validatePredictData(data)
                    if bool:
                        X=preprocessPredict.preprocess(data)
                        result=predict.predictData(X)
                        result.to_csv("predict.csv")
                        return send_file('predict.csv',attachment_filename= 'predict.csv',as_attachment = True)
                    else:
                        return "Data Validation Failed. Mismatched number of columns"
                else: 
                    return "Please pass .csv file"
            else:
                return "Please enter the csv File path"

    except Exception as e:
        return f"Something went wrong {e}"

if __name__ == "__main__":
    app.run()