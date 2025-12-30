from dataset.database_manager import DatabaseManager
import config
from datetime import datetime
from bson.objectid import ObjectId

collection_name = config.COLLECTIONS['user']

class UserModel:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.collection = self.db_manager.get_collection(collection_name=collection_name)

    def create_user(self, email: str) -> str:
        """Create new user"""

        user = {
            "email": email,
            "created_at": datetime.now(),
            "last_modified": datetime.now(),
            "is_activate": True
        }

        result = self.collection.insert_one(user)
        return str(result.inserted_id)
    
    def login(self, email: str) -> str:
        # check user exist (use find_one)
        user = self.collection.find_one({'email': email})
        
        # case 1: user not exist:
        # create: call create_user(email)
        if not user:
            return self.create_user(email)

        # case 2: user exist but deactivate
        # raise Error
        if user.get("is_activate") is not True:
            raise ValueError("This account is deactivated! Please connect to CS")

        # all checking passed
        return str(user.get("_id"))
    
    def deactivate(self, user_id: str) -> bool:
        # find and update:
        user = self.collection.find_one({
            "_id": ObjectId(user_id),
            "is_activate": True
        })

        # case: not exist user
        if not user:
            raise ValueError("User not found")
        
        # user is validate and ready to deactivate -> update them
        result = self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"is_activate": False}}
        )

        return result.modified_count > 0
    
    def delete_user_completely(self, user_id: str) -> dict:
        """
        Delete user and all related data (CASCADE DELETE)
        
        Returns:
            dict with deletion counts
        """
        try:
            user_oid = ObjectId(user_id)
            
            # Check if user exists
            user = self.collection.find_one({"_id": user_oid})
            if not user:
                return {"success": False, "error": "User not found"}
            
            counts = {}
            
            # Delete transactions (delete_many - NO LOOP)
            trans_collection = self.db_manager.get_collection(config.COLLECTIONS['transaction'])
            trans_result = trans_collection.delete_many({"user_id": user_oid})
            counts['transactions'] = trans_result.deleted_count
            
            # Delete budgets (delete_many - NO LOOP)
            budget_collection = self.db_manager.get_collection(config.COLLECTIONS['budget'])
            budget_result = budget_collection.delete_many({"user_id": user_oid})
            counts['budgets'] = budget_result.deleted_count
            
            # Delete custom categories (delete_many - NO LOOP)
            # NOTE: Only delete categories created by user, keep system defaults
            category_collection = self.db_manager.get_collection(config.COLLECTIONS['category'])
            category_result = category_collection.delete_many({"user_id": user_oid})
            counts['categories'] = category_result.deleted_count
            
            # Delete user (delete_one)
            user_result = self.collection.delete_one({"_id": user_oid})
            counts['users'] = user_result.deleted_count
            
            # Format summary message
            message = f"Deleted: {counts['users']} user, {counts['transactions']} transactions, {counts['budgets']} budgets, {counts['categories']} categories"
            
            return {
                "success": True,
                "counts": counts,
                "message": message,
                "total": sum(counts.values())
            }
        except Exception as e:
            print(f"Error deleting user: {e}")
            return {"success": False, "error": str(e)}