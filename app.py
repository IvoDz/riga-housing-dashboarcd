import pandas as pd
import streamlit as st
import visualizations

@st.cache_data
def load_data():
    df_area = pd.read_csv('data/area.csv', sep=';')
    df_type = pd.read_csv('data/type.csv', sep=';')
    df_owner = pd.read_csv('data/ownership.csv', sep=';') 
    return df_area, df_type, df_owner

df_area, df_type, df_owner = load_data()

st.title('Rīgas mājokļu datu informācijas panelis')

st.sidebar.header('Filtri')

data_selection = st.sidebar.radio(
    'Skatīt datus vai vizualizācijas',
    options=['Dati (CSV)', 'Vizualizācijas']
)

if data_selection == 'Dati (CSV)':
    csv_selection = st.sidebar.radio(
        'Datu kopa',
        options=['Īpašumtiesību veids', 'Īpašumu veids', 'Platība uz vienu iedzīvotāju']
    )

    if csv_selection == 'Īpašumtiesību veids':
        st.header('Īpašumtiesību veidi')
        st.dataframe(df_owner)
    elif csv_selection == 'Īpašumu veids':
        st.header('Īpašumu veidi')
        st.dataframe(df_type)
    elif csv_selection == 'Platība uz vienu iedzīvotāju':
        st.header('Platība uz vienu iedzīvotāju')
        st.dataframe(df_area)
else:
    chart_type = st.sidebar.radio(
        'Vizualizācijas veidi',
        options=['Īpašumtiesību veids', 'Īpašumu veids', 'Platība uz vienu iedzīvotāju']
    )

    st.header(f"{chart_type}")
    
    if chart_type == 'Īpašumtiesību veids':
        visualizations.top_x(df_owner)
        
    if chart_type == 'Platība uz vienu iedzīvotāju':
        visualizations.changes_in_area(df_area)
    
    if chart_type == 'Īpašumu veids':
        visualizations.housing_type(df_type)