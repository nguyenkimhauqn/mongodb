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

    def update_category(self, old_name: str, new_name: str, old_type: str, new_type: str = None):
        """
        Update category name and/or type, with transaction sync
        
        Args:
            old_name: Current category name
            new_name: New category name
            old_type: Current category type (Expense/Income)
            new_type: New category type (optional, if changing type)
        
        Returns:
            (success: bool, message: str, counts: dict)
        """
        from dataset.transaction_model import TransactionModel
        from dataset.budget_model import BudgetModel
        
        # Use old_type if new_type not provided (rename only)
        if new_type is None:
            new_type = old_type
        
        # VALIDATION 1: Check duplicate name in target type
        existing = self.collection.find_one({
            "name": new_name,
            "type": new_type,
            "user_id": self.user_id
        })
        
        # If exists and it's not the same category
        if existing and (existing.get('name') != old_name or existing.get('type') != old_type):
            return False, f"❌ Category '{new_name}' already exists in {new_type}", {}
        
        trans_model = TransactionModel()
        trans_model.set_user_id(str(self.user_id))
        
        budget_model = BudgetModel()
        budget_model.set_user_id(str(self.user_id))
        
        counts = {
            "transactions": 0,
            "budgets": 0
        }
        
        # CASE 1: Only rename (same type)
        if old_type == new_type:
            # Update category name
            cat_result = self.collection.update_one(
                {"name": old_name, "type": old_type, "user_id": self.user_id},
                {"$set": {"name": new_name, "last_modified": datetime.now()}}
            )
            
            if cat_result.modified_count == 0:
                return False, "❌ Category not found", counts
            
            # Sync transactions (MongoDB update_many - NO LOOP)
            trans_result = trans_model.collection.update_many(
                {"category": old_name, "user_id": self.user_id},
                {"$set": {"category": new_name}}
            )
            counts["transactions"] = trans_result.modified_count
            
            # Sync budgets (MongoDB update_many - NO LOOP)
            budget_result = budget_model.collection.update_many(
                {"category": old_name, "user_id": self.user_id},
                {"$set": {"category": new_name}}
            )
            counts["budgets"] = budget_result.modified_count
            
            message = f"✅ Renamed to '{new_name}' and updated {counts['transactions']} transactions, {counts['budgets']} budgets"
            return True, message, counts
        
        # CASE 2: Change type (Expense ↔ Income)
        else:
            # Count affected transactions
            trans_count = trans_model.collection.count_documents({
                "category": old_name,
                "user_id": self.user_id
            })
            
            # Count affected budgets
            budget_count = budget_model.collection.count_documents({
                "category": old_name,
                "user_id": self.user_id
            })
            
            # VALIDATION 2: Block type change if has transactions or budgets
            if trans_count > 0 or budget_count > 0:
                return False, f"❌ Cannot change type. Found {trans_count} transactions and {budget_count} budgets with this category", {}
            
            # No transactions/budgets, safe to change type
            cat_result = self.collection.update_one(
                {"name": old_name, "type": old_type, "user_id": self.user_id},
                {"$set": {"name": new_name, "type": new_type, "last_modified": datetime.now()}}
            )
            
            if cat_result.modified_count > 0:
                message = f"✅ Changed '{old_name}' ({old_type}) → '{new_name}' ({new_type})"
                return True, message, counts
            else:
                return False, "❌ Category not found", counts
    
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
        
        # Count affected data using MongoDB count_documents (NO LOOP)
        related_trans_count = trans_model.collection.count_documents({
            "category": category_name,
            "user_id": self.user_id
        })
        
        related_budgets_count = budget_model.collection.count_documents({
            "category": category_name,
            "user_id": self.user_id,
            "is_active": True
        })
        
        counts = {
            "transactions": related_trans_count,
            "budgets": related_budgets_count,
            "transactions_moved": 0,
            "transactions_deleted": 0,
            "budgets_moved": 0,
            "budgets_deleted": 0
        }
        
        # If no related data, just delete
        if related_trans_count == 0 and related_budgets_count == 0:
            result = self.delete_category(category_type, category_name)
            message = "✅ Category deleted successfully" if result > 0 else "❌ Failed to delete category"
            return result > 0, message, counts
        
        # Handle based on action
        if action == "cancel":
            message = f"❌ Deletion cancelled. Found {related_trans_count} transactions and {related_budgets_count} budgets"
            return False, message, counts
        
        elif action == "move_to_others":
            # Ensure "Others" category exists
            self.upsert_category(category_type, "Others")
            
            # Move transactions using MongoDB update_many (NO LOOP)
            if related_trans_count > 0:
                trans_result = trans_model.collection.update_many(
                    {"category": category_name, "user_id": self.user_id},
                    {"$set": {"category": "Others"}}
                )
                counts["transactions_moved"] = trans_result.modified_count
            
            # Move budgets using MongoDB update_many (NO LOOP)
            if related_budgets_count > 0:
                budget_result = budget_model.collection.update_many(
                    {"category": category_name, "user_id": self.user_id},
                    {"$set": {"category": "Others"}}
                )
                counts["budgets_moved"] = budget_result.modified_count
            
            message = f"✅ Moved {counts['transactions_moved']} transactions and {counts['budgets_moved']} budgets to 'Others'"
        
        elif action == "delete_all":
            # Delete transactions using MongoDB delete_many (NO LOOP)
            if related_trans_count > 0:
                trans_result = trans_model.collection.delete_many({
                    "category": category_name,
                    "user_id": self.user_id
                })
                counts["transactions_deleted"] = trans_result.deleted_count
            
            # Delete budgets using MongoDB delete_many (NO LOOP)
            if related_budgets_count > 0:
                budget_result = budget_model.collection.delete_many({
                    "category": category_name,
                    "user_id": self.user_id
                })
                counts["budgets_deleted"] = budget_result.deleted_count
            
            message = f"✅ Deleted {counts['transactions_deleted']} transactions and {counts['budgets_deleted']} budgets"
        
        # Delete category
        result = self.delete_category(category_type, category_name)
        if result > 0:
            return True, message, counts
        else:
            return False, "❌ Failed to delete category", counts

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