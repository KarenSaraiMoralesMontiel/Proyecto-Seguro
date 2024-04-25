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

def read_insurance_data() -> pd.DataFrame:
    """Devuelve el archivo de insurance_data.csv que contiene
    todas las polizas
    Returns:
        pd.DataFrame: DataFrame con las polizas
    """
    file_path = os.path.join(os.path.dirname(__file__), '..', constants.INSURANCE_DATA_PATH)
    return pd.read_csv(file_path)

def write_insurance_data(insurance_df: pd.DataFrame):
    """Escribe el dataframe de las polizas en el archivo insurance_Df

    Args:
        insurance_df (pd.DataFrame): DataFrame que contiene las polizas con las columnas
        Número de póliza,Fecha de inicio,Fecha de vencimiento,}
        Tipo de cobertura,Modelo del coche,Año del coche,
        Valor asegurado,Deducible,Estado del seguro,Gastos médicos,Daños a terceros

        
    """
    file_path = os.path.join(os.path.dirname(__file__), '..', constants.INSURANCE_DATA_PATH)
    insurance_df.to_csv(file_path, index=False)


def read_model() :
    """Devuelve el modelo de Gastos medicos

    Returns:
        model: Modelo de Gastos médicos
    """
    file_path = os.path.join(os.path.dirname(__file__), '..' , constants.GASTOS_MEDICOS_MODEL_PATH)
    return joblib.load(file_path)

def write_model(model):
    """Escribe el modelo en un archivo pkl en 
    common/model/gastos_medicos_model.pkl

    Args:
        model (Model): Modelo de Gastos médicos
    """
    file_path = os.path.join(os.path.dirname(__file__), '..' , constants.GASTOS_MEDICOS_MODEL_PATH)
    joblib.dump(model, file_path)

    
def read_model_data() -> dict:
    """Devuelve un diccionario con los datos del modelo

    Returns:
        dict: Diccionario que contiene encoded columns 
        que tiene las columnas necesarias para la predicción
        y accuracy que contiene la exactitud del modelo
    """
    model_data_path = os.path.join(os.path.dirname(__file__), '..' ,  constants.MODEL_DATA_PATH)
    
    # Import the module containing the variables
    spec = importlib.util.spec_from_file_location("model_data", model_data_path)
    model_data_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(model_data_module)
    
    # Access the variables
    return model_data_module.model_data

def write_model_data(encoded_columns : list, accuracy: float):
    """Escribe los datos del modelo de gastos médicos en un diccionario
    en common/model/model_data.py

    Args:
        encoded_columns (list): Columnas necesarias para hacer la predicción.
        accuracy (float): Exactitud del modelo
    """
    file_path = os.path.join(os.path.dirname(__file__), '..', constants.MODEL_DATA_PATH)
    with open(file_path, 'w', encoding='utf-8') as file:
    # Write the array to the file as a Python variable assignment
        file.write('model_data = {')
        file.write(f'"encoded_columns" : {encoded_columns},\n')
        file.write(f'"accuracy" : {accuracy}\n')
        file.write("}")
    
def read_valor_asegurado_promedio() -> dict:
    """Devueve el diccionario con los datos de
    los valores asegurado promedio por modelo de 
    coche a lo largo de los años

    Returns:
        dict: Diccionario que contiene el valor min para 
        la gráfica y data que contiene los datos
    """
    file_path = os.path.join(os.path.dirname(__file__), '..', constants.VALOR_ASEGURADO_JSON_PATH)
    with open(file_path) as f:
        raw_data = json.load(f)
    return raw_data

def write_valor_asegurado_promedio():
    """Saca los valores asegurados promedio de los modelos de coche acorde
    al año del coche.y los guarda en el archivo common/data/json/valor_asegurado.json
    """
    #Hace el file_path
    file_path = os.path.join(os.path.dirname(__file__), '..', constants.VALOR_ASEGURADO_JSON_PATH)
    insurance_data_df = read_insurance_data()
    #Agrupa los valores acorde al Modelo del coche, Año del coche y saca el promedio del valor asegurado y 
    #ordena los valores acorde al Año del coche
    valor_asegurado_promedio = insurance_data_df.groupby(['Modelo del coche', "Año del coche"])['Valor asegurado'].mean().reset_index().sort_values("Año del coche")
    #Columnas de los valores
    columns = ["Car Model", "Year" , "Insurance Value"]
    #Se guarda las columnas en una variable llamada data
    data = [columns]
    #Ponemos un min_value grande para encontrar el valor mínimo para la 
    #gráfica
    min_value = 100000

    # Itera por cada línea
    for index, row in valor_asegurado_promedio.iterrows():
        #Append el valor de la línea como una lista
        data.append(row.tolist())
        #Busca el valor mínimo
        if min_value > row[2]:
            min_value = row[2]
    #Saca el siguiente valor minimo 1000
    min_value = ((min_value // 1000) *1000) - 1000
    #Asigna los valos en el diccionario
    json_file_dict = {
        "min" : min_value,
        "data" : data
    }
    # Escribe los valores al archivo JSON
    with open(file_path, 'w') as json_file:
        json.dump(json_file_dict, json_file)

def read_siniestros_json() -> dict:
    """Devuelve el diccionario en
    common/data/json/siniestros_venn.json

    Returns:
        dict: Diccionario con listas de polizas "Sin Siniestros", "Gastos médicos"
        y "Daños a terceros"
    """
    file_path = os.path.join(os.path.dirname(__file__), '..', constants.SINIESTROS_VENN_DATA_JSON_PATH)
    with open(file_path, "r") as file:
        siniestros_venn = json.load(file)
    return siniestros_venn

def write_siniestros_json():
    """Escribe el diccionario con las listas de pólizas 
    "Sin Siniestros", "Gastos médicos", "Daños a terceros"
    en common/data/json/siniestros_venn.json
    """
    file_path = os.path.join(os.path.dirname(__file__), '..', constants.SINIESTROS_VENN_DATA_JSON_PATH)
    insurance_data_df = read_insurance_data()
    #Saca las polizas
    poliza_sin_siniestros = insurance_data_df.loc[(insurance_data_df['Gastos médicos'] == 0) & (insurance_data_df['Daños a terceros'] == 0), 'Número de póliza']
    polizas_medicos = insurance_data_df.loc[insurance_data_df['Gastos médicos'] == 1, 'Número de póliza']
    polizas_terceros = insurance_data_df.loc[insurance_data_df['Daños a terceros'] == 1, 'Número de póliza']
    
    #Guarda las polizas como listas en diccionario
    data = {
        "Sin Siniestros" : list(poliza_sin_siniestros),
        "Gastos medicos": list(polizas_medicos),
        "Terceros" : list(polizas_terceros)
    }
    #Los guarda en el archivo
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file)

def write_heatmap_coberturas_json():
    """Escrive los datos para el heatmap de estados de seguro vs coberturas
    """
    file_path = os.path.join(os.path.dirname(__file__), '..', constants.HEATMAP_COBERTURAS_SEGUROS_JSON)
    insurance_data_df = read_insurance_data()
    #Saca los valores
    df_2dhist = pd.DataFrame({
    x_label: grp['Estado del seguro'].value_counts()
    for x_label, grp in insurance_data_df.groupby('Tipo de cobertura')
})
    #Obtiene listas con los estados y las coberturas
    estados = list(df_2dhist.index)
    coberturas = list(df_2dhist.columns)

    #Inicializa los valores min_count, max_count (para el mapa visual)
    min_count = 10000
    max_count = 0
    #Lista con los valores, el heamap va de abajo hacia arriba y de izquierda a deracha
    data = []
    #Inicializa el valor x
    x = 0
    #Va por cada línea del dataframe
    for _, row in reversed(list(df_2dhist.iterrows())):
        #Inicializa un valor y
        y = 0
        # Itera por cada línea
        for _, value in row.items():
            #Appen los valores en la lista
            data.append([y, x, value])
            #Busca los valores minimum y máximos
            #para el mapa visual
            if (min_count > value):
                min_count = value
            if (max_count < value):
                max_count = value
            #El contador y suma 1
            y += 1
        #El contador x suma
        x += 1
    #Transforma el valor máximo y minimo para el
    #mapa visual
    max_count = (max_count // 100) *100 + 100
    min_count = (min_count // 100) *100
    
    #Hace el diccionario
    json_data = {
        "max_count" : max_count,
        "min_count" : min_count,
        "estados" : estados,
        "coberturas" : coberturas,
        "data": data
    }
    #Guarda el diccionario
    with open(file_path, 'w', encoding="utf-8") as json_file:
        json.dump(json_data, json_file, ensure_ascii=False)
    

def read_heatmap_coberturas_json() -> dict:
    """Devuelve el diccionario con los datos del heatmap

    Returns:
        dict: Diccionario con los datos para el heatmap
        max_count, min_count (para el mapa visual)
        estados, coberturas (x, y)
        data (datos para el heatmap)
    """
    file_path = os.path.join(os.path.dirname(__file__), '..', constants.HEATMAP_COBERTURAS_SEGUROS_JSON)
    with open(file_path, "r") as file:
        heatmap_coberturas = json.load(file)
    return heatmap_coberturas

def apply_siniestros(gastos_medico, daños_terceros) -> str:
    """Devuelve si hubo siniestros

    Args:
        gastos_medico (int): Valor 0,1 
        da (int): Valor 0,1

    Returns:
        str: Devuelve "yes" or "no"
    """
    if (gastos_medico == 1 or daños_terceros == 1):
        return "yes"
    return "no"

def apply_month(fecha):
    """Consigue el número del mes

    Args:
        fecha (datetime.datetime): Fecha

    Returns:
        str: Número del mes
    """
    month = str(fecha).split("-")[1]
    return month

def change_month(month):
    """Devuelve el nombre del mes

    Args:
        month (str): Número del mes

    Returns:
        str: Nombre del mes
    """
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