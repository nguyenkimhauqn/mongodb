import os
from dotenv import load_dotenv

# Load .env file for local development
load_dotenv()

# APP CONFIGURATION
APP_NAME = "Finance Tracker"

# MONGO CONFIGURATION
# Support both Streamlit Cloud secrets and .env file
def get_mongo_uri():
    """Get MONGO_URI from Streamlit secrets (Cloud) or environment variables (local)"""
    # Try to get from Streamlit secrets (for Streamlit Cloud)
    try:
        import streamlit as st
        if hasattr(st, 'secrets') and st.secrets is not None:
            if 'MONGO_URI' in st.secrets:
                return st.secrets['MONGO_URI']
    except (ImportError, AttributeError, RuntimeError, KeyError):
        # Not running in Streamlit or secrets not available
        pass
    
    # Fall back to environment variable (for local development)
    return os.getenv("MONGO_URI", "mongodb://localhost:27017/")

MONGO_URI = get_mongo_uri()
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


