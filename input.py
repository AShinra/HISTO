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
    except Exception as e:
        st.error(f"Error accessing Google Sheet: {e}")
        
    with st.container(border=True):
        col1, col2 = st.columns(2, border=True)
        with col1:
            input_date = st.date_input('Date', key='i_date').isoformat()
            input_date = datetime.strptime(input_date, '%Y-%m-%d')
            input_date = input_date.strftime('%-m/%-d/%Y')
            # input_client = st.multiselect('Client', key='i_client', options=client_list)
            input_client = st.text_input('Client')
        with col2:
            input_tier = st.text_input('Tier')
            input_hyperlink = st.text_input('Hyperlink')

        data_area, col22 = st.columns([0.8, 0.2], border=True)
        with col22:
            b_add = st.button('Add' , key='input_archive', use_container_width=True)
            b_clear = st.button('Clear', use_container_width=True)
            b_delete = st.button('Delete', use_container_width=True)
            b_submit = st.button('Submit', use_container_width=True)

    if b_add:

        sheet.worksheet('TEMP').append_row([input_date, input_client, input_tier, input_hyperlink])
        with data_area:
            data = sheet.worksheet('TEMP').get_all_values()
            df1 = pd.DataFrame(data)
            df1.columns = df1.iloc[0]
            df1 = df1[1:]
            st.dataframe(df1)

    if b_submit:

        data = sheet.worksheet('TEMP').get_all_values()
        for idx, i in enumerate(data):
            if idx == 0:
                continue
            else:
                sheet.worksheet('ARCHIVE').append_row(i)
            

        sheet.worksheet('TEMP').batch_clear(["A2:D100"])


        with data_area:
            data = sheet.worksheet('TEMP').get_all_values()
            df1 = pd.DataFrame(data)
            df1.columns = df1.iloc[0]
            df1 = df1[1:]
            st.dataframe(df1)
        
        st.success('Added to Archives!!!')
    
    if b_clear:
        sheet.worksheet('TEMP').batch_clear(["A2:D100"])
        st.warning('Deleted all Entry!!!')

	

    return
