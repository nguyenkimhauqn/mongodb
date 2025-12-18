from dataset.transaction_model import TransactionModel

if __name__ == "__main__":
    transaction_model = TransactionModel()
    
    # Xóa tất cả transactions không có trường category
    result = transaction_model.collection.delete_many({"category": {"$exists": False}})
    print(f"Deleted {result.deleted_count} transactions without category")
    
    # Hoặc xóa tất cả transactions
    # result = transaction_model.collection.delete_many({})
    # print(f"Deleted {result.deleted_count} all transactions")
