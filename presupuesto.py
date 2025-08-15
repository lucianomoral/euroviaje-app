#from streamlit_extras.styllable_container import styllable_container
import streamlit as st

st.markdown('<style>.st-column: {background-color: "red"}</style>', unsafe_allow_html=True)

row1 = st.columns(2)

with row1[0]:
    cont = st.container(border=True, vertical_alignment='center')
    cont.write('Alquiler')
    cont.button('Agregar gasto', key='alq')

with row1[1]:
    cont = st.container(border=True, vertical_alignment='center')
    cont.write('Servicios')
    cont.button('Agregar gasto', key='serv')