import streamlit as st
import pandas as pd
import time

st.title('Presupuesto')

df = pd.read_csv('test.csv')

fecha = st.sidebar.selectbox('Fecha', df['Fecha'])

left_column, right_column, last_column = st.columns(3)

with left_column:
    st.table(df[ df['Fecha'] == fecha ] )

with right_column:
    x = st.slider('x')
    st.write(x, 'squared is', x * x)


'Starting a long computation...'

# Add a placeholder
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
  # Update the progress bar with each iteration.
  latest_iteration.text(f'Iteration {i+1}')
  bar.progress(i + 1)
  time.sleep(0.1)

'...and now we\'re done!'

st.html('<p>HOLAAAA</p>')
