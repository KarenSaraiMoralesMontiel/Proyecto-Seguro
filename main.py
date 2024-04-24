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
from matplotlib_venn import venn3      

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
        st_pyecharts(coches_siniestros_bar, key="Coches Siniestros")
        
        mes_siniestros_bar = self.siniestros_por_mes()
        st_pyecharts(mes_siniestros_bar, key="Mes Siniestros")

        option = self.line_race_valor_asegurado()
        st_echarts(options=option, height="600px")
        
        #json_data = utils.read_siniestros_json()
        venn_diagram = self.plot_venn_diagram()
        st.pyplot(venn_diagram)
        
        
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


        coches_siniestros = self.insurance_data_df

        coches_siniestros["Siniestros"] = coches_siniestros[["Gastos médicos", "Daños a terceros"]].apply(lambda row: utils.apply_siniestros(row["Gastos médicos"], row["Daños a terceros"]), axis=1)
        

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
                title="Siniestros por coche", subtitle="Count of Siniestros"
        ),
        toolbox_opts=opts.ToolboxOpts(),
            )
        )
        return b
    
    def siniestros_por_mes(self) -> Bar:
        mes_siniestros = self.insurance_data_df.copy()

        # Create a new column "Siniestros" by applying a custom function to "Gastos médicos" and "Daños a terceros" columns
        mes_siniestros["Siniestros"] = mes_siniestros[["Gastos médicos", "Daños a terceros"]].apply(lambda row: utils.apply_siniestros(row["Gastos médicos"], row["Daños a terceros"]), axis=1)

        # Extract month information from "Fecha de inicio" column and create a new column "Mes Siniestros"
        mes_siniestros["Mes Siniestros"] = pd.to_datetime(mes_siniestros["Fecha de inicio"]).dt.month

        # Compute a cross-tabulation of "Mes Siniestros" and "Siniestros" to count occurrences of different types of claims for each month
        mes_siniestros = pd.crosstab(index=mes_siniestros['Mes Siniestros'], columns=mes_siniestros['Siniestros']).sort_index()

        # Map month names using the `utils.change_month` function (assuming it's defined correctly)
        mes_siniestros.index = mes_siniestros.index.map(utils.change_month)
        x_axis = list(mes_siniestros.index)
        y_axis = list(mes_siniestros.yes)
        b = (
            Bar()
            .add_xaxis(x_axis)
            .add_yaxis("Siniestros",y_axis, color="#9facd8")
            .set_global_opts(
                title_opts=opts.TitleOpts(
                title="Siniestros por mes", subtitle="Count of Siniestros"
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
    
    def plot_venn_diagram(self):
        # Load data from JSON
        data = utils.read_siniestros_json()
        
        # Create figure and axis
        fig, ax = plt.subplots()
        
        
        # Create Venn diagram
        venn3([set(data["Sin Siniestros"]), set(data["Gastos medicos"]), set(data["Terceros"])], ('', '', ''))
        
        ax.legend(handles=[plt.Rectangle((0,0),1,1,color='#99CC99', alpha=0.5),
                           plt.Rectangle((0,0),1,1,color='#9999FF', alpha=0.5),
                           plt.Rectangle((0,0),1,1,color='#FF9999', alpha=0.5)],
                  labels=['Gastos médicos', 'Daños a terceros', 'Sin Siniestros'],
                  loc='upper left',
                  bbox_to_anchor=(1, 1))
        plt.title("Análisis de Siniestros")
        return fig
        
    

sales_df = utils.read_insurance_data()
    
app = StreamlitApp(sales_df)
app.build_app()