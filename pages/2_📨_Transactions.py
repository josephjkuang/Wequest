import streamlit as st
import plotly.graph_objects as go
import calendar
from datetime import datetime
from venmo_api import Client

from streamlit_modal import Modal
import streamlit.components.v1 as components
import pandas as pd

st.title("Transactions")

years = [datetime.today().year,datetime.today().year-1,datetime.today().year-2,datetime.today().year-3]
months = [calendar.month_name[i] for i in range(1,13)]

with st.form("transaction_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    selected_year = col1.selectbox("Select Year", years, key="year")
    selected_month = col2.selectbox("Select Month", months, key="month")
    submit_button = st.form_submit_button("Submit")
    
# store the selected year and month in session state
st.session_state.selected_year = selected_year
st.session_state.selected_month = selected_month

#store data from transaction
data = []

# Open the file and read the data line by line
with open("transactions.txt", "r") as f:
    for line in f:
        # Extract the necessary data from each line and store it in a dictionary
        transaction = {}
        transaction["name"] = line.split("display_name=")[1].split(",")[0]
        transaction["amount"] = line.split("payment_id=")[1].split(",")[0]
        transaction["description"] = line.split("note=")[1].split(",")[0]
        transaction["date"] = pd.to_datetime(line.split("date_completed=")[1].split(",")[0], unit="s")
        # Add the dictionary to the list
        data.append(transaction)

# Create a pandas DataFrame from the list of dictionaries
df = pd.DataFrame(data)
df = df.set_index("name")

# filter the data by the selected month and year
df = df.loc[(df['date'].dt.year == st.session_state.selected_year) & (df['date'].dt.month == list(calendar.month_name).index(st.session_state.selected_month))]

st.dataframe(df)
