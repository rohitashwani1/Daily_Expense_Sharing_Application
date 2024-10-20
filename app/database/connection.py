import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://rohitashwani:1234@cluster0.whmiaqd.mongodb.net/")
db = client.expense_db
