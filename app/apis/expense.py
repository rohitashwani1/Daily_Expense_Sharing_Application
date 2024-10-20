from fastapi import APIRouter, HTTPException
from app.models.expense import Expense
from app.database.connection import db
from app.utils import calculate_equal_split, calculate_percentage_split
import pandas as pd
from fastapi.responses import StreamingResponse, JSONResponse
import io

router = APIRouter()








@router.post("/expenses/")
async def add_expense(expense: Expense):
    """
    Adds a new expense to the database.

    This function validates the provided expense details, calculates the split amounts based on the specified method,
    and inserts the expense into the database.

    Args:
        expense (Expense): The expense object containing details of the expense to be added.

    Raises:
        HTTPException: If the user mentioned in 'paid_by' field does not exist.
        HTTPException: If any user mentioned in the splits does not exist.
        HTTPException: If the percentages in the 'percentage' method do not sum to 100%.
        HTTPException: If the exact split amounts do not match the total amount.
        HTTPException: If an invalid split method is provided.

    Returns:
        JSONResponse: A JSON response indicating the success of the operation with a status code of 201.
    """
    if (await db.users.find_one({"mobile_number":expense.paid_by}) == None):
        raise HTTPException(status_code=400 , detail="User mentioned in 'paid_by' field does not exist")
    users = [split.user_mobile_number for split in expense.splits]
    for user in users:
        if (await db.users.find_one({"mobile_number":user}) == None):
            raise HTTPException(status_code=400 , detail="One of the user mentioned does not exist")
    if expense.method == "equal":
        split_amounts = calculate_equal_split(float(expense.amount), users)
    elif expense.method == "percentage":
        percentages = {split.user_mobile_number: float(split.amount) for split in expense.splits}
        split_amounts = calculate_percentage_split(float(expense.amount), percentages)
        if split_amounts == -1:
            raise HTTPException(status_code=400 , detail="Percentages must sum to 100%")
    elif expense.method == "exact":
        split_amounts = {split.user_mobile_number: float(split.amount) for split in expense.splits}
        if sum(split_amounts.values()) != float(expense.amount):
            raise HTTPException(status_code=400, detail="Exact split does not match total amount")
    else:
        raise HTTPException(status_code=400, detail="Invalid split method")

    expense_data = expense.dict()
    expense_data["split_amounts"] = split_amounts
    print(expense_data)
    await db.expenses.insert_one(expense_data)
    return JSONResponse(content={"message": "Expense added successfully"},status_code=201)







@router.get('/expenses/')
async def get_all_expenses():

    """
    This module provides API endpoints for managing expenses in the Daily Expense Sharing Application.
        Retrieve all expenses from the database.

        This asynchronous function fetches all expense records from the database,
        formats them, and returns them as a JSON response. If no expenses are found,
        it raises an HTTP 404 exception.

        Returns:
            JSONResponse: A JSON response containing a list of formatted expense records
                          with a status code of 200.

        Raises:
            HTTPException: If no expenses are found, an HTTP 404 exception is raised.
        """
    
    expenses = await db.expenses.find({}).to_list(length=None)
    if not expenses:
        raise HTTPException(status_code=404, detail="No expenses found")
    formatted_expenses = []
    print(expenses)
    for expense in expenses:
        print(expense)
        tmp = {}
        tmp['description'] = expense['description']
        tmp['paid_by'] = expense['paid_by']
        tmp['amount'] = expense['amount']
        tmp['expenses'] = expense['split_amounts']
        formatted_expenses.append(tmp)

    return JSONResponse(content=formatted_expenses,status_code=200)





@router.get("/expenses/user/{mobile_number}")
async def get_user_expenses(mobile_number: str):
    """
    Fetches and returns the expenses for a user based on their mobile number.

    Args:
        mobile_number (str): The mobile number of the user whose expenses are to be fetched.

    Raises:
        HTTPException: If the user does not exist (status code 400).
        HTTPException: If no expenses are found for the user (status code 404).

    Returns:
        JSONResponse: A JSON response containing a list of expenses formatted with description, paid_by, and expense_amount.
    """
    if (await db.users.find_one({"mobile_number":mobile_number}) == None):
        raise HTTPException(status_code=400 , detail="One of the user mentioned does not exist")
    expenses = await db.expenses.find({"splits.user_mobile_number": mobile_number}).to_list(length=None)
    if not expenses:
        raise HTTPException(status_code=404, detail="No expenses found for this user")
    formatted_expenses = []
    for expense in expenses:
        # i.pop('_id')
        tmp = {}
        tmp['description'] = expense['description']
        tmp['paid_by'] = expense['paid_by']
        tmp['expense_amount'] = expense['split_amounts'][mobile_number]
        formatted_expenses.append(tmp)

    return JSONResponse(content=formatted_expenses,status_code=200)




@router.get("/balance_sheet/")
async def download_balance_sheet():
    """
    Asynchronously retrieves all expenses from the database, processes them into a CSV format,
    and returns the CSV file as a streaming response.

    Raises:
        HTTPException: If no expenses are found in the database.

    Returns:
        StreamingResponse: A streaming response containing the CSV file with the balance sheet.
    """
    expenses = await db.expenses.find().to_list(length=None)
    if not expenses:
        raise HTTPException(status_code=404, detail="No expenses found")

    data = []
    for expense in expenses:
        for user, amount in expense["split_amounts"].items():
            data.append([user, expense["description"], amount])

    df = pd.DataFrame(data, columns=["User", "Expense Description", "Amount"])

    stream = io.StringIO()
    df.to_csv(stream, index=False)
    stream.seek(0)  # Move to the beginning of the stream for reading
    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=balance_sheet.csv"
    return response

