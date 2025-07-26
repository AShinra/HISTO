import streamlit as st
from streamlit_option_menu import option_menu
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime
import time
from PIL import Image
import requests
from io import BytesIO

from archive import archive
from input import input
from summary import summary

@st.cache_resource
def get_logo():

    url = "https://i.ibb.co/JRW19H4Y/AShinra-Logo.png"
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    image = Image.open(BytesIO(response.content))

    return image

@st.cache_resource
def get_bgimage():

    background_image = """
    <style>
    [data-testid="stAppViewContainer"] > .main {
    background-image: url("https://i.ibb.co/8D4hLbSX/natural-light-white-background.jpg");
    background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
    background-position: center;
    background-repeat: no-repeat;}</style>"""

    st.markdown(background_image, unsafe_allow_html=True)

    return


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

    get_bgimage()

    hide_streamlit_style = """<style>
    ._link_gzau3_10 {
        display: none !important;
    }    
    </style>"""
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)    


    st.set_page_config(
        layout="wide",
        page_title='HISTO')
    
    # hide streamlit toolbar
    st.markdown("""<style>[data-testid="stToolbar"] {display: none;}</style>""", unsafe_allow_html=True)
    st.markdown("""<style>[data-testid="manage-app-button"] {display: none !important;}</style>""", unsafe_allow_html=True)
    st.markdown("""<style>.stApp {background-image: url("https://i.ibb.co/8D4hLbSX/natural-light-white-background.jpg");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;}</style>""", unsafe_allow_html=True)
    
    try:
        st.sidebar.image(get_logo())
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
