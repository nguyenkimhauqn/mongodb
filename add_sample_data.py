from dataset.transaction_model import TransactionModel
from dataset.category_model import CategoryModel
from datetime import datetime, timedelta
import random

def add_sample_data(user_id):
    """Add sample transaction data for testing"""
    
    transaction_model = TransactionModel(user_id=user_id)
    category_model = CategoryModel(user_id=user_id)
    
    # Categories for expenses and income
    expense_categories = [
        "Food & Dining", "Transportation", "Utilities", "Entertainment",
        "Shopping", "Healthcare", "Education"
    ]
    
    income_categories = [
        "Salary", "Freelance", "Investments", "Bonuses"
    ]
    
    print("Adding sample transactions...")
    
    # Add 50 sample transactions over the last 3 months
    today = datetime.now()
    
    for i in range(50):
        # Random date in the last 90 days
        days_ago = random.randint(0, 90)
        transaction_date = today - timedelta(days=days_ago)
        
        # Random transaction type
        transaction_type = random.choice(["Expense", "Income"])
        
        if transaction_type == "Expense":
            category = random.choice(expense_categories)
            amount = round(random.uniform(10, 500), 2)
            descriptions = [
                "Lunch with friends",
                "Grocery shopping",
                "Monthly bill payment",
                "Movie tickets",
                "Coffee shop",
                "Gas station",
                "Restaurant dinner",
                "Online shopping",
                "Pharmacy",
                "Book purchase"
            ]
        else:
            category = random.choice(income_categories)
            amount = round(random.uniform(500, 5000), 2)
            descriptions = [
                "Monthly salary",
                "Freelance project payment",
                "Dividend payment",
                "Performance bonus",
                "Side gig income",
                "Investment returns"
            ]
        
        description = random.choice(descriptions)
        
        # Add transaction
        result = transaction_model.add_transaction(
            transaction_type=transaction_type,
            category=category,
            amount=amount,
            transaction_date=transaction_date,
            description=description
        )
        
        if result:
            print(f"✓ Added {transaction_type}: ${amount} - {category}")
    
    print(f"\n✅ Successfully added 50 sample transactions!")
    
    # Show statistics
    stats = transaction_model.get_statistics()
    print(f"\n📊 Statistics:")
    print(f"   Total Income: ${stats['total_income']:,.2f}")
    print(f"   Total Expense: ${stats['total_expense']:,.2f}")
    print(f"   Balance: ${stats['balance']:,.2f}")
    print(f"   Total Transactions: {stats['total_transactions']}")


if __name__ == "__main__":
    # You need to provide a valid user_id
    # Get this from your MongoDB after logging in
    user_id = input("Enter your user_id (from MongoDB): ")
    
    if user_id:
        add_sample_data(user_id)
    else:
        print("❌ Please provide a valid user_id")
