import streamlit as st
import pandas as pd

df = pd.read_csv('euroviaje2.csv', dtype='object')

columns_destino = ['DestinoId', 'DestinoNombre', 'DestinoBandera', 'Desde', 'Hasta', 'Cantidad de noches', 'Dias completos', 'Comentario']
columns_destino_short = ['Desde', 'Hasta', 'Cantidad de noches', 'Dias completos', 'Comentario']

columns_eventos = ['DestinoId','TipoEvento','Detalle','Código','Precio original','Precio USD','Estado','Fecha','Dirección','Link1','Link2','Comentarios']

destinos = df[columns_destino].drop_duplicates()

st.title("Euroviaje!")

for index, row in destinos.iterrows():

    st.markdown(
    f"""
        <div style="display: flex; align-items: center;">
            <img src="{row['DestinoBandera']}" height="25" style="margin-right: 8px;">
            <span style="font-size: 18px; font-weight: 600;">{row['DestinoNombre']}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.expander(f'Destino {index+1} - Desde:{row['Desde']} hasta:{row['Hasta']} '):

        st.header('Datos generales')

        df_tmp = df[ df['DestinoId'] == row['DestinoId'] ]

        general = df_tmp[columns_destino_short] 

        general = general.T

        st.table(general)

        for tipoEvento in df_tmp['TipoEvento'].drop_duplicates():

            st.header(tipoEvento)

            details = df_tmp[columns_eventos]

            details = details[ details['TipoEvento'] == tipoEvento ]

            del(details['DestinoId'])
            del(details['TipoEvento'])

            details = details.T

            st.table(details)