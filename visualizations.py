import plotly.express as px
import streamlit as st

def top_x(ownership_type, df, x, year):
    filtered = df[df['Īpašumtiesību veids'] == ownership_type]
    top_neighborhoods = filtered[filtered['Teritoriālā vienība'] != 'Rīga'].sort_values(by="% "+ year, ascending=False).head(x)
    fig = px.bar(top_neighborhoods, 
                 x="% "+ year, 
                 y='Teritoriālā vienība',
                 labels={'% {year}}': 'Īpašnieka apdzīvotu mājokļu īpatsvars (%)', 'Teritoriālā vienība': 'Apkaime'},
                 title=f'Top {x} apkaimes pēc {ownership_type} īpatsvara ({year})',
                 text="% "+ year,
                 orientation='h')

    fig.update_layout(
        xaxis_title='Īpašnieka apdzīvotu mājokļu īpatsvars (%)',
        yaxis_title='Apkaime',
        showlegend=False,
        margin=dict(l=100, r=20, t=50, b=100)
    )

    st.plotly_chart(fig)