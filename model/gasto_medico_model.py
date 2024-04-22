"""
gasto_medico_model.py
Este archivo contiene la clase de 
los gastos médicos del model
Autor: Karen Sarai Morales Montiel
Fecha de creación: 22/04/2024
"""
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pandas as pd
from common import utils

class Gastos_Medico_Model():
    def __init__(self, insurance_df):
        self.insurance_df = insurance_df
        self.encoded_columns = None
        self.model = None
        self.accuracy = None
        
    def modelar(self):
        df_encoded = pd.get_dummies(self.insurance_df.drop([ 'Número de póliza', 'Fecha de inicio', 'Fecha de vencimiento'], axis=1))
        
# División de datos en entrenamiento y prueba
        X = df_encoded.drop(columns=['Gastos médicos'], axis=1)
        y = df_encoded['Gastos médicos']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.encoded_columns = list(X.columns)

# Entrenamiento del modelo
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)

# Evaluación del modelo
        y_pred = self.model.predict(X_test)
        self.accuracy = accuracy_score(y_test, y_pred)
        
    
    
    def save_model(self):
        utils.write_model_data(self.encoded_columns, self.accuracy)
        utils.write_model(self.model)

    def get_accuracy(self):
        return self.accuracy
    
    def get_model(self):
        return self.model

import pandas as pd

data = {
    'Año del coche': [2010],
    'Valor asegurado': [10000],
    'Deducible': [500],
    'Daños a terceros': [False],
    'Tipo de cobertura_Cobertura amplia': [False],
    'Tipo de cobertura_Cobertura de colisión': [True],
    'Tipo de cobertura_Cobertura de robo': [False],
    'Tipo de cobertura_Cobertura total': [False],
    'Tipo de cobertura_Responsabilidad civil': [False],
    'Modelo del coche_Chevrolet Cruze': [False],
    'Modelo del coche_Ford Focus': [False],
    'Modelo del coche_Honda Civic': [False],
    'Modelo del coche_Hyundai Elantra': [True],
    'Modelo del coche_Kia Forte': [False],
    'Modelo del coche_Mazda 3': [False],
    'Modelo del coche_Nissan Sentra': [False],
    'Modelo del coche_Subaru Impreza': [False],
    'Modelo del coche_Toyota Corolla': [False],
    'Modelo del coche_Volkswagen Jetta': [True],
    'Estado del seguro_Al día': [True],
    'Estado del seguro_Vencido': [False]
}

df = pd.DataFrame(data)


insurance_df = utils.read_insurance_data()
modelo = Gastos_Medico_Model(insurance_df)
modelo.modelar()
modelo.save_model()
modelo = utils.read_model()
y = modelo.predict(df)
print(y)
