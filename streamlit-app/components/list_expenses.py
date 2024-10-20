import streamlit as st
from services.api import list_expenses_api

def list_expenses():
    st.header("List All Expenses")
    response = list_expenses_api()
    print(response)
    if response.status_code == 200:
        expenses = response.json()
        for expense in expenses:
            st.write(f"Description: {expense['description']}")
            st.write(f"Amount: {expense['amount']}")
            st.write(f"Paid by: {expense['paid_by']}")
            st.write("Splits:")
            for split in expense['expenses'].keys():
                st.write(f"  - {split} owes {expense['expenses'][split]}")
            st.write("---")
    else:
        st.error("No expenses found!")
