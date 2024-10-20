from pydantic import BaseModel, EmailStr

class User(BaseModel):
    email: EmailStr
    name: str
    mobile_number: str
