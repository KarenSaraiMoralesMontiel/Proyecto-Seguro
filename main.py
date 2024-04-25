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

        valor_option = self.line_race_valor_asegurado()
        st_echarts(options=valor_option, height="600px")
        
        #json_data = utils.read_siniestros_json()
        venn_diagram = self.plot_venn_diagram()
        st.pyplot(venn_diagram)
        
        heatmap_options = self.plot_heatmap_cobertura_seguro()
        st_echarts(options=heatmap_options, height="600px")
        
        policies_options = self.policies_analysis()
        st_echarts(policies_options, height="600px")
        
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
        
        dict = utils.read_valor_asegurado_promedio()
        raw_data = dict["data"]
        min_insurance_value = int(dict["min"])
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
        "yAxis": {"name": "Insurance Value", "min":min_insurance_value},
        "grid": {"right": 140},
        "series": seriesList,
    }
        return option
    
    def plot_venn_diagram(self):
        # Load data from JSON
        data = utils.read_siniestros_json()
        
        # Create figure and axis
        fig, ax = plt.subplots(figsize=(8, 8))  # Increase figure size
        
        # Create Venn diagram
        venn3([set(data["Sin Siniestros"]), set(data["Gastos medicos"]), set(data["Terceros"])], 
              set_labels=('', '', ''),
              set_colors=('#FF9999', '#99CC99', '#9999FF'))
        
        # Add legend
        ax.legend(handles=[plt.Rectangle((0,0),1,1,color='#99CC99', alpha=0.5),
                           plt.Rectangle((0,0),1,1,color='#9999FF', alpha=0.5),
                           plt.Rectangle((0,0),1,1,color='#FF9999', alpha=0.5)],
                  labels=['Gastos médicos', 'Daños a terceros', 'Sin Siniestros'],
                  loc='upper left',
                  bbox_to_anchor=(1, 1))
        
        plt.title("Análisis de Siniestros")
        return fig
    
    def plot_heatmap_cobertura_seguro(self):
        heatmap_data = utils.read_heatmap_coberturas_json()
        coberturas = heatmap_data["coberturas"]
        estados = heatmap_data["estados"]
        data = heatmap_data["data"]
        max_count = heatmap_data["max_count"]
        min_count = heatmap_data["min_count"]
        option = {
    "title": {"text": "Tipo de cobertura vs Estado del seguro"},
    "tooltip": {"position": "top"},
    "grid": {"height": "50%", "top": "10%"},
    "xAxis": {"type": "category", "data": coberturas},
    "yAxis": {"type": "category", "data": estados, "splitArea": {"show": True}},
    "visualMap": {
        "min": min_count,
        "max": max_count,
        "calculable": True,
        "orient": "horizontal",
        "left": "center",
        "bottom": "15%",
    },
    "series": [
        {
            "name": "Punch Card",
            "type": "heatmap",
            "data": data,
            "label": {"show": True},
            "emphasis": {
                "itemStyle": {"shadowBlur": 10, "shadowColor": "rgba(0, 0, 0, 0.5)"}
            },
        }
    ],
}   
        return option

    def policies_analysis(self):
        df = self.insurance_data_df
        df['Fecha de inicio'] = pd.to_datetime(df['Fecha de inicio'])
        df['Fecha de vencimiento'] = pd.to_datetime(df['Fecha de vencimiento'])

        # Extract year-month from the 'Fecha de inicio' and 'Fecha de vencimiento' columns and convert to string
        df['Inicio Year-Month'] = df['Fecha de inicio'].dt.strftime('%Y-%m')
        df['Vencimiento Year-Month'] = df['Fecha de vencimiento'].dt.strftime('%Y-%m')

        # Group data by year-month and count the number of policies for 'Fecha de inicio'
        inicio_policy_count = df.groupby('Inicio Year-Month').size().reset_index(name='Inicio Count')

        # Group data by year-month and count the number of policies for 'Fecha de vencimiento'
        vencimiento_policy_count = df.groupby('Vencimiento Year-Month').size().reset_index(name='Vencimiento Count')

        # Create ECharts options with different colors for each series
        options = {
    "title": {"text": "Number of Policies by Year-Month"},
    "xAxis": {"type": "category", "data": inicio_policy_count['Inicio Year-Month'].tolist()},
    "yAxis": {"type": "value"},
    "tooltip": {
        "trigger": "item",
        "formatter": "Fecha de {a} ({b})<br />Count: <strong>{c}</strong>",
    },  # Customize tooltip format to show series name and count
    "series": [
        {
            "name": "inicio",
            "type": "line",
            "data": inicio_policy_count[['Inicio Year-Month', 'Inicio Count']].values.tolist(),
            "itemStyle": {"color": "#4682B4"},  # Set color for line of 'Fecha de inicio'
            "connectNulls": True,  # Connect null values with lines
        },
        {
            "name": "vencimiento",
            "type": "line",
            "data": vencimiento_policy_count[['Vencimiento Year-Month', 'Vencimiento Count']].values.tolist(),
            "itemStyle": {"color": "#FFA500"},  # Set color for line of 'Fecha de vencimiento'
            "connectNulls": True,  # Connect null values with lines
        },
    ],
}
        return options
        

insurance_data_df = utils.read_insurance_data()
    
app = StreamlitApp(insurance_data_df)
app.build_app()