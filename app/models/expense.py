from pydantic import BaseModel
from typing import List

class ExpenseSplit(BaseModel):
    user_mobile_number: str
    amount: float

class Expense(BaseModel):
    description: str
    amount: float
    paid_by: str
    splits: List[ExpenseSplit]
    method: str  # "equal", "exact", or "percentage"
