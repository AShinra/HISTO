import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from datetime import datetime
import time


def archive(client):
    st.title("Archive Data")

    
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

    except Exception as e:
        st.error(f"Error accessing Google Sheet: {e}")

    with st.container(border=True):
        col1, col2, col3 = st.columns([0.15, 0.25, 0.6], border=True)
        
        with col1:
            radio_options = st.radio(
                label='OPTIONS',
                options=['Off', 'All Dates', 'All Clients'],
                horizontal=False)
            
        with col2:
            _date = st.date_input('DATE', key='a_date').isoformat()
    
        with col3:
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
                     
                        filtered_df = df[(df['DATE'] == formatted_date_1) & (df['CLIENT NAME'] == cl)]
                        
                        st.header(cl)
                        st.write(formatted_date_1)
                        if filtered_df.shape[0] > 0:
                            selected_columns = filtered_df[['DATE', 'TIER', 'LINK']]
                            st.dataframe(selected_columns, use_container_width=True, hide_index=True)
                        elif filtered_df.shape[0] == 0:
                            st.error('No Data Found')

            elif radio_options == 'All Clients':

                formatted_date_1 = datetime.strptime(_date, '%Y-%m-%d')
                formatted_date_1 = formatted_date_1.strftime('%-m/%-d/%Y')

                filtered_df = df[(df['DATE'] == formatted_date_1)]
                
                new_cl = filtered_df['CLIENT NAME'].unique()

                for cl in new_cl:
                    st.header(cl)
                    new_df = filtered_df[filtered_df['CLIENT NAME'] == cl]
                    selected_columns = new_df[['DATE', 'TIER', 'LINK']]
                    st.dataframe(selected_columns, use_container_width=True, hide_index=True)
                    
            
            elif radio_options == 'All Dates':
                if _client == []:
                    st.error('No Client/s Selected')
                else:
                    for cl in _client:
                        st.header(cl)
                        filtered_df = df[df['CLIENT NAME'] == cl]
                        selected_columns = filtered_df[['DATE', 'TIER', 'LINK']]
                        st.dataframe(selected_columns, use_container_width=True, hide_index=True)

                    



            


            
    return