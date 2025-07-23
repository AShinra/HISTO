import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from datetime import datetime
import time
import altair as alt

def summary(client):

    st.header('Summary')

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
    
    st.header('')
    cola, colb = st.columns([0.3, 0.7], border=True)
    with cola:
        
        # client selection
        client_selection = st.selectbox(
            label='Client',
            options=client_list
        )

        if client_selection != 'ALL':
            df_clientfiltered = df[df['CLIENT NAME'] == client_selection]
        else:
            df_clientfiltered = df

        cola1, cola2 = st.columns(2)

        with cola1:
            cap_option = st.radio(
                label='Options',
                options=['Captured', 'Missed', 'Request'],
                horizontal=False
            )
        
        with cola2:
            year_selected = st.selectbox(
                label='YEAR',
                options=year_list)

        if cap_option=='Captured':
            df_captured = df_clientfiltered[df_clientfiltered['CAPTURED'] == 'Y']
        elif cap_option=='Missed':
            df_captured = df_clientfiltered[df_clientfiltered['CAPTURED'] == 'N']
        elif cap_option=='Request':
            df_captured = df_clientfiltered


    with colb:
        colb1, colb2 = st.columns([0.3, 0.7])
        with colb1:
            monthcount = df_captured['MONTH_NAME'].value_counts(sort=False)
            df_monthcount = monthcount.to_frame()
            df_monthcount = df_monthcount.reset_index()
            st.dataframe(df_monthcount, hide_index=True)
        with colb2:
            _chart1 = alt.Chart(df_monthcount, title=alt.TitleParams(f'Monthly {cap_option}', anchor='middle')).mark_bar().encode(
                x=alt.X('MONTH_NAME', sort=None, title='Month'),
                y=alt.Y('count', title='Count'))
            st.write(_chart1)
        
        st.divider()
        
        colb11, colb22 = st.columns([0.3, 0.7])
        with colb11:
            countdate = df_captured['DATE'].value_counts(sort=False)
            df_countdate = countdate.to_frame()
            df_countdate = df_countdate.reset_index()
            st.dataframe(df_countdate, hide_index=True)
        with colb22:
            _chart2 = alt.Chart(df_countdate, title=alt.TitleParams(f'Daily {cap_option}', anchor='middle')).mark_bar().encode(
                    x=alt.X('DATE', sort=None, title='Date'),
                    y=alt.Y('count', title='Count'))
            st.write(_chart2)
    
    

        



    return