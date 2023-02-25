import streamlit as st

st.title("Debts")

payees = ["SS","SG","JJ"]
debt_types = ["Request","Payback"]
with st.form("debts_form",clear_on_submit=True):
    col1,col2,col3,col4,col5 = st.columns(5)
    col1.selectbox("Select Payee", payees, key="payee")
    col2.number_input("Enter Amount", min_value = 0,key="amount")
    col3.text_input("Enter Description", key="description")
    col4.selectbox("Debt Type",debt_types, key="debt_type")
    submit_button = st.form_submit_button("Submit")

