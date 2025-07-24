import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from datetime import datetime
import time

@st.cache_data
def get_data(_client):
    
    try:
        # client = get_gsheet_client()
        sheet_id = "1VVLZ0O3NncvMjex8gonkgPTfIKzkJh22UON55991_QE"
        sheet = _client.open_by_key(sheet_id)

        data = sheet.sheet1.get_all_values()

        df = pd.DataFrame(data)
        df.columns = df.iloc[0]
        df = df[1:]


    except Exception as e:
        st.error(f"Error accessing Google Sheet: {e}")

    return df


def archive(client):
    st.title("Archive Data")

    df = get_data(client)

    client_list = df['CLIENT NAME'].unique()
    client_list = sorted(client_list)    

    with st.container(border=True):
        col1, col2, col3, col4 = st.columns([0.15, 0.15, 0.15, 0.55], border=True)
        
        with col1:
            radio_options = st.radio(
                label='OPTIONS',
                options=['Off', 'All Dates', 'All Clients'],
                horizontal=False)
            
        with col2:
            captured_options = st.radio(
                label='CAPTURED',
                options=['Captured', 'Missed'],
                horizontal=False
            )
            
        with col3:
            _date = st.date_input('DATE', key='a_date').isoformat()
    
        with col4:
            _client = st.multiselect('CLIENT', key='a_client', options=client_list)
        
    
    
    b_search = st.button('Search' , key='search_archive', use_container_width=True)
        
     
    if b_search:

        with st.spinner(text="Reading Archives", show_time=False, width="content"):
            time.sleep(5)

            if radio_options == 'Off':
                if _client == []:
                    st.error('No Client/s Selected')
                else:
                    for cl in _client:

                        formatted_date_1 = datetime.strptime(_date, '%Y-%m-%d')
                        formatted_date_1 = formatted_date_1.strftime('%-m/%-d/%Y')

                        if captured_options == 'Captured':
                            filtered_df = df[(df['DATE'] == formatted_date_1) & (df['CLIENT NAME'] == cl) & (df['CAPTURED'] == 'Y')]
                        elif captured_options == 'Missed':
                            filtered_df = df[(df['DATE'] == formatted_date_1) & (df['CLIENT NAME'] == cl) & (df['CAPTURED'] == 'N')]

                        # st.write(formatted_date_1)
                        if filtered_df.shape[0] > 0:
                            selected_columns = filtered_df[['DATE', 'TIER', 'LINK']]
                            st.header(f'{cl} {captured_options} - {selected_columns.shape[0]}')
                            st.dataframe(selected_columns, use_container_width=True, hide_index=True)
                        elif filtered_df.shape[0] == 0:
                            st.error('No Data Found')

            elif radio_options == 'All Clients':

                formatted_date_1 = datetime.strptime(_date, '%Y-%m-%d')
                formatted_date_1 = formatted_date_1.strftime('%-m/%-d/%Y')

                # if captured_options == 'Captured':
                #     filtered_df = df[(df['DATE'] == formatted_date_1) & (df['CAPTURED'] == 'Y')]
                # elif captured_options == 'Missed':
                #     filtered_df = df[(df['DATE'] == formatted_date_1) & (df['CAPTURED'] == 'N')]
                
                filtered_df = df[(df['DATE'] == formatted_date_1)]
                new_cl = filtered_df['CLIENT NAME'].unique()

                for cl in new_cl:
                    with st.container(border=True):
                        
                        st.header(f'{cl}')

                        col_cap, col_mis = st.columns(2)

                        with col_cap:
                            captured_df = df[(df['DATE'] == formatted_date_1) & (df['CAPTURED'] == 'Y')]
                            cl_captured = captured_df[captured_df['CLIENT NAME']==cl]
                            sel_cl_captured = cl_captured[['DATE', 'TIER', 'LINK']]

                            st.subheader(f':green[Captured - {sel_cl_captured.shape[0]}]')

                            st.dataframe(sel_cl_captured, use_container_width=True, hide_index=True)
                        
                        with col_mis:
                            missed_df = df[(df['DATE'] == formatted_date_1) & (df['CAPTURED'] == 'N')]
                            cl_missed = missed_df[missed_df['CLIENT NAME']==cl]
                            sel_cl_missed = cl_missed[['DATE', 'TIER', 'LINK']]

                            st.subheader(f':red[Missed - {sel_cl_missed.shape[0]}]')

                            st.dataframe(sel_cl_missed, use_container_width=True, hide_index=True)                       
            
            elif radio_options == 'All Dates':
                if _client == []:
                    st.error('No Client/s Selected')
                else:
                    for cl in _client:

                        if captured_options == 'Captured':
                            filtered_df = df[(df['CLIENT NAME'] == cl) & (df['CAPTURED'] == 'Y')]
                        if captured_options == 'Missed':
                            filtered_df = df[(df['CLIENT NAME'] == cl) & (df['CAPTURED'] == 'N')]
                            
                        selected_columns = filtered_df[['DATE', 'TIER', 'LINK']]
                        st.header(f'{cl} {captured_options} - {selected_columns.shape[0]}')
                        st.dataframe(selected_columns, use_container_width=True, hide_index=True)
            
    return