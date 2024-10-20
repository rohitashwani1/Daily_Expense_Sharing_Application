import streamlit as st
from components.create_user import create_user
from components.add_expense import add_expense
from components.list_expenses import list_expenses
from components.list_expenses_user import list_expenses_user
from components.download_balance_sheet import download_balance_sheet

def main():
    st.title("Daily Expenses Sharing App")

    menu = ["Create User", "Add Expense", "List All Expenses", "List Expenses User","Download Balance Sheet"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Create User":
        create_user()
    elif choice == "Add Expense":
        add_expense()
    elif choice == "List All Expenses":
        list_expenses()
    elif choice == "List Expenses User":
        list_expenses_user()
    else:
        download_balance_sheet()

if __name__ == "__main__":
    main()
