from dataset.transaction_model import TransactionModel
from datetime import date

if __name__ == "__main__":
    
    transaction_model = TransactionModel()

    transaction_type = "Income"
    category_name = "Salary"
    amount = 5000.0
    transaction_date = date.today()
    
    # # Add transaction
    # result = transaction_model.add_transaction(
    #     transaction_type=transaction_type,
    #     category_name=category_name,
    #     amount=amount,
    #     transaction_date=transaction_date,
    #     description="Monthly salary"
    # )
    
    # print(f"Transaction added with ID: {result}")
    
    # # Get all transactions
    # all_transactions = transaction_model.get_all_transactions()
    # print(f"\nTotal transactions: {len(all_transactions)}")
    
    # for trans in all_transactions[:5]:  # Show first 5
    #     trans_type = trans.get('type', 'Unknown')
    #     category = trans.get('category', 'N/A')
    #     amount = trans.get('amount', 0)
    #     print(f"- {trans_type}: {category} - ${amount}")
    
    # test delete transaction
    result = transaction_model.delete_transaction("6925b286782868e2a256c9bc")
    print(f"Deleted {result} transaction(s)")