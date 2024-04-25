"""
generate_data.py
Este archivo contiene el generador 
de datos para el proyecto.
Autor: Karen Sarai Morales Montiel
Fecha de creación: 20/04/2024
"""
import pandas as pd # type: ignore
import numpy as np
import datetime
import random
from common import utils

class Generador_Datos():
    def __init__(self, n_cases = 10000):
        random.seed(42)
        #Número de casos
        self.n_cases= n_cases
        #El dataframe que va a contener los datos
        self.df = None
        #Fecha, minima el 1/01/2020 hasta el 31/12/2025
        self.start_date_coverage = datetime.datetime(2020, 1, 1)
        self.end_date_coverage = datetime.datetime(2025, 12, 31)
        # Tipos de cobertura
        self.coverage_types = ['Responsabilidad civil', 'Cobertura total', 'Cobertura de colisión', 'Cobertura amplia', 'Cobertura de robo']
        # Modelos de coches y probabilidades de ocurrencia
        self.car_models = ['Toyota Corolla', 'Honda Civic', 'Ford Focus', 'Chevrolet Cruze', 'Nissan Sentra',
              'Hyundai Elantra', 'Volkswagen Jetta', 'Kia Forte', 'Mazda 3', 'Subaru Impreza']
        self.car_probabilities = [0.2, 0.15, 0.12, 0.1, 0.08, 0.1, 0.08, 0.07, 0.05, 0.05]
    
    def generate_random_date(self, start_date=datetime.datetime(2020, 1, 1), end_date=datetime.datetime(2025, 12, 31)) -> datetime.datetime:
        """_summary_

        Args:
            start_date (_type_, optional): Fecha de minima de inicio. Defaults to datetime.datetime(2020, 1, 1).
            end_date (_type_, optional): Fecha máxima de inicio. Defaults to datetime.datetime(2025, 12, 31).

        Returns:
            datetime.datetime: Fecha random de inicio
        """
        days_difference = (end_date - start_date).days
        random_day = start_date + datetime.timedelta(days=random.randint(0, days_difference))
        return random_day
    
    def generate_data(self):
        """Genera los datos y los almacena en 
        """
        data = {}
        data['Número de póliza'] = [f"P00000{i}" for i in range(self.n_cases)]
        data['Fecha de inicio'] = [self.generate_random_date() for _ in range(self.n_cases)]
        data['Fecha de vencimiento'] = [(start_date + datetime.timedelta(days=365)) for start_date in data['Fecha de inicio']]
        data['Tipo de cobertura'] = np.random.choice(self.coverage_types, self.n_cases)
        data['Modelo del coche'] = np.random.choice(self.car_models, self.n_cases, p=self.car_probabilities)
        data['Año del coche'] = np.random.randint(2010, 2023, size=self.n_cases)
        data['Valor asegurado'] = [np.random.randint(10000,50000) for _ in range (self.n_cases)]
        data['Deducible'] = np.random.choice([500,600,700], self.n_cases)
        data['Estado del seguro'] = np.random.choice(["Al día", "Vencido"], self.n_cases)
        data['Gastos médicos'] = np.random.choice([0,1], self.n_cases)
        data['Daños a terceros'] = np.random.choice([0,1], self.n_cases)
# Crear DataFrame
        self.df = pd.DataFrame(data)

    def get_data(self) -> pd.DataFrame:
        """Devuelve el dataframe de los datos

        Returns:
            pd.DataFrame: El DataFrame de los datos
        """
        return self.df
    def save_data(self):
        """Guarda los datos en un csv dentro de la carpeta common
        """
        utils.write_insurance_data(self.df)
        utils.write_valor_asegurado_promedio()
        utils.write_siniestros_json()
        utils.write_heatmap_coberturas_json()
