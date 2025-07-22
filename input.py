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

        # get fqdn tiering data
        fqdn_temp = sheet.worksheet('TIER').get_all_values()
        df_fqdn = pd.DataFrame(fqdn_temp)
        df_fqdn.columns = df_fqdn.iloc[0]
        df_fqdn = df_fqdn[1:]

        # convert to list
        fqdn_list = df_fqdn['FQDN'].to_list()
        tier_list = df_fqdn['TIER'].to_list()

        # convert to dict
        for i, val in enumerate(fqdn_list):
            st.write(f'{i} - {val}')
        
        
    except Exception as e:
        st.error(f"Error accessing Google Sheet: {e}")
        
    with st.container(border=True):
        col1, col2, col3 = st.columns([0.15, 0.7, 0.15], border=True)
        with col1:
            input_date = st.date_input('Date', key='i_date', format='YYYY-MM-DD').isoformat()
            input_date = datetime.strptime(input_date, '%Y-%m-%d')
            input_date = input_date.strftime('%-m/%-d/%Y')
            # input_client = st.multiselect('Client', key='i_client', options=client_list)
            input_tier = st.text_input('Tier')
            input_captured = st.selectbox(
                label='Captured',
                options=['Yes', 'No'],
                accept_new_options=False
            )
        with col2:
            input_client = st.text_input('Client')
            # input_hyperlink = st.text_input('Hyperlink')
            input_hyperlink = st.text_area('Hyperlink')
        with col3:
            b_add = st.button('Add' , key='input_archive', use_container_width=True)
            b_clear = st.button('Clear', use_container_width=True)
            b_delete = st.button('Delete', use_container_width=True)
            b_submit = st.button('Submit', use_container_width=True)

    if b_add:
        
        if input_captured == 'Yes':
            captured = 'Y'
        elif input_captured == 'No':
            captured = 'N'

        _hyperlinks = input_hyperlink.splitlines()
        for _hyperlink in _hyperlinks:
            if _hyperlink not in ['', None]:
                # get the tiering of the website
                

                sheet.worksheet('TEMP').append_row([input_date, input_client, input_tier, _hyperlink, captured])

        with st.container(border=True):
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
            

        sheet.worksheet('TEMP').batch_clear(["A2:E100"])
        
        data = sheet.worksheet('TEMP').get_all_values()
        df1 = pd.DataFrame(data)
        df1.columns = df1.iloc[0]
        df1 = df1[1:]
        st.dataframe(df1)
        
        st.success('Added to Archives!!!')
    
    if b_clear:
        sheet.worksheet('TEMP').batch_clear(["A2:E100"])
        st.warning('Deleted all Entry!!!')

	

    return
