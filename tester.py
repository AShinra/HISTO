import streamlit as st
from datetime import date

st.title("Date Range Picker with st.date_input")

today = date.today()
start_date = today
end_date = today

# Set initial values for the date range
date_range = st.date_input(
    "Select a date range",
    value=(start_date, end_date),
    min_value=date(2000, 1, 1),
    max_value=date(2030, 12, 31)
)

if date_range is not None and len(date_range) == 2:
    st.write(date_range)
    selected_start_date, selected_end_date = date_range
    st.write(start_date)
    st.write(f"Selected date range: From {selected_start_date} to {selected_end_date}")
else:
    st.write("Please select a valid date range.")