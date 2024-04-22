"""
utils.py
Este archivo contiene las functiones
utils que utilizamos en todo el
proyecto.
Autor: Karen Sarai Morales Montiel
Fecha de creación: 22/04/2024
"""
import pandas as pd
import os
import joblib
import importlib.util
from . import constants


def read_insurance_data():
    """Read data from a file in the common folder."""
    file_path = os.path.join(os.path.dirname(__file__), '..', constants.INSURANCE_DATA_PATH)
    return pd.read_csv(file_path)

def write_insurance_data(insurance_df: pd.DataFrame):
    file_path = os.path.join(os.path.dirname(__file__), '..', constants.INSURANCE_DATA_PATH)
    insurance_df.to_csv(file_path, index=False)


def read_model():
    file_path = os.path.join(os.path.dirname(__file__), '..' , constants.GASTOS_MEDICOS_MODEL_PATH)
    return joblib.load(file_path)

def write_model(model):
    file_path = os.path.join(os.path.dirname(__file__), '..' , constants.GASTOS_MEDICOS_MODEL_PATH)
    joblib.dump(model, file_path)

    
def read_model_data():
    model_data_path = os.path.join(os.path.dirname(__file__), '..' ,  constants.MODEL_DATA_PATH)
    
    # Import the module containing the variables
    spec = importlib.util.spec_from_file_location("model_data", model_data_path)
    model_data_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(model_data_module)
    
    # Access the variables
    return model_data_module.model_data

def write_model_data(encoded_columns, accuracy):
    file_path = os.path.join(os.path.dirname(__file__), '..', constants.MODEL_DATA_PATH)
    with open(file_path, 'w', encoding='utf-8') as file:
    # Write the array to the file as a Python variable assignment
        file.write('model_data = {')
        file.write(f'"encoded_columns" : {encoded_columns},\n')
        file.write(f'"accuracy" : {accuracy}\n')
        file.write("}")
    
