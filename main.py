import streamlit as st
from streamlit_option_menu import option_menu
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime
import time

def get_gsheet_client():
    # Load credentials from Streamlit secrets
    credentials_dict = {
        "type": st.secrets["gcp_service_account"]["type"],
        "project_id": st.secrets["gcp_service_account"]["project_id"],
        "private_key_id": st.secrets["gcp_service_account"]["private_key_id"],
        "private_key": st.secrets["gcp_service_account"]["private_key"],
        "client_email": st.secrets["gcp_service_account"]["client_email"],
        "client_id": st.secrets["gcp_service_account"]["client_id"],
        "auth_uri": st.secrets["gcp_service_account"]["auth_uri"],
        "token_uri": st.secrets["gcp_service_account"]["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["gcp_service_account"]["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["gcp_service_account"]["client_x509_cert_url"]
    }
    
    credentials = Credentials.from_service_account_info(credentials_dict, scopes=["https://www.googleapis.com/auth/spreadsheets"])
    client = gspread.authorize(credentials)
    return client


def get_client_names(df):


    return


def input():

    return

def archive():
    st.title("Archive Data")

    
    try:
        client = get_gsheet_client()
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
        
        col1, col2 = st.columns(2, border=True)
        
        with col1:
            _date = st.date_input('Date', key='i_date').isoformat()
            _date_all = st.checkbox('All', help='Selects all Dates for selected Client/s')
        
        with col2:
            _client = st.multiselect('Client', key='i_client', options=client_list)
    
        b_search = st.button('Search' , key='search_archive', use_container_width=True)
        
     
    if b_search:

        with st.spinner(text="Reading Archives", show_time=False, width="content"):
            time.sleep(5)
            if _client != []:
                for cl in _client:

                    formatted_date_1 = datetime.strptime(_date, '%Y-%m-%d')
                    # formatted_date_1 = formatted_date_1.strftime('%d-%b-%y')
                    st.write(formatted_date_1)

                    if _date_all:
                        filtered_df = df[(df['CLIENT NAME'] == cl)]
                    else:
                        st.write(type(df['DATE']))
                        filtered_df = df[(df['DATE'] == formatted_date_1) & (df['CLIENT NAME'] == cl)]
                    
                    if filtered_df.shape[0] > 0:
                        selected_columns = filtered_df[['DATE', 'TIER', 'LINK']]
                        st.header(cl)
                        st.dataframe(selected_columns, use_container_width=True, hide_index=True)
                    elif filtered_df.shape[0] == 0:
                        st.error('No Data Found')

            elif _client == []:
                st.error('Select a client from the list')

    return


def onhand():

    st.title("Inventory Tracker")

    try:
        client = get_gsheet_client()
        # sheet = client.open("Your Google Sheet Name").sheet1  # Update with your sheet name
        sheet_id = "1ZmilDNuV_h-w1OkKNwlbZCyD42KpaL5ilEK1hELRJpo"
        sheet = client.open_by_key(sheet_id)
        # values_list = sheet.sheet1.row_values(1)
        # st.write(values_list)

    except Exception as e:
        st.error(f"Error accessing Google Sheet: {e}")

    data = sheet.sheet1.get_all_values()
    df = pd.DataFrame(data)
    df.columns = ['Date', 'Item', 'Brand', 'Description', 'Quantity', 'Unit']
    df['Quantity'] = df['Quantity'].astype(int)
    new_df = df.groupby(["Item", "Brand", "Description"]).agg({"Quantity": "sum"})
    st.dataframe(new_df, use_container_width=True)


    return



if __name__ == "__main__":

    with st.sidebar:
        selected = option_menu(
            menu_title='Histo Data',
            menu_icon='',
            options=['Input', 'Archive']
        )

    if selected == 'Input':
        input()
    
    if selected == 'Archive':
        archive()
