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
    
    print("📋 Checking and creating categories...")
    
    # ✅ STEP 1: Ensure categories exist before adding transactions
    existing_categories = category_model.get_total()
    existing_names = {cat['name']: cat['type'] for cat in existing_categories}
    
    # Create missing expense categories
    for cat_name in expense_categories:
        if cat_name not in existing_names:
            category_model.upsert_category(category_type="Expense", category_name=cat_name)
            print(f"  ✓ Created Expense category: {cat_name}")
        elif existing_names[cat_name] != "Expense":
            print(f"  ⚠️  Category '{cat_name}' exists but as {existing_names[cat_name]}")
    
    # Create missing income categories
    for cat_name in income_categories:
        if cat_name not in existing_names:
            category_model.upsert_category(category_type="Income", category_name=cat_name)
            print(f"  ✓ Created Income category: {cat_name}")
        elif existing_names[cat_name] != "Income":
            print(f"  ⚠️  Category '{cat_name}' exists but as {existing_names[cat_name]}")
    
    print("\n💰 Adding sample transactions...")
    
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
        
        # Add transaction with error handling
        try:
            result = transaction_model.add_transaction(
                transaction_type=transaction_type,
                category=category,
                amount=amount,
                transaction_date=transaction_date,
                description=description
            )
            
            if result:
                print(f"  ✓ Added {transaction_type}: ${amount} - {category}")
        except ValueError as e:
            print(f"  ❌ Error: {e}")
        except Exception as e:
            print(f"  ❌ Unexpected error: {e}")
    
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
