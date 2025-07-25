import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from datetime import datetime
import time
import altair as alt


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


def summary(client):

    st.title(':violet[Summary]')

    df = get_data(client)

    df['DATE'] = pd.to_datetime(df['DATE'])
    df['MONTH_NAME'] = df['DATE'].dt.month_name()
    df['YEAR'] = df['DATE'].dt.year
    monthly_data = df['MONTH_NAME'].value_counts(sort=False)

    year_list = df['YEAR'].unique()

    client_list = df['CLIENT NAME'].unique()
    client_list = sorted(client_list)
    client_list.insert(0, 'ALL')
    
    selection_col, chart_col = st.columns([0.3, 0.7], border=True)
    with selection_col:
        
        # client selection
        client_selection = st.selectbox(
            label='Client',
            options=client_list
        )

        if client_selection != 'ALL':
            df_clientfiltered = df[df['CLIENT NAME'] == client_selection]
        else:
            df_clientfiltered = df
        
        total_request = df_clientfiltered.shape[0]

        months = df_clientfiltered['MONTH_NAME'].unique()
        number_of_months = months.shape[0]

        _days = df_clientfiltered['DATE'].unique()
        number_of_days = _days.shape[0]

        _misses = df_clientfiltered[df['CAPTURED']=='N']
        total_misses = _misses.shape[0]

        _misses_tier = df_clientfiltered[(df['CAPTURED']=='N') & (df['TIER'] != '')]        

        _misses_tier1 = _misses_tier[_misses_tier['TIER']=="1"]
        _misses_tier1_pub = _misses_tier1['FQDN'].to_list()
        count_misses_tier1 = _misses_tier1.shape[0]

        _misses_tier2 = _misses_tier[_misses_tier['TIER']=="2"]
        _misses_tier2_pub = _misses_tier2['FQDN'].to_list()
        count_misses_tier2 = _misses_tier2.shape[0]

        _misses_tier3 = _misses_tier[_misses_tier['TIER']=="3"]
        _misses_tier3_pub = _misses_tier3['FQDN'].to_list()
        count_misses_tier3 = _misses_tier3.shape[0]

        _misses_tieru = _misses_tier[_misses_tier['TIER']=="Unlisted"]
        _misses_tieru_pub = _misses_tieru['FQDN'].to_list()
        count_misses_tieru = _misses_tieru.shape[0]

        request_per_month = total_request/number_of_months
        request_per_day = total_request/number_of_days
        misses_per_month = total_misses/number_of_months
        misses_per_day = total_misses/number_of_days
        misses_percent = total_misses/total_request


        cola1, cola2 = st.columns(2)

        with cola1:
            cap_option = st.radio(
                label='Options',
                options=['Missed', 'Captured', 'Request'],
                horizontal=False                
            )
        
        with cola2:
            year_selected = st.selectbox(
                label='YEAR',
                options=year_list)
        
        st.divider()
        # compute statistics
        with st.spinner('Processing Data', show_time=True):
            st.header(f'Statistics ({client_selection})')
            st.write(f'Total Requests: {int(total_request):,}')
            st.write(f'Average Requests per Month: {int(request_per_month):,}')
            st.write(f'Average Requests per Day: {int(request_per_day):,}')
            st.write('')
            st.write(f'Total Misses: {int(total_misses):,} ({misses_percent:.2%})')
            st.write(f'Average Misses per Month: {int(misses_per_month):,}')
            st.write(f'Average Misses per Day: {int(misses_per_day):,}')
            st.write('')

            coltiera1, coltiera2 = st.columns([0.3, 0.7])
            with coltiera1:
                with st.popover(
                    label='Details'
                ):  
                    _misses_tier1_pub = list(dict.fromkeys(_misses_tier1_pub))
                    for _pub in sorted(_misses_tier1_pub):
                        st.write(_pub)
            with coltiera2:
                st.write(f'Tier 1 Missed: {count_misses_tier1}')
            

            coltierb1, coltierb2 = st.columns([0.3, 0.7])
            with coltierb1:                            
                with st.popover(
                    label='Details'
                ):  
                    _misses_tier2_pub = list(dict.fromkeys(_misses_tier2_pub))
                    for _pub in sorted(_misses_tier2_pub):
                        st.write(_pub)
            with coltierb2:
                st.write(f'Tier 2 Missed: {count_misses_tier2}')
            
            coltierc1, coltierc2 = st.columns([0.3, 0.7])
            with coltierc1:
                with st.popover(
                    label='Details'
                ):
                    _misses_tier3_pub = list(dict.fromkeys(_misses_tier3_pub))
                    for _pub in sorted(_misses_tier3_pub):
                        st.write(_pub)
            with coltierc2:
                st.write(f'Tier 3 Missed: {count_misses_tier3}')
            
            coltierd1, coltierd2 = st.columns([0.3, 0.7])
            with coltierd1:
                with st.popover(
                    label='Details'
                ):
                    _misses_tieru_pub = list(dict.fromkeys(_misses_tieru_pub))
                    for _pub in sorted(_misses_tieru_pub):
                        st.write(_pub)
            with coltierd2:
                st.write(f'Tier Unlisted Missed: {count_misses_tieru}')

        


        if cap_option=='Captured':
            df_captured = df_clientfiltered[df_clientfiltered['CAPTURED'] == 'Y']
        elif cap_option=='Missed':
            df_captured = df_clientfiltered[df_clientfiltered['CAPTURED'] == 'N']
        elif cap_option=='Request':
            df_captured = df_clientfiltered


    with chart_col:
        chart_cola1, chart_cola2 = st.columns([0.3, 0.7], border=True)
        with chart_cola1:
            with st.spinner('Generating Table', show_time=True):
                monthcount = df_captured['MONTH_NAME'].value_counts(sort=False)
                df_monthcount = monthcount.to_frame()
                df_monthcount = df_monthcount.reset_index()
                st.dataframe(df_monthcount, hide_index=True)
        with chart_cola2:
            with st.spinner('Generating Chart', show_time=True):
                _chart1 = alt.Chart(df_monthcount, title=alt.TitleParams(f'Monthly {cap_option}', anchor='middle')).mark_bar().encode(
                    x=alt.X('MONTH_NAME', sort=None, title='Month'),
                    y=alt.Y('count', title='Count'))
                st.write(_chart1)       
                
        chart_colb1, chart_colb2 = st.columns([0.3, 0.7], border=True)
        with chart_colb1:
            with st.spinner('Generating Table', show_time=True):
                countdate = df_captured['DATE'].value_counts(sort=False)
                df_countdate = countdate.to_frame()
                df_countdate = df_countdate.reset_index()            
                st.dataframe(df_countdate, hide_index=True)
        with chart_colb2:
            with st.spinner('Generating Chart', show_time=True):
                _chart2 = alt.Chart(df_countdate, title=alt.TitleParams(f'Daily {cap_option}', anchor='middle')).mark_bar().encode(
                        x=alt.X('yearmonthdate(DATE):O', sort=None, title='Date', axis=alt.Axis(format='%b %d')),
                        y=alt.Y('count', title='Count'))
                st.write(_chart2)
        
        chart_colc1, chart_colc2 = st.columns([0.3, 0.7], border=True)
        with chart_colc1:
            with st.spinner('Generating Table', show_time=True):
                countfqdn = df_captured['FQDN'].value_counts(sort=True)
                df_fqdn = countfqdn.to_frame()
                df_fqdn = df_fqdn.reset_index()
                top10_fqdn = df_fqdn[:10]
                st.dataframe(top10_fqdn, hide_index=True)
        with chart_colc2:
            with st.spinner('Generating Chart', show_time=True):
                _chart3 = alt.Chart(top10_fqdn, title=alt.TitleParams(f'Top 10 {cap_option}', anchor='middle')).mark_bar().encode(
                        x=alt.X('FQDN', sort=None, title='FQDN'),
                        y=alt.Y('count', title='Count'))
                st.write(_chart3)
    

        



    return