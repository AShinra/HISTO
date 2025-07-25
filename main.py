import streamlit as st
from streamlit_option_menu import option_menu
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime
import time
from PIL import Image

from archive import archive
from input import input
from summary import summary


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


if __name__ == "__main__":

    st.set_page_config(
        layout="wide",
        page_title='HISTO')
    
    try:
        image = Image.open("https://i.ibb.co/JRW19H4Y/AShinra-Logo.png")
        st.sidebar.image(image)
    except FileNotFoundError:
        st.sidebar.write("Image file not found. Please check the path.")

    with st.sidebar:
        selected = option_menu(
            menu_title='Histo Data',
            menu_icon='clock-history',
            options=['Entry', 'Archive', 'Summary'],
            icons=['pencil-square', 'archive', 'journals']
        )

    client = get_gsheet_client()
    client_list = []
    if selected == 'Entry':
        input(client, client_list)
    
    if selected == 'Archive':
        archive(client)
    
    if selected == 'Summary':
        summary(client)
