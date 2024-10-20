# import streamlit as st
# from services.api import download_balance_sheet_api

# def download_balance_sheet():
#     st.header("Balance Sheet")
#     if st.button("Download"):
#         response = download_balance_sheet_api()
        
#         # print(response)
#         # if response.status_code == 200:
#         #     sheet = response.json()
#         #     st.write(sheet)
#         #     st.write("---")
#         # else:
#         #     st.error("No expenses found!")

import streamlit as st
from services.api import download_balance_sheet_api

def download_balance_sheet():
    st.header("Balance Sheet")
    
    download_link = "http://localhost:8000/balance_sheet/"  # Use the appropriate base URL for your API
    
    st.markdown(
        f"[Download Balance Sheet]( {download_link} )",
        unsafe_allow_html=True
    )
