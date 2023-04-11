import streamlit as st
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns


@st.cache
def load_data(nrows=500):
    employees = pd.read_csv("Employees (2).csv", nrows=nrows)
    return employees

@st.cache
def search_employee(df, employee_id=None, hometown=None, unit=None):
    if employee_id:
        df = df[df['Employee_ID'] == employee_id]
    if hometown:
        df = df[df['Hometown'] == hometown]
    if unit:
        df = df[df['Unit'] == unit]
    return df

@st.cache
def filter_by_education(df, education_level):
    return df[df['Education_Level'] == education_level]

@st.cache
def filter_by_city(df, city):
    return df[df['Hometown'] == city]

@st.cache
def filter_by_unit(df, unit):
    return df[df['Unit'] == unit]

employees = load_data()

st.title("Aplicación Web de RETO 5")
st.header("Análisis de Empleados")
st.write("Esta aplicación analiza un conjunto de datos de empleados.")

sidebar = st.sidebar

show_dataframe = sidebar.checkbox("Mostrar dataframe completo", False)

if show_dataframe:
    st.write(employees)

employee_id = st.text_input("Buscar por Employee_ID")
hometown = st.text_input("Buscar por Hometown")
unit = st.text_input("Buscar por Unit")
search_button = st.button("Buscar")

if search_button:
    results = search_employee(employees, employee_id, hometown, unit)
    st.write(f"Total de empleados encontrados: {len(results)}")
    st.write(results)

education_level = sidebar.selectbox("Filtrar por nivel educativo", ["Ninguno"] + employees["Education_Level"].unique().tolist())

if education_level != "Ninguno":
    filtered_df = filter_by_education(employees, education_level)
    st.write(f"Total de empleados con nivel educativo '{education_level}': {len(filtered_df)}")
    st.write(filtered_df)

city = sidebar.selectbox("Filtrar por ciudad", ["Ninguna"] + employees["Hometown"].unique().tolist())

if city != "Ninguna":
    filtered_df = filter_by_city(employees, city)
    st.write(f"Total de empleados en '{city}': {len(filtered_df)}")
    st.write(filtered_df)

unit = sidebar.selectbox("Filtrar por unidad funcional", ["Ninguna"] + employees["Unit"].unique().tolist())

if unit != "Ninguna":
    filtered_df = filter_by_unit(employees, unit)
    st.write(f"Total de empleados en la unidad '{unit}': {len(filtered_df)}")
    st.write(filtered_df)

st.header("Histograma de empleados por edad")
plt.hist(employees["Age"], bins='auto')
plt.xlabel("Edad")
plt.ylabel("Frecuencia")
st.pyplot(plt.gcf())

st.header("Frecuencia de empleados por unidad funcional")
sns.countplot(data=employees, x='Unit')
plt.xlabel("Unidad Funcional")
plt.ylabel("Frecuencia")
st.pyplot(plt.gcf())

st.header("Ciudades con mayor índice de deserción")
desertion_by_city = employees.groupby("Hometown")["Attrition_rate"].sum().reset_index()
plt.bar(desertion_by_city["Hometown"], desertion_by_city["Attrition_rate"])
plt.xlabel("Ciudad")
plt.ylabel("Índice de Deserción")
plt.xticks(rotation=45)
st.pyplot(plt.gcf())

st.header("Edad y tasa de deserción")
age_desertion = employees.groupby("Age")["Attrition_rate"].mean().reset_index()
plt.plot(age_desertion["Age"], age_desertion["Attrition_rate"])
plt.xlabel("Edad")
plt.ylabel("Tasa de Deserción")
st.pyplot(plt.gcf())

st.header("Relación entre tiempo de servicio y tasa de deserción")
service_time_desertion = employees.groupby("Time_of_service")["Attrition_rate"].mean().reset_index()
plt.plot(service_time_desertion["Time_of_service"], service_time_desertion["Attrition_rate"])
plt.xticks(rotation=90)
plt.xlabel("Tiempo de Servicio")
plt.ylabel("Tasa de Deserción")
st.pyplot(plt.gcf())
