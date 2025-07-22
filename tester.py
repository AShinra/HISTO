import streamlit as st



ccc = st.text_area('Sample')

if st.button('Write') and ccc is not None:
    t = ccc.splitlines()


st.write(t)
