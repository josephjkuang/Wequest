import streamlit as st
import plotly.graph_objects as go
import calendar
from datetime import datetime
from venmo_api import Client

from streamlit_modal import Modal
import streamlit.components.v1 as components


modal = Modal("Demo Modal",key="T")
open_modal = st.button("Open")
if open_modal:
    modal.open()

if modal.is_open():
    with modal.container():
        st.write("Text goes here")

        html_string = '''
        <h1>HTML string in RED</h1>

        <script language="javascript">
          document.querySelector("h1").style.color = "red";
        </script>
        '''
        components.html(html_string)

        st.write("Some fancy text")
        value = st.checkbox("Check me")
        st.write(f"Checkbox checked: {value}")

st.title("Transactions")



years = [datetime.today().year,datetime.today().year-1,datetime.today().year-2,datetime.today().year-3]
months = [calendar.month_name[i] for i in range(1,13)]

with st.form("transaction_form",clear_on_submit=True):
    col1,col2 = st.columns(2)
    col1.selectbox("Select Year", years, key="year")
    col2.selectbox("Select Month", months, key="month")
    submit_button = st.form_submit_button("Submit")