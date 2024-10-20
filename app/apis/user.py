from fastapi import APIRouter, HTTPException
from app.models.user import User
from pydantic import EmailStr
from app.database.connection import db
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/users/")
async def create_user(user: User):
    """
    Asynchronously creates a new user in the database.
    Args:
        user (User): The user object containing user details.
    Raises:
        HTTPException: If the mobile number is not a 10-digit number.
        HTTPException: If a user with the given mobile number already exists.
    Returns:
        JSONResponse: A JSON response with a success message and a 201 status code.
    """

    # Check if the mobile number is a 10-digit number
    if len(user.mobile_number) != 10 or not user.mobile_number.isdigit():
        raise HTTPException(status_code=400, detail="Mobile number must be a 10-digit number")
    
    existing_user = await db.users.find_one({"mobile_number": user.mobile_number})

    if existing_user:
        raise HTTPException(status_code=400, detail="User with this mobile number already exists")
    
    user_data = user.dict()
    await db.users.insert_one(user_data)
    return JSONResponse(content={"message": "User created successfully"},status_code=201)




@router.get("/users/{mobile_number}")
async def get_user(mobile_number: str):
    """
    Endpoint to retrieve user details by mobile number.

    Args:
        mobile_number (str): The mobile number of the user to retrieve.

    Returns:
        dict: A dictionary containing user details excluding the '_id' field.

    Raises:
        HTTPException: If the user is not found, raises a 404 HTTPException with the message "User not found".
    """
    user = await db.users.find_one({"mobile_number":mobile_number})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.pop('_id')
    return user
