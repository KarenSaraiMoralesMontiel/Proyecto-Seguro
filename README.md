# Proyecto de Pólizas de Seguro con Modelo Predictivo de Gastos Médicos y Análisis de Datos

## Overview

Esta aplicación de Streamlit contiene un modelo predictivo de gastos médicos y análisis de datos,
permite cambiar los párametros para hacer una predicción de gastos médicos (Tipo de cobertura, Modelo del coche, Año del coche, Valor Asegurado, Deductibles y el Estado del Seguro) de datos generados aleatoriamente.

## Access the Deployed App

Puede acceder a la aplicación en este link: [Predicción de Gastos Médicos](https://karensaraimoralesmontiel-proyecto-seguro-main-74lvwl.streamlit.app/)

## How to Use

Una vez que acceda a la aplicación, podrá interactuar con ella siguiendo los siguientes pasos: 

1. **Ajustar parámetros**: utilice los campos de entrada de la barra lateral para realizar una nueva predicción, como Tipo de Cobertura, Modelo del Coche, Año del coche, Valor asegurado, Deductible, Estado del Seguro y Daños a terceros.

2. **Haz predicción**: Haga click en el botón "Predecir" para hacer una predicción, la predicción se realiza con un modelo RandomForestClassifier.

3. **Explora Análisis**: Independientemente de la predicción se puede ver análisis de los datos como Siniestros por coche, Siniestros por mes, Valor Asegurado Promedio por Modelo del Coche acorde al Año del Coche, Análisis de Siniestros con un diagrama de Venn, un heatmap con la cuneta del Tipo de cobertura vs Estado del Seguro y el número de pólizas que iniciaro y se vencieron por Año-Mes.
## Screenshots

**Predicción Gastos Médicos**
![prediccion](https://github.com/KarenSaraiMoralesMontiel/Proyecto-Seguro/assets/62195892/65f853db-d488-4b22-aae9-b382209b38c7)

**Análisis De Datos**
![analisis](https://github.com/KarenSaraiMoralesMontiel/Proyecto-Seguro/assets/62195892/8ff9e093-fcfd-48c3-9b89-d844080353d4)

## Acknowledgments

- Este proyecto usa datos generados aleatoriamente.
- Este proyecto usa Streamlit para generar una aplicación web.


