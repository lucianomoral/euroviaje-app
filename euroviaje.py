import streamlit as st
import pandas as pd

st.set_page_config(layout = 'wide')

itinerario_database_file = 'https://drive.google.com/uc?export=download&id=1xR8Ygg6BqKaolKi_u89TnEpa87Kiy39o'

presupuesto_database_file = 'https://drive.google.com/uc?export=download&id=17o5-D_nBg2HbDgQ93mtroeahqMn9_Uhy'

@st.cache_data
def load_database_file(database_file):
    df = pd.read_csv(database_file, dtype='object', encoding='utf-8')
    return df

def page_itinerario():

    df = load_database_file(itinerario_database_file)

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

    cantidad_noches = 23

    df = load_database_file(presupuesto_database_file)

    estados= list(df['Estado'].drop_duplicates())

    estados.append('Todos')
    estados.append('No pagado o pago parcial')

    st.sidebar.header("Filtros")
    status_filter = st.sidebar.radio(
        "Estado:",
        options=estados
    )

    st.title("Presupuesto")
    #st.subheader(f"Presupuesto original: {presupuesto_total} USD")
    presupuesto_total = st.slider(label='Para ajustar presupuesto, mover el slider:', value=3500, min_value=3500, max_value=5000)
    st.subheader(f"Presupuesto original: {presupuesto_total} USD (Cantidad de noches: {cantidad_noches})")

    presupuesto_consumido = df['Pagado'].astype(int).sum()  
    presupuesto_comprometido = df['Pendiente'].astype(int).sum()
    restante_por_noche = round((presupuesto_total - presupuesto_consumido - presupuesto_comprometido) / cantidad_noches, 2)

    col1, col2, col3 = st.columns(3)
    col1.metric(label="Pagado", value=f"{presupuesto_consumido} USD", delta="Gastos ya pagados", delta_color="off", border=True)
    col2.metric(label="Comprometido a pagar", value=f"{presupuesto_comprometido} USD", delta="Gastos ya realizados, pero aún no pagados", delta_color="off", border=True)
    col3.metric(label="Restante por noche", value=f"{restante_por_noche} USD", delta="(Total - Pagado - Por pagar) / Cant. de noches", delta_color="off", border=True)


    if status_filter == 'No pagado o pago parcial':
        df = df[df['Estado'].isin(['No pagado', 'Pago parcial'])]
    elif status_filter != 'Todos':
        df = df[df['Estado'] == status_filter]

    df = df[['Fecha de pago pendiente', 'Pagado por', 'Descripcion', 'Pagado', 'Pendiente', 'Monto total', 'Categoria', 'Estado']]

    df['Fecha de pago pendiente'] = pd.to_datetime(df['Fecha de pago pendiente'])

    df['Periodo'] = df['Fecha de pago pendiente'].dt.to_period('M')

    df = df.sort_values(by='Fecha de pago pendiente')

    grouped = df.groupby('Periodo')

    for period, group in grouped:
        pagado = group['Pagado'].astype(int).sum()  
        pendiente = group['Pendiente'].astype(int).sum()
        with st.expander(f"{period.strftime('%B %Y')} || Pagado: {pagado} USD || Pendiente: {pendiente} USD"):
            st.dataframe(group.drop(columns=['Periodo', 'Fecha de pago pendiente']))

    #st.dataframe(df)

pg = st.navigation([
    st.Page(page_itinerario, title="Itinerario", icon="📝"),
    st.Page(page_presupuesto, title="Presupuesto", icon="💰"),
])

pg.run()