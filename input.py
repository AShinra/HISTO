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
        for i in sheet:
            st.write(i)

        # data = sheet.sheet1.get_all_values()
        # data = sheet.sheet1.get_all_values()
        # st.write(data)

    except Exception as e:
        st.error(f"Error accessing Google Sheet: {e}")
        
    with st.container(border=True):
        
        col1, col2 = st.columns(2, border=True)
        
        with col1:
            input_date = st.date_input('Date', key='i_date').isoformat()
        
        with col2:
            input_client = st.multiselect('Client', key='i_client', options=client_list)
        
        input_hyperlink = st.text_input('Hyperlink')
    
        b_add = st.button('Add to List' , key='input_archive', use_container_width=True)

    # if b_add:

    #     data = load_data(input_date, input_client, input_hyperlink)

    #     df = pd.DataFrame(data)

    #     st.dataframe(df)



    return
