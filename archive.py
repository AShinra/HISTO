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
        col1, col2, col3 = st.columns(3, border=True)
        
        with col1:
            _date = st.date_input('Date', key='a_date').isoformat()
    
        
        with col2:
            _client = st.multiselect('Client', key='a_client', options=client_list)
            # _date_all = st.checkbox('All Dates', help='Selects all Dates for selected Client/s')

        with col3:
            st.radio(
                label='Options',
                options=['Off', 'All Dates', 'All Clients'],
                horizontal=False)
    
    
    b_search = st.button('Search' , key='search_archive', use_container_width=True)
        
     
    if b_search:

        with st.spinner(text="Reading Archives", show_time=False, width="content"):
            time.sleep(5)



            # if _client != []:
            #     for cl in _client:

            #         formatted_date_1 = datetime.strptime(_date, '%Y-%m-%d')
            #         formatted_date_1 = formatted_date_1.strftime('%-m/%-d/%Y')

            #         if _date_all:
            #             filtered_df = df[(df['CLIENT NAME'] == cl)]
            #         else:
            #             filtered_df = df[(df['DATE'] == formatted_date_1) & (df['CLIENT NAME'] == cl)]
                    
            #         if filtered_df.shape[0] > 0:
            #             selected_columns = filtered_df[['DATE', 'TIER', 'LINK']]
            #             st.header(cl)
            #             st.dataframe(selected_columns, use_container_width=True, hide_index=True)
            #         elif filtered_df.shape[0] == 0:
            #             st.error('No Data Found')

            # elif _client == []:
            #     st.error('Select a client from the list')

    return