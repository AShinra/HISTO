import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from datetime import datetime
import time


@st.cache_data
def load_data(_date, client, link):

    data = {'DATE':[], 'CLIENT':[], 'LINK':[]}

    data['DATE'].append(_date)


    return data


def input(client, client_list):

    data = {}

    st.title("Data Entry")


    try:
        sheet_id = "1VVLZ0O3NncvMjex8gonkgPTfIKzkJh22UON55991_QE"
        sheet = client.open_by_key(sheet_id)
        # data = sheet.worksheet('TEMP').get_all_values()

        # df1 = pd.DataFrame(data)
        # df1.columns = df1.iloc[0]
        # df1 = df1[1:]               
        

    except Exception as e:
        st.error(f"Error accessing Google Sheet: {e}")
        
    with st.container(border=True):
        
        col1, col2 = st.columns(2, border=True)
        
        with col1:
            input_date = st.date_input('Date', key='i_date').isoformat()
            # input_client = st.multiselect('Client', key='i_client', options=client_list)
            input_client = st.text_input('Client')
        with col2:
            input_tier = st.text_input('Tier')
            input_hyperlink = st.text_input('Hyperlink')
    
        b_add = st.button('Add to List' , key='input_archive', use_container_width=True)

    if b_add:

        sheet.worksheet('TEMP').append_row([input_date, input_client, input_tier, input_hyperlink])

        data = sheet.worksheet('TEMP').get_all_values()

        df1 = pd.DataFrame(data)
        df1.columns = df1.iloc[0]
        df1 = df1[1:]

        st.dataframe(df1)

        b_submit = st.button('Submit Data')

        if b_submit:
            sheet.worksheet('TEMP').update_cell(2,2, "")

	

    return
