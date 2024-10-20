import streamlit as st
from services.api import create_user_api

def create_user():
    st.header("Create User")
    name = st.text_input("Name")
    email = st.text_input("Email")
    mobile = st.text_input("Mobile")

    if st.button("Create User"):
        user_data = {"name": name, "email": email, "mobile_number": mobile}
        response = create_user_api(user_data)
        if response.status_code == 201:
            st.success("User created successfully!")
        else:
            st.error(f"Error: {response.json()}")
