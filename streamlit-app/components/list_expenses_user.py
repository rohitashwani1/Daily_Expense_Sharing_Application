import streamlit as st
from services.api import list_expenses_user_api

def list_expenses_user():
    st.header("List User Expenses")
    mobile = st.text_input("Mobile")
    if st.button("Fetch Expenses"):
        response = list_expenses_user_api(mobile)
        if response.status_code == 200:
            expenses = response.json()
            for expense in expenses:
                st.write(f"Description: {expense['description']}")
                st.write(f"Amount: {expense['expense_amount']}")
                st.write(f"Paid by: {expense['paid_by']}")
                st.write("---")
        else:
            st.error(f"Error: {response.json()}")