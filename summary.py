import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from datetime import datetime
import time
import altair as alt

def summary(client):

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

        df['DATE'] = pd.to_datetime(df['DATE'])
        df['MONTH_NAME'] = df['DATE'].dt.month_name()

        month_list = df['MONTH_NAME'].unique()
        count_month = df['MONTH_NAME'].value_counts(sort=False)               
        
        date_list = df['DATE'].unique()        

    except Exception as e:
        st.error(f"Error accessing Google Sheet: {e}")
    
    st.header('Monthly Breakdown')
    cola, colb = st.columns([0.3, 0.7], border=True)
    with cola:
        st.dataframe(count_month)
    with colb:
        st.header('')
        # st.bar_chart(count_month, use_container_width=True)
        bar_chart = alt.Chart(count_month).mark_bar().encode(
            x=alt.X('MONTH_NAME'),
            y=alt.Y('count'))
        st.altair_chart(bar_chart, use_container_width=True)
    
    st.header('Daily Breakdown')
    cola1, colb1 = st.columns([0.3, 0.7], border=True)
    with cola1:
        count_date = df['DATE'].value_counts(sort=False)
        st.dataframe(count_date)
    with colb1:
        st.header('')
        st.bar_chart(count_date, use_container_width=True)
    
    st.header('Client Breakdown')

    col1, col2 = st.columns(2, border=True)
    with col1:  
        c_list = st.multiselect('Select Client', options=client_list, help='Leave Blank to see all clients')
        button_select = st.button('Select')

        if button_select:
            with st.spinner(text="Preparing Data", show_time=True, width="content"):
                time.sleep(5)

                if c_list == []:
                    count_df = df['CLIENT NAME'].value_counts()                
                    st.dataframe(count_df)           
                else:
                    # filtered_df = df[df['CLIENT NAME'].isin(c_list)]
                    with col2:
                        for cl in c_list:
                            filtered_df = df[df['CLIENT NAME'] == cl]
                            count_df = filtered_df['CLIENT NAME'].value_counts()
                            date_df = filtered_df['DATE'].value_counts(sort=False)
                            with st.expander(f'Click to view breakdown for {cl}'):
                                st.dataframe(count_df)
                                st.dataframe(date_df)
                                st.bar_chart(date_df)
                            st.write('')

    
    # with col2:
    #     st.header('Missed per Date')
    #     count_date = df['DATE'].value_counts(sort=False)
    #     st.dataframe(count_date)
    #     st.bar_chart(count_date, use_container_width=True)

        



    return