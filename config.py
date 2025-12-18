import os
from dotenv import load_dotenv
 
load_dotenv()

# APP CONFIGURATION
APP_NAME = "Finance Tracker"

#MONGO  CONFIGURATION
MONGO_URI = os.getenv("MONGO_URI","mongodb://localhost:27017/")
DATABASE_NAME = "finance_tracker"


#collection names
COLLECTIONS = {
    "user": "users",
    "transaction": "transactions",
    "category": "categories",
    "budget": "budgets",
}

#transaction types
TRANSACTION_TYPES = ['Expense', 'Income']

# DEFAULT_CATEGORIES_EXPENSE:
DEFAULT_CATEGORIES_EXPENSE = [
    "Food & Dining",
    "Transportation",
    "Utilities",
    "Entertainment",
    "Healthcare",
    "Shopping",
    "Education",
    "Travel",
    "Personal Care",
    "Gifts & Donations",
]

# DEFAULT_CATEGORIES_INCOME:
DEFAULT_CATEGORIES_INCOME = [
    "Salary",
    "Business",
    "Investments",
    "Gifts",
    "Freelance",
    "Rental Income",
    "Interest",
    "Dividends",
    "Bonuses",
    "Other Income",
]


