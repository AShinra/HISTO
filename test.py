import streamlit as st
from streamlit_option_menu import option_menu
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

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

def delivery():
    st.title("Delivery Tracker")

    with st.container(border=True):
        col1, col2, col3 = st.columns(3, border=True)
        with col1:
            _date = st.date_input('Delivery Date', key='i_date').isoformat()
            _edate = st.date_input('Expiration Date', key='i_edate').isoformat()
        with col2:
            _item = st.text_input('Item', key='i_item')
            _brand = st.text_input('Brand', key='i_brand')
            _desc = st.text_input('Description', key='i_desc')
        with col3:
            _qty = st.number_input('Quantity', step=1, key='i_qty')
            _unit = st.selectbox('Unit', options=['pouch', 'sack', 'box', 'pcs', 'can'], key='i_unit')
        st.button('Add' , key='add_item', use_container_width=True)
    
    try:
        client = get_gsheet_client()
        # sheet = client.open("Your Google Sheet Name").sheet1  # Update with your sheet name
        sheet_id = "1ZmilDNuV_h-w1OkKNwlbZCyD42KpaL5ilEK1hELRJpo"
        sheet = client.open_by_key(sheet_id)
        # values_list = sheet.sheet1.row_values(1)
        # st.write(values_list)

    except Exception as e:
        st.error(f"Error accessing Google Sheet: {e}")

    if st.session_state['add_item']:
        # sheet.sheet1.append_row([_date, _item, _brand, _desc, _qty, _unit])
        sheet.sheet1.insert_row([_date, _item, _brand, _desc, _qty, _unit, _edate])
        

    data = sheet.sheet1.get_all_values()

    df = pd.DataFrame(data)
    # df.columns = df.iloc[0]
    # df = df[1:]
    df.columns = ['Date', 'Item', 'Brand', 'Description', 'Quantity', 'Unit', 'Expiration']
    st.dataframe(df, use_container_width=True, hide_index=True)

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
        selected = option_menu("Inventory Menu", ["Delivery", 'Set Out', 'Inventory'],
                               menu_icon='box2-heart',
                               icons=['truck', 'basket', 'bank'],
                               default_index=1)
    
    if selected=='Delivery':
        delivery()
    if selected=='Inventory':
        onhand()
