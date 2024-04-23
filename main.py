"""
main.py
Este archivo contiene la clase de Análisis de Datos.
Autor: Karen Sarai Morales Montiel
Fecha de creación: 20/04/2024
"""
import common.utils as utils
import streamlit as st
import pandas as pd
from streamlit_echarts import st_pyecharts,st_echarts
from streamlit_echarts import JsCode
import matplotlib.pylab as plt
from pyecharts import options as opts
from pyecharts.charts import Bar

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
        coches_siniestros_bar = self.siniestros_modelo_carro()
        self.line_race_valor_asegurado()
        st_pyecharts(coches_siniestros_bar, key="Coches Siniestros")
        option = self.line_race_valor_asegurado()
        st_echarts(options=option, height="600px")
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
    
    def siniestros_modelo_carro(self) -> Bar:
        def apply_siniestros(gastos_medico, daños_terceros):
            if (gastos_medico == 1 or daños_terceros == 1):
                return "yes"
            return "no"

        coches_siniestros = self.insurance_data_df

        coches_siniestros["Siniestros"] = coches_siniestros[["Gastos médicos", "Daños a terceros"]].apply(lambda row: apply_siniestros(row["Gastos médicos"], row["Daños a terceros"]), axis=1)
        

        coches_siniestros = pd.crosstab(index=coches_siniestros['Siniestros'],
                                    columns=coches_siniestros['Modelo del coche'])
        coches_siniestros = coches_siniestros.T.sort_values('yes', ascending=False)
        x_axis  = list(coches_siniestros.index)
        y_axis = list(coches_siniestros.yes)
        
        b = (
            Bar()
            .add_xaxis(x_axis)
            .add_yaxis("Siniestros",y_axis)
            .set_global_opts(
                title_opts=opts.TitleOpts(
                title="Siniestros por coche", subtitle="Count of Games"
        ),
        toolbox_opts=opts.ToolboxOpts(),
            )
        )
        return b
        
    def line_race_valor_asegurado(self):
        cars = ['Toyota Corolla', 
                'Honda Civic', 
                'Ford Focus', 
                'Chevrolet Cruze', 
                'Nissan Sentra',
               'Hyundai Elantra', 
               'Volkswagen Jetta', 
               'Kia Forte', 
               'Mazda 3', 
               'Subaru Impreza']
        
        
        raw_data = utils.read_valor_asegurado_promedio()
        
        datasetWithFilters = [
        {
        "id": f"dataset_{car}",
        "fromDatasetId": "dataset_raw",
        "transform": {
            "type": "filter",
            "config": {
                "and": [
                    {"dimension": "Year", "gte": 2010},
                    {"dimension": "Car Model", "=": car},
                    ]
                },
            },
        }
        for car in cars
        ]

        seriesList = [
        {
        "type": "line",
        "datasetId": f"dataset_{car}",
        "showSymbol": False,
        "name": car,
        "endLabel": {
            "show": True,
            "formatter": JsCode(
                "function (params) { return params.value[0] + ': ' + params.value[2];}"
            ).js_code,
            },
        "labelLayout": {"moveOverlap": "shiftY"},
        "emphasis": {"focus": "series"},
        "encode": {
            "x": "Year",
            "y": "Insurance Value",
            "label": ["Model Car", "Insurance Value"],
            "itemName": "Year",
            "tooltip": ["Insurance Value"],
            },
        }
        for car in cars
        ]

        option = {
        "animationDuration": 10000,
        "dataset": [{"id": "dataset_raw", "source": raw_data}] + datasetWithFilters,
        "title": {"text": "Valor Asegurado"},
        "tooltip": {"order": "valueDesc", "trigger": "axis"},
        "xAxis": {"type": "category", "nameLocation": "middle"},
        "yAxis": {"name": "Insurance Value"},
        "grid": {"right": 140},
        "series": seriesList,
    }
        return option

        
    

sales_df = utils.read_insurance_data()
    
app = StreamlitApp(sales_df)
app.build_app()