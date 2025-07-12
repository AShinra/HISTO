import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from datetime import datetime
import time

def summary(client):

    st.title("SUMMARY")
    
    try:
        # client = get_gsheet_client()
        sheet_id = "1VVLZ0O3NncvMjex8gonkgPTfIKzkJh22UON55991_QE"
        sheet = client.open_by_key(sheet_id)

        data = sheet.sheet1.get_all_values()

        df = pd.DataFrame(data)
        df.columns = df.iloc[0]
        df = df[1:]

        client_list = df['CLIENT NAME'].unique()
        client_list = sorted(client_list)

        date_list = df['DATE'].unique()

    except Exception as e:
        st.error(f"Error accessing Google Sheet: {e}")
    

    col1, col2 = st.columns(2, border=True)

    with col1:
        st.header('Client Misses')
        client_df = df['CLIENT NAME'].value_counts()
        st.multiselect('Select Client', options=client_list)
    
    with col2:
        st.header('Missed per Date')
        st.dataframe(df['DATE'].value_counts(sort=False))



    return