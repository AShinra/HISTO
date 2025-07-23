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

        df['DATE'] = pd.to_datetime(df['DATE'])
        df['MONTH_NAME'] = df['DATE'].dt.month_name()
        df['YEAR'] = df['DATE'].dt.year

        year_list = df['YEAR'].unique()

        client_list = df['CLIENT NAME'].unique()
        client_list = sorted(client_list)
        client_list.insert(0, 'ALL')

        # st.dataframe(df_captured)

    except Exception as e:
        st.error(f"Error accessing Google Sheet: {e}")
    
    st.header('Monthly Breakdown')
    cola, colb = st.columns([0.3, 0.7], border=True)
    with cola:
        
        client_selection_mb = st.selectbox(
            label='Client',
            options=client_list
        )

        if client_selection_mb != 'ALL':
            df_clientfiltered = df[df['CLIENT NAME'] == client_selection_mb]
        else:
            df_clientfiltered = df

        cola1, cola2 = st.columns(2)

        with cola1:
            cap_option = st.radio(
                label='Options',
                options=['Captured', 'Missed'],
                horizontal=True
            )
        
        with cola2:
            year_selected = st.selectbox(
                label='YEAR',
                options=year_list)

        if cap_option == 'Captured':
            df_captured = df_clientfiltered[df_clientfiltered['CAPTURED'] == 'Y']
        if cap_option == 'Missed':
            df_captured = df_clientfiltered[df_clientfiltered['CAPTURED'] == 'N']


    with colb:
        colb1, colb2 = st.columns([0.3, 0.7])
        with colb1:
            monthcount = df_captured['MONTH_NAME'].value_counts(sort=False)
            df_monthcount = monthcount.to_frame()
            df_monthcount = df_monthcount.reset_index()        
            st.dataframe(df_monthcount, hide_index=True)
        with colb2:
            _chart1 = alt.Chart(df_monthcount, title=alt.TitleParams(f'Monthly {cap_option} Breakdown', anchor='middle')).mark_bar().encode(
                x=alt.X('MONTH_NAME', sort=None, title='Month'),
                y=alt.Y('count', title='Count'))
            st.write(_chart1)
        
        colb11, colb22 = st.columns([0.3, 0.7])
        with colb11:
            countdate = df_captured['DATE'].value_counts(sort=False)
            df_countdate = countdate.to_frame()
            df_countdate = df_countdate.reset_index()
            st.dataframe(df_countdate, hide_index=True)
        with colb22:
            _chart2 = alt.Chart(df_countdate, title=alt.TitleParams(f'Daily {cap_option} Breakdown', anchor='middle')).mark_bar().encode(
                    x=alt.X('DATE', sort=None, title='Date'),
                    y=alt.Y('count', title='Count'))
            st.write(_chart2)
    
    st.header('Daily Breakdown')
    cola1, colb1 = st.columns([0.3, 0.7], border=True)
    with colb1:
        st.header('')
        # st.bar_chart(countdate, use_container_width=True, x_label='Date', y_label='Count', color=["#f35b09"])


    
    

    st.header('Client Breakdown')

    col1, col2 = st.columns(2, border=True)
    with col1:  
        c_list = st.multiselect('Select Client', options=client_list, help='Leave Blank to see all clients')
        button_select = st.button('Select')

        if button_select:
            with st.spinner(text="Preparing Data", show_time=True, width="content"):
                time.sleep(5)

                if c_list == []:
                    with col2:
                        count_df = df_captured['CLIENT NAME'].value_counts()                
                        st.dataframe(count_df)           
                else:
                    # filtered_df = df[df['CLIENT NAME'].isin(c_list)]
                    with col2:
                        for cl in c_list:
                            filtered_df = df[df['CLIENT NAME'] == cl]
                            count_df = filtered_df['CLIENT NAME'].value_counts()
                            date_df = filtered_df['DATE'].value_counts(sort=False)
                            with st.expander(f'Click to view breakdown for {cl}'):
                                with st.container(border=True):
                                    st.dataframe(count_df)
                                with st.container(border=True):
                                    st.dataframe(date_df)
                                with st.container(border=True):
                                    st.bar_chart(date_df, x_label='Date', y_label='Count')
                            st.write('')

        
        # with col2:
        #     st.header('Missed per Date')
        #     count_date = df['DATE'].value_counts(sort=False)
        #     st.dataframe(count_date)
        #     st.bar_chart(count_date, use_container_width=True)

        



    return