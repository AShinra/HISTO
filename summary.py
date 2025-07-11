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
    

    # for cl in client_list:
    #     st.write(cl)
    #     cl_count = (df['CLIENT NAME'] == cl).value_counts()
    #     st.write(f'{cl} - {cl_count}')

    st.dataframe(df['CLIENT NAME'].value_counts())



    return