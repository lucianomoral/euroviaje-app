import streamlit as st
import pandas as pd

df = pd.read_csv('euroviaje.csv', dtype='object')

st.title("Euroviaje!")

for index, row in df.iterrows():

    #col1, col2 = st.columns(2)
    #col1.image(row['Bandera'], width=40)

    st.markdown(
    f"""
        <div style="display: flex; align-items: center;">
            <img src="{row['Bandera']}" height="25" style="margin-right: 8px;">
            <span style="font-size: 18px; font-weight: 600;">{row['País']} - {row['Ciudad']}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.expander(f'Día {index+1} - {row['Fecha']}'):
        st.write(row['Actividad'])


