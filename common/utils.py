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
import json
from pprint import pprint


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
    
def read_valor_asegurado_promedio():
    file_path = os.path.join(os.path.dirname(__file__), '..', constants.VALOR_ASEGURADO_JSON_PATH)
    with open(file_path) as f:
        raw_data = json.load(f)
    return raw_data

def write_valor_asegurado_promedio():
    file_path = os.path.join(os.path.dirname(__file__), '..', constants.VALOR_ASEGURADO_JSON_PATH)
    insurance_data_df = read_insurance_data()
    valor_asegurado_promedio = insurance_data_df.groupby(['Modelo del coche', "Año del coche"])['Valor asegurado'].mean().reset_index().sort_values("Año del coche")
    columns = ["Car Model", "Year" , "Insurance Value"]
    data = [columns]

# Iterate through each row of the DataFrame and append it to the data list
    for index, row in valor_asegurado_promedio.iterrows():
        data.append(row.tolist())

# Write the JSON data to a file
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file)

def apply_siniestros(gastos_medico, daños_terceros):
    if (gastos_medico == 1 or daños_terceros == 1):
        return "yes"
    return "no"

def apply_month(fecha):
    month = str(fecha).split("-")[1]
    return month

def change_month(month):
  months = {
      1: "Enero",
      2: "Febrero",
      3: "Marzo",
      4: "Abril",
      5: "Mayo",
      6: "Junio",
      7: "Julio",
      8: "Agosto",
      9: "Septiembre",
      10: "Octubre",
      11: "Noviembre",
      12:"Diciembre"
  }
  return months[int(month)]

def read_siniestros_json():
    file_path = os.path.join(os.path.dirname(__file__), '..', constants.SINIESTROS_VENN_DATA_JSON_PATH)
    with open(file_path, "r") as file:
        siniestros_venn = json.load(file)
    return siniestros_venn

def write_siniestros_json():
    file_path = os.path.join(os.path.dirname(__file__), '..', constants.SINIESTROS_VENN_DATA_JSON_PATH)
    insurance_data_df = read_insurance_data()
    
    polizas_medicos = insurance_data_df.loc[insurance_data_df['Gastos médicos'] == 1, 'Número de póliza']
    polizas_terceros = insurance_data_df.loc[insurance_data_df['Daños a terceros'] == 1, 'Número de póliza']
    
    data = {
        "Gastos medicos": list(polizas_medicos),
        "Terceros" : list(polizas_terceros)
    }
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file)

write_siniestros_json()
    

    