import streamlit as st
import pandas as pd

def calculate_total_sales(df):
    return df['Sales'].sum()

st.title("Sales Dashboard")

# Initialize DataFrame in session state
if 'sales_data' not in st.session_state:
    st.session_state.sales_data = pd.DataFrame({
        'Product': ['Laptop', 'Mouse', 'Keyboard'],
        'Sales': [1200, 50, 75]
    })

# Display and allow editing of the DataFrame
edited_df = st.data_editor(st.session_state.sales_data, key="sales_editor")

# Update session state with the edited DataFrame
st.session_state.sales_data = edited_df

# Calculate and display the updated metric
total_sales = calculate_total_sales(st.session_state.sales_data)
st.metric(label="Total Sales", value=f"${total_sales:,.2f}")