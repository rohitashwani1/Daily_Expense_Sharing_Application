import requests

API_BASE_URL = "http://localhost:8000/"

def create_user_api(user_data):
    return requests.post(f"{API_BASE_URL}/users/", json=user_data)

def add_expense_api(expense_data):
    return requests.post(f"{API_BASE_URL}/expenses/", json=expense_data)

def list_expenses_api():
    return requests.get(f"{API_BASE_URL}/expenses/")

def list_expenses_user_api(mobile_number):
    return requests.get(f"{API_BASE_URL}/expenses/user/{mobile_number}")  

def download_balance_sheet_api():
    return requests.get(f"{API_BASE_URL}/balance_sheet")
