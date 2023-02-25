from datetime import datetime
import plotly.graph_objects as go
import streamlit as st

currency = "USD"
page_title = "WeQuest"

page_icon = ":money_with_wings:"
# layout = "centered"
st.set_page_config(page_title=page_title, page_icon=page_icon, layout="wide")

st.title(page_title+ " " + page_icon)
st.sidebar.success(("Select a page above."))
