import plotly.express as px
import streamlit as st
import pandas as pd

def top_x(df):
    top = st.number_input("Apkaimju skaits", 2, 30, value=5)
    ownership_type = st.selectbox("Īpašumtiesību veids", ["Īpašnieka apdzīvoti mājokļi", "Īres mājokļi", "Citu īpašumtiesību veidu mājokļi"])
    year = st.radio(
            'Gads:',
            options=['2011', '2021',]
        )
        
    st.header(f"Top {top} apkaimju pēc {ownership_type} skaita ({year})")
    
    
    filtered = df[df['Īpašumtiesību veids'] == ownership_type]
    top_neighborhoods = filtered[filtered['Teritoriālā vienība'] != 'Rīga'].sort_values(by="% "+ year, ascending=False).head(top)
    fig = px.bar(top_neighborhoods, 
                 x="% "+ year, 
                 y='Teritoriālā vienība',
                 labels={'% {year}}': 'Īpašnieka apdzīvotu mājokļu īpatsvars (%)', 'Teritoriālā vienība': 'Apkaime'},
                 title=f'Top {top} apkaimes pēc {ownership_type} īpatsvara ({year})',
                 text="% "+ year,
                 orientation='h')

    fig.update_layout(
        xaxis_title=f"{ownership_type} īpatsvars (%)",
        yaxis_title='Apkaime',
        showlegend=False,
        margin=dict(l=100, r=20, t=50, b=100)
    )

    st.plotly_chart(fig)
    
def changes_in_area(df):
    districts = st.multiselect(
        'Izvēlieties apkaimes',
        options=df['Teritoriālā vienība'].unique(),
        default=['Ziepniekkalns', 'Teika', 'Grīziņkalns']
    )
    
    area = st.selectbox(
        'Platības kategorija uz vienu iedzīvotāju',
        options=df['Dzīvojamā platība uz vienu iemītnieku'].unique()
    )

    subset = df[
        (df['Teritoriālā vienība'].isin(districts)) & 
        (df['Dzīvojamā platība uz vienu iemītnieku'] == area)
    ]
    
    subset_melted = subset.melt(
        id_vars='Teritoriālā vienība',
        value_vars=['2011', '2021'],
        var_name='Gads',
        value_name='Skaits'
    )
    
    fig = px.line(
        subset_melted,
        x='Gads',
        y='Skaits',
        color='Teritoriālā vienība',
        markers=True,
        title=f"Izmaiņas platībai: {area} uz vienu iemītnieku"
    )
    
    for _, row in subset_melted.iterrows():
        fig.add_annotation(
            x=row['Gads'],
            y=row['Skaits'],
            text=f"{row['Skaits']}",
            showarrow=False,
            font=dict(size=9),
            align='center',
            yshift=5
        )
    
    fig.update_layout(
        xaxis_title="Gads",
        yaxis_title="Iedzīvotāju skaits",
        margin=dict(t=40, b=40, l=40, r=40),
        height=500
    )
    
    st.plotly_chart(fig)

def housing_type(df):
    selected_ter = st.selectbox("Izvēlies teritoriālo vienību", sorted(df['Teritoriālā vienība'].unique()))
    selected_veids = st.selectbox("Izvēlies mājokļu veidu", sorted(df['Dzīvojamo telpu veids'].unique()))

    filtered = df[
        (df['Teritoriālā vienība'] == selected_ter) &
        (df['Dzīvojamo telpu veids'] == selected_veids)
    ]

    data = {
        "Gads": ["2011", "2021", "2011", "2021"],
        "Lielums": ["Apdzīvoti mājokļi", "Apdzīvoti mājokļi", "Personas", "Personas"],
        "Skaits": [
            filtered["Apdzīvoti mājokļi 2011"].values[0],
            filtered["Apdzīvoti mājokļi 2021"].values[0],
            filtered["Mājokļos dzīvojošās personas 2011"].values[0],
            filtered["Mājokļos dzīvojošās personas 2021"].values[0]
        ]
    }
    df_long = pd.DataFrame(data)

    fig = px.bar(
        df_long, x="Lielums", y="Skaits", color="Gads",
        barmode="group", title=f"{selected_ter} – {selected_veids}"
    )
    st.plotly_chart(fig, use_container_width=True)