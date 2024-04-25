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
        """Hace el modelo de gastos médicos
        """
        df_encoded = pd.get_dummies(self.insurance_df.drop([ 'Número de póliza', 'Fecha de inicio', 'Fecha de vencimiento'], axis=1))
        
#        División de datos en entrenamiento y prueba
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
        """Guarda el model y los datos del modelo
        """
        utils.write_model_data(self.encoded_columns, self.accuracy)
        utils.write_model(self.model)

    def get_accuracy(self):
        """Devuelve la exactitud del modelo

        Returns:
            float: Exactitud del modelo
        """
        return self.accuracy
    
    def get_model(self):
        """Devuelve el modelo

        Returns:
            model: Modelo de gastos médicos
        """
        return self.model
