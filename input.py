import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from datetime import datetime
import time




def input(client, client_list):

    st.title("Data Entry")

    with st.container(border=True):
        
        col1, col2 = st.columns(2, border=True)
        
        with col1:
            input_date = st.date_input('Date', key='i_date').isoformat()
            input_date_all = st.checkbox('All', help='Selects all Dates for selected Client/s')
        
        with col2:
            input_client = st.multiselect('Client', key='i_client', options=client_list)
    
        b_search = st.button('Search' , key='search_archive', use_container_width=True)



    return