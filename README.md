# Forest Cover Prediction
![my badge](https://img.shields.io/badge/Python-3-blue)
![my badge](https://img.shields.io/badge/Machine-Learning-brightgreen)
![my badge](https://img.shields.io/badge/Flask-App-green)
![my badge](https://img.shields.io/badge/ML-Flow-yellowgreen)
![my badge](https://img.shields.io/badge/AI-OPS-orange)
![my badge](https://img.shields.io/badge/-Heroku-purple)
![my badge](https://img.shields.io/badge/-GIT-green)
![my badge](https://img.shields.io/badge/-DVC-darkblue)

# About The Project

This project has been developed to predict what type of trees grow in an area based on it's surrounding characteristics. The dataset consists of observations of various catagrophic features (No sensor data). The dataset used for the project mostly contain observations from Roosevelt National Forest in Colorado.

# Project Description 

This project has been developed in semi-supervised learning way. Initally, the data without the target column is passed through a clustering model which predicts the cluster. Then for each cluster, a ML supervised learning model has been used to predict the type of forest cover. A web app has been developed for this project which takes a CSV file as an input and returns the predictions as a result. The app is deployed in Heroku.

# Dataset Used

This dataset is part of the UCI Machine Learning Repository and more information about the dataset can be found below.

Dataset : [Link](https://archive.ics.uci.edu/ml/datasets/Covertype)

# Project Structure


<img width="227" alt="image" src="https://user-images.githubusercontent.com/58848985/169639264-cea3427c-633b-4d3f-a789-335aa2baefcc.png">

<img width="226" alt="image" src="https://user-images.githubusercontent.com/58848985/169639295-a198e0d0-8bef-41c0-87b1-9b237443c9db.png">

<img width="226" alt="image" src="https://user-images.githubusercontent.com/58848985/169639340-f0f85dc2-d5f3-4257-bfa5-46c6945326bd.png">

* data_given - This directory contains the data that has been given for both training as well as predicting 
* data - This directory contains good and bad data after validation of files with respect to everything in schema for training and prediction
* frontend - This directory contains files related to frontend of the web app
* logs - This directories contains logs file that has been generated during both training and prediction
* mlruns - This directory contains all the logs from the experimentation of finding the best model
* notebooks - This directory contains notebooks used for EDA and testing purposes
* savedModels - This directory contains all the saved models for each cluster and also clustering and scaling models
* savedModel - This directory contains plots geenrated udring training
* schema - This directaory contains schema as JSon file used for data validation 
* src - This directory contains the source code for this project
* test_dir - This directory contains data used for tesing the web app


# Preview of the Web App

webApp : [Link](https://forestcover-webapp.herokuapp.com/)

Home page :

<img width="960" alt="image" src="https://user-images.githubusercontent.com/58848985/169639173-b49ffd00-f3ac-443e-a9a7-c0d9e89ca450.png">

After prediction:

<img width="959" alt="image" src="https://user-images.githubusercontent.com/58848985/169639225-12196595-7de7-47bf-bcde-73610e5b28b0.png">

# Points to Note : 

* The app may take while to load ,Please bear with it 
* Many of the libraries are commented in requirements.txt and libraries needed only for prediction has been installed to reduce slug size while deploying to heroku. 