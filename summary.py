import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from datetime import datetime
import time
import altair as alt

def summary(client):

    st.title('Summary')

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

        # data for statistics
        # total_request = df.shape[0]

        # months = df['MONTH_NAME'].unique()
        # number_of_months = months.shape[0]

        # _days = df['DATE'].unique()
        # number_of_days = _days.shape[0]

        # _misses = df[df['CAPTURED']=='N']
        # total_misses = _misses.shape[0]


        # request_per_month = total_request/number_of_months
        # request_per_day = total_request/number_of_days
        # misses_per_month = total_misses/number_of_months
        # misses_per_day = total_misses/number_of_days
        # misses_percent = total_misses/total_request

        monthly_data = df['MONTH_NAME'].value_counts(sort=False)
        

        # --------------------

        year_list = df['YEAR'].unique()

        client_list = df['CLIENT NAME'].unique()
        client_list = sorted(client_list)
        client_list.insert(0, 'ALL')

        # st.dataframe(df_captured)

    except Exception as e:
        st.error(f"Error accessing Google Sheet: {e}")
    
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

        request_per_month = total_request/number_of_months
        request_per_day = total_request/number_of_days
        misses_per_month = total_misses/number_of_months
        misses_per_day = total_misses/number_of_days
        misses_percent = total_misses/total_request


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
        
        st.divider()
        # compute statistics
        st.header(f'{client_selection} Statistics')
        st.markdown("""
                    <style>
                    [data-testid=column]:nth-of-type(1) [data-testid=stVerticalBlock]{gap: 0rem;}
                    </style>""",
                    unsafe_allow_html=True
                    )
        st.write(f'Total Requests: {int(total_request):,}')
        st.write(f'Average Requests per Month: {int(request_per_month):,}')
        st.write(f'Average Requests per Day: {int(request_per_day):,}')
        st.write('')
        st.write(f'Total Misses: {int(total_misses):,} ({misses_percent:.2%})')
        st.write(f'Average Misses per Month: {int(misses_per_month):,}')
        st.write(f'Average Misses per Day: {int(misses_per_day):,}')

        


        if cap_option=='Captured':
            df_captured = df_clientfiltered[df_clientfiltered['CAPTURED'] == 'Y']
        elif cap_option=='Missed':
            df_captured = df_clientfiltered[df_clientfiltered['CAPTURED'] == 'N']
        elif cap_option=='Request':
            df_captured = df_clientfiltered


    with chart_col:
        chart_cola1, chart_cola2 = st.columns([0.3, 0.7])
        with chart_cola1:
            monthcount = df_captured['MONTH_NAME'].value_counts(sort=False)
            df_monthcount = monthcount.to_frame()
            df_monthcount = df_monthcount.reset_index()
            st.dataframe(df_monthcount, hide_index=True)
        with chart_cola2:
            _chart1 = alt.Chart(df_monthcount, title=alt.TitleParams(f'Monthly {cap_option}', anchor='middle')).mark_bar().encode(
                x=alt.X('MONTH_NAME', sort=None, title='Month'),
                y=alt.Y('count', title='Count'))
            st.write(_chart1)
        
        st.divider()
        
        chart_colb1, chart_colb2 = st.columns([0.3, 0.7])
        with chart_colb1:
            countdate = df_captured['DATE'].value_counts(sort=False)
            df_countdate = countdate.to_frame()
            df_countdate = df_countdate.reset_index()
            st.dataframe(df_countdate, hide_index=True)
        with chart_colb2:
            _chart2 = alt.Chart(df_countdate.dropna(), title=alt.TitleParams(f'Daily {cap_option}', anchor='middle')).mark_bar().encode(
                    x=alt.X('DATE', sort=None, title='Date'),
                    y=alt.Y('count', title='Count'))
            st.write(_chart2)
        
        st.divider()

        chart_colc1, chart_colc2 = st.columns([0.3, 0.7])
        with chart_colc1:
            countfqdn = df_captured['FQDN'].value_counts(sort=True)
            df_fqdn = countfqdn.to_frame()
            df_fqdn = df_fqdn.reset_index()
            # st.dataframe(df_fqdn, hide_index=True)
            top10_fqdn = df_fqdn[:10]
            st.dataframe(top10_fqdn, hide_index=True)
        with chart_colc2:
            _chart3 = alt.Chart(top10_fqdn, title=alt.TitleParams(f'Top 10 {cap_option}', anchor='middle')).mark_bar().encode(
                    x=alt.X('FQDN', sort=None, title='FQDN'),
                    y=alt.Y('count', title='Count'))
            st.write(_chart3)
    

        



    return