"""
main.py
Este archivo contiene la clase de Análisis de Datos.
Autor: Karen Sarai Morales Montiel
Fecha de creación: 20/04/2024
"""
import common.model.model_data as model_data
import common.utils as utils
import streamlit as st
import pandas as pd
from pprint import pprint

class StreamlitApp():
    def __init__(self, insurance_data_df):
        self.insurance_data_df = insurance_data_df
        self.modelo = utils.read_model()
        self.model_data = utils.read_model_data()
        
    
    def build_app(self):
        st.title('Predicción de Gastos Médicos')
        st.write('Ingrese los detalles del seguro para predecir si habrá gastos médicos.')

# Formulario de entrada de datos
        form = st.form(key='insurance_form')
        coverage_type = form.selectbox('Tipo de cobertura', self.insurance_data_df['Tipo de cobertura'].unique())
        car_model = form.selectbox('Modelo del coche', self.insurance_data_df['Modelo del coche'].unique())
        car_year = form.number_input('Año del coche', min_value=2010, max_value=2022)
        insured_value = form.number_input('Valor asegurado', min_value=10000, max_value=50000)
        deductible = form.select_slider('Deducible', options=[500, 600, 700])
        insurance_state = form.selectbox('Estado del seguro', ['Al día', 'Vencido'])
        third_party_damage = form.select_slider('Daños a terceros', options=[0, 1])
        submit_button = form.form_submit_button(label='Predecir')
        if submit_button:
                input = {
                        "Tipo de cobertura" : [coverage_type],
                        "Modelo del coche" : [car_model],
                        "Año del coche" : [car_year],
                        "Valor asegurado" : [insured_value],
                        "Deducible" : [deductible],
                        "Estado del seguro" : [insurance_state],
                        "Daños a terceros" : [third_party_damage]
                }
                input_encoded = self.transform_data(input)
                prediction = self.modelo.predict(input_encoded)
                # Assuming self.message(prediction[0]) returns a string
                prediction_message = self.message(prediction[0])

                # Write the message with Markdown formatting for centering and increasing font size
                st.write(f"<div style='text-align: center; font-size: 24px;'>{prediction_message}</div>", unsafe_allow_html=True)
    
    def transform_data(self, input_data):
        try:
            data = pd.DataFrame(input_data)
            data_encoded = pd.get_dummies(data)
        
            # Ensure all columns from encoded_columns are present
            missing_cols = set(self.model_data["encoded_columns"]) - set(data_encoded.columns)
            for col in missing_cols:
                data_encoded[col] = False
        
            # Reorder columns
            data_encoded = data_encoded[self.model_data["encoded_columns"]]
        
            # Convert binary encoded values to True/False
            for col in self.model_data["encoded_columns"][3:]:
                data_encoded[col] = data_encoded[col].astype(bool)
        
            return data_encoded
    
        except Exception as e:
            print("An error occurred during data transformation:", e)
            return None
    
    def message(self, prediction):
        if (prediction):
            return "Si, van a haber gastos médicos"
        return "No, no van a haber gastos médictos"
            
        
sales_df = utils.read_insurance_data()
    
app = StreamlitApp(sales_df)
app.build_app()