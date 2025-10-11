import streamlit as st
import pandas as pd

def page_itinerario():

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

        with st.expander(f'Destino {row['DestinoId']} - Desde:{row['Desde']} hasta:{row['Hasta']} '):

            st.header('Datos generales')

            df_tmp = df[ df['DestinoId'] == row['DestinoId'] ]

            general = df_tmp[columns_destino_short].drop_duplicates()

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

def page_presupuesto():
    st.title("Presupuesto:")

    presupuesto_total = 3500
    cantidad_noches = 23
    
    
    df = pd.read_csv('gastos.csv', encoding='utf-8')

    presupuesto_consumido = df['Pagado'].sum()
    presupuesto_comprometido = df['Pendiente'].sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Presupuesto total", f"{presupuesto_total} USD", border=True)
    col2.metric("Pagado", f"{presupuesto_consumido} USD", border=True)
    col3.metric("Comprometido a pagar", f"{presupuesto_comprometido} USD", border=True)
    col4.metric("Restante por noche", f"{round((presupuesto_total - presupuesto_consumido) / cantidad_noches, 2)} USD", border=True)


    st.dataframe(df)

pg = st.navigation([
    st.Page(page_itinerario, title="Itinerario", icon="📝"),
    st.Page(page_presupuesto, title="Presupuesto", icon="💰"),
])

pg.run()