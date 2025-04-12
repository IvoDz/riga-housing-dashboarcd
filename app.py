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
        'Izvēlieties datu kopu',
        options=['Īpašumtiesību veids', 'Īpašumu veids', 'Platība uz vienu iedzīvotāju']
    )

    if csv_selection == 'Īpašumtiesību veids':
        st.header('Īpašumtiesību veidi:')
        st.dataframe(df_owner)
    elif csv_selection == 'Īpašumu veids':
        st.header('Īpašumu veidi:')
        st.dataframe(df_type)
    elif csv_selection == 'Platība uz vienu iedzīvotāju':
        st.header('Platība uz vienu iedzīvotāju:')
        st.dataframe(df_area)
else:
    chart_type = st.sidebar.radio(
        'Vizualizācijas veidi:',
        options=['Īpašumtiesību veids', 'Īpašumu veids', 'Platība uz vienu iedzīvotāju']
    )

    st.header(f"{chart_type}")
    
    if chart_type == 'Īpašumtiesību veids':
        top = st.number_input("Apkaimju skaits", 2, 20, value=5)
        ownership_type = st.selectbox("Īpašumtiesību veids", ["Īpašnieka apdzīvoti mājokļi", "Īres mājokļi", "Citu īpašumtiesību veidu mājokļi"])
        year_option = st.radio(
            'Gads:',
            options=['2011', '2021',]
        )
        
        st.header(f"Top {top} apkaimju pēc {ownership_type} mājokļu skaita ({year_option})")
        visualizations.top_x(ownership_type, df_owner, top, year_option)