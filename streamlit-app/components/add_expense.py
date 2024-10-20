import streamlit as st
from services.api import add_expense_api

def add_expense():
    st.header("Add Expense")
    description = st.text_input("Description")
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    paid_by = st.text_input("Paid by (mobile_number)")
    method = st.selectbox("Split Method", ["equal", "exact", "percentage"])

    splits = []
    if method == "exact" or method == "percentage" or method == "equal":
        num_participants = st.number_input("Number of Participants", min_value=1, step=1)
        for i in range(num_participants):
            participant_mobile_number = st.text_input(f"Participant {i+1} Mobile Number")
            if method == "exact":
                participant_amount = st.number_input(f"Participant {i+1} Amount", min_value=0.0, format="%.2f")
            elif method == "percentage":
                participant_amount = st.number_input(f"Participant {i+1} Percentage", min_value=0.0, max_value=100.0, format="%.2f")
            else:
                participant_amount = 0.0
            splits.append({"user_mobile_number": participant_mobile_number, "amount": participant_amount})

    if st.button("Add Expense"):
        expense_data = {"description": description, "amount": amount, "paid_by": paid_by, "method": method, "splits": splits}
        response = add_expense_api(expense_data)
        if response.status_code == 201:
            st.success("Expense added successfully!")
        else:
            st.error(f"Error: {response.json()}")
