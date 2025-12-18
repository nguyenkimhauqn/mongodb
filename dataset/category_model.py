from dataset.database_manager import DatabaseManager
import config
from datetime import datetime
from typing import Optional
from bson.objectid import ObjectId

collection_name = config.COLLECTIONS['category']

class CategoryModel:
    def __init__(self, user_id: Optional[str] = None):
        self.db_manager = DatabaseManager()
        self.collection = self.db_manager.get_collection(collection_name=collection_name)

        # init:
        self.user_id = user_id

    def set_user_id(self, user_id: str):
        self.user_id = ObjectId(user_id) if user_id is not None else None

        # after we have user_id, initialize their default categories
        self._initialize_user_default_categories()

    def _initialize_user_default_categories(self):
        """Initialize user categories if they dont exist"""

        # Check if there is user_id, exist earlier
        if not self.user_id:
            return
        
        # EXPENSE
        for cate in config.DEFAULT_CATEGORIES_EXPENSE:
            # # calling by params order
            # self.upsert_category("Expense", cate)

            # calling by params keywords
            self.upsert_category(category_type = "Expense", category_name= cate)

        # INCOME
        for cate in config.DEFAULT_CATEGORIES_INCOME:
            self.upsert_category(category_type = "Income", category_name = cate)

    def upsert_category(self, category_type: str, category_name: str):

        # define filter
        filter_ = {
            "type": category_type,
            "name": category_name,
            "user_id": self.user_id
        }

        # define update_doc
        update_doc = {
            "$set": {
                "last_modified": datetime.now()
            },
            "$setOnInsert": {
                "created_at": datetime.now()
            } 
        }

        result = self.collection.update_one(
            filter_,
            update_doc,
            upsert=True
        )
        return result.upserted_id

    def update_category(self, old_name: str, new_name: str, category_type: str):
        """
        Rename category and update all related data
        
        Returns:
            (success: bool, error_message: str)
        """
        # Check if new name already exists
        existing = self.collection.find_one({
            "name": new_name,
            "type": category_type,
            "user_id": self.user_id
        })
        
        if existing:
            return False, "Category name already exists"
        
        # Update category
        result = self.collection.update_one(
            {"name": old_name, "type": category_type, "user_id": self.user_id},
            {"$set": {"name": new_name, "last_modified": datetime.now()}}
        )
        
        if result.modified_count > 0:
            # Update transactions
            from dataset.transaction_model import TransactionModel
            trans_model = TransactionModel()
            trans_model.set_user_id(str(self.user_id))
            trans_model.collection.update_many(
                {"category": old_name, "user_id": self.user_id},
                {"$set": {"category": new_name}}
            )
            
            # Update budgets
            from dataset.budget_model import BudgetModel
            budget_model = BudgetModel()
            budget_model.set_user_id(str(self.user_id))
            budget_model.collection.update_many(
                {"category": old_name, "user_id": self.user_id},
                {"$set": {"category": new_name}}
            )
            
            return True, None
        
        return False, "Category not found"
    
    def delete_category(self, category_type: str, category_name: str):
        result = self.collection.delete_one({"type": category_type, "name": category_name, "user_id": self.user_id}) # add user_id condition
        return result.deleted_count
    
    def delete_category_with_handling(self, category_type: str, category_name: str, action: str = "cancel"):
        """
        Delete category with transaction and budget handling
        
        Args:
            action: "move_to_others" | "delete_all" | "cancel"
        
        Returns:
            (success: bool, message: str, counts: dict)
        """
        from dataset.transaction_model import TransactionModel
        from dataset.budget_model import BudgetModel
        
        trans_model = TransactionModel()
        trans_model.set_user_id(str(self.user_id))
        
        budget_model = BudgetModel()
        budget_model.set_user_id(str(self.user_id))
        
        # Check transactions
        related_trans_count = trans_model.collection.count_documents({
            "category": category_name,
            "user_id": self.user_id
        })
        
        # Check budgets
        related_budgets_count = budget_model.collection.count_documents({
            "category": category_name,
            "user_id": self.user_id,
            "is_active": True
        })
        
        counts = {
            "transactions": related_trans_count,
            "budgets": related_budgets_count
        }
        
        # If no related data, just delete
        if related_trans_count == 0 and related_budgets_count == 0:
            result = self.delete_category(category_type, category_name)
            return result > 0, None, counts
        
        # Handle based on action
        if action == "cancel":
            return False, f"Cannot delete. Found {related_trans_count} transactions and {related_budgets_count} budgets", counts
        
        elif action == "move_to_others":
            # Ensure "Others" category exists
            self.upsert_category(category_type, "Others")
            
            # Move transactions
            if related_trans_count > 0:
                trans_model.collection.update_many(
                    {"category": category_name, "user_id": self.user_id},
                    {"$set": {"category": "Others"}}
                )
            
            # Move budgets
            if related_budgets_count > 0:
                budget_model.collection.update_many(
                    {"category": category_name, "user_id": self.user_id},
                    {"$set": {"category": "Others"}}
                )
        
        elif action == "delete_all":
            # Delete transactions
            if related_trans_count > 0:
                trans_model.collection.delete_many({
                    "category": category_name,
                    "user_id": self.user_id
                })
            
            # Delete budgets
            if related_budgets_count > 0:
                budget_model.collection.delete_many({
                    "category": category_name,
                    "user_id": self.user_id
                })
        
        # Delete category
        result = self.delete_category(category_type, category_name)
        return result > 0, None, counts

    def get_categories_by_type(self, category_type: str):
        return list(self.collection.find({"type": category_type, "user_id": self.user_id}).sort("created_at", -1))  # add user_id condition
    
    def get_categories_by_user_id(self, user_id: str):
        """Get all categories for a specific user (admin function)"""
        return list(self.collection.find({"user_id": ObjectId(user_id)}).sort("created_at", -1))
    
    def get_total(self):
        result = self.collection.find({"user_id": self.user_id})
        result = list(result)
        return result

# if __name__ == "__main__":
#     print("Init cate collection")
#     cate = CategoryModel()

#     item = {
#         "type": "Expense",
#         "name": "Rent"
#     }

#     result = cate.add_category(category_type = "Expense", category_name="Rent")