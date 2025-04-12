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
        xaxis_title=f"{ownership_type} īpatsvars (%)",
        yaxis_title='Apkaime',
        showlegend=False,
        margin=dict(l=100, r=20, t=50, b=100)
    )

    st.plotly_chart(fig)
    
def changes_in_area(districts, df, area):
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
