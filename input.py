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

    st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1rem; /* Adjust this value as needed (e.g., 0rem for minimal padding) */
        padding-bottom: 0rem;
        padding-left: 5rem;
        padding-right: 5rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

    data = {}

    st.title(":violet[Data Entry]")

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
        
        fqdn_dict = {}
        # convert to dict
        for i, val in enumerate(fqdn_list):
            fqdn_dict[val] = tier_list[i]      
        
    except Exception as e:
        st.error(f"Error accessing Google Sheet: {e}")
        
    with st.container(border=True):
        col1, col2, col3 = st.columns([0.15, 0.7, 0.15], border=True)
        with col1:
            input_date = st.date_input(':calendar: Date', key='i_date', format='YYYY-MM-DD').isoformat()
            input_date = datetime.strptime(input_date, '%Y-%m-%d')
            input_date = input_date.strftime('%-m/%-d/%Y')            
            # input_tier = st.text_input('Tier')
            input_captured = st.selectbox(
                label='Captured',
                options=['Yes', 'No'],
                accept_new_options=False
            )
        with col2:
            input_client = st.text_input('Client', key='in_client')
            # input_hyperlink = st.text_input('Hyperlink')
            input_hyperlink = st.text_area('Hyperlink', key='in_hyperlink')
        with col3:
            b_add = st.button('Add' , key='input_archive', use_container_width=True)
            b_clear = st.button('Clear', use_container_width=True)
            b_delete = st.button('Delete', use_container_width=True)
            b_submit = st.button('Submit', use_container_width=True)

    if b_add:

        with st.spinner('Processing Data', show_time=True):
            time.sleep(15)
        
            if input_captured == 'Yes':
                captured = 'Y'
            elif input_captured == 'No':
                captured = 'N'

            _hyperlinks = input_hyperlink.splitlines()
            for _hyperlink in _hyperlinks:
                if _hyperlink not in ['', None]:
                    # get the tiering of the website
                    input_tier = 'Unlisted'
                    for k, v in fqdn_dict.items():
                        if k in _hyperlink:
                            input_fqdn = k
                            input_tier = v
                            break
                    
                    if input_tier == 'Unlisted':
                        _fqdn = _hyperlink.split('/')
                        _fqdn = _fqdn[2]
                        if _fqdn[:4] == 'www.':
                            input_fqdn = _fqdn[4:]
                        else:
                            input_fqdn = _fqdn
                    try:    
                        sheet.worksheet('TEMP').append_row([input_date, input_client.upper(), input_tier, _hyperlink, captured, input_fqdn])
                    # except Exception as e:
                    #     st.error(f"Error accessing Google Sheet: {e}")
                    except:
                        pass
                    else:
                        # get fqdn unlisted data
                        fqdn_unlisted = sheet.worksheet('UNLISTED').get_all_values()
                        df_fqdn_unli = pd.DataFrame(fqdn_unlisted)
                        df_fqdn_unli.columns = df_fqdn_unli.iloc[0]
                        df_fqdn_unli = df_fqdn_unli[1:]
                        unlisted_list = df_fqdn_unli['FQDN'].to_list()

                        if input_tier == 'Unlisted' and input_fqdn not in unlisted_list:
                            sheet.worksheet('UNLISTED').append_row([input_fqdn])

            with st.container(border=True):
                try:
                    data = sheet.worksheet('TEMP').get_all_values()
                except:
                    st.error('API Connection Error')
                else:
                    df1 = pd.DataFrame(data)
                    df1.columns = df1.iloc[0]
                    df1 = df1[1:]
                    st.dataframe(df1)

    if b_submit:

        with st.spinner('Processing Data', show_time=True):
            time.sleep(15)

            data = sheet.worksheet('TEMP').get_all_values()
            for idx, i in enumerate(data):
                if idx == 0:
                    continue
                else:
                    sheet.worksheet('ARCHIVE').append_row(i)
                

            sheet.worksheet('TEMP').batch_clear(["A2:F100"])
            
            data = sheet.worksheet('TEMP').get_all_values()
            df1 = pd.DataFrame(data)
            df1.columns = df1.iloc[0]
            df1 = df1[1:]
            st.dataframe(df1)
            
            st.success('Added to Archives!!!')
    
    if b_clear:

        with st.spinner('Processing Data', show_time=True):
            time.sleep(15)

            sheet.worksheet('TEMP').batch_clear(["A2:F100"])
            st.warning('Deleted all Entry!!!')

	

    return
