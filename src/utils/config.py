import yaml
import os
import pandas as pd

def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

def data_load(path):
    data=pd.DataFrame()
    for file in os.listdir(path):
        df=pd.read_csv(os.path.join(path,file))
        data=data.append(df)
    return data