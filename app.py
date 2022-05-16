from flask import Flask, render_template, request, jsonify
from flask_cors import  cross_origin
import os
import pandas as pd 
import numpy as np
from src.validationPredictData import predictDataValidation
from src.preprocessingPredictData import preproceesingPredictDataclass
from prediction_service.predict import predictClass


webapp_root = "frontend"

template_dir = os.path.join(webapp_root, "templates")

app = Flask(__name__,template_folder=template_dir)

@app.route('/')
@cross_origin()
def home():
    return render_template('Index.html')


@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRouteClient():
    try:
        if request.form is not None: 
            if ".csv" in request.form['filepath']: 
                data = pd.read_csv(request.form['filepath'])
                validate=predictDataValidation()
                if validate.validatePredictData(data) :
                    preprocess=preproceesingPredictDataclass()
                    predict=predictClass()
                    data=preprocess.preprocess(data)
                    result=predict.predictData(data)
                    return result
                else:
                    pass
            else: 
                pass
        else:
            pass

    except Exception as e:
        print(e)
        error = {"error": "Something went wrong!! Try again later!"}
        error = {"error": e}
        return render_template("404.html", error=error)

if __name__ == "__main__":
    app.run()