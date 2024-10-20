from fastapi import FastAPI
from app.apis import user, expense

app = FastAPI()

# Include user and expense routes
app.include_router(user.router)
app.include_router(expense.router)
