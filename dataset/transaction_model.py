from typing import Optional, Any
from datetime import datetime, date
from bson.objectid import ObjectId
from .database_manager import DatabaseManager
import config
from pymongo import DESCENDING, ASCENDING
from utils import handler_datetime


class TransactionModel:

    def __init__(self, user_id: Optional[str] = None):
        self.db_manager = DatabaseManager()
        self.collection = self.db_manager.get_collection(config.COLLECTIONS["transaction"])
        self.user_id = user_id

    def set_user_id(self, user_id: Optional[str]):
        """Set or clear the current user id used to scope queries."""
        self.user_id = ObjectId(user_id) if user_id is not None else None
    
    def get_transactions(
        self,
        advanced_filters: dict[str, any] = None
    ) -> list[dict]:

        # Build query filter
        query = self._build_query(advanced_filters)
              
        # Fetch transactions, sort from newest to oldest
        cursor = self.collection.find(query).sort("created_at", -1)
        return list(cursor)     
    
    def _build_query(self, advanced_filter: Optional[dict]) -> dict:
        conditions = []
        if not advanced_filter:
            return self._add_user_constraint(conditions)
        
        # Check transaction_type:
        if "transaction_type" in advanced_filter:
            conditions.append({"type": advanced_filter.get("transaction_type")})

        # Check Category:
        if "category" in advanced_filter:
            conditions.append({"category": advanced_filter.get("category")})

        # Check amount:
        min_amount = advanced_filter.get("min_amount")
        max_amount = advanced_filter.get("max_amount")
        if min_amount or max_amount:
            amount = {}
            if min_amount is not None:
                amount["$gte"] = min_amount # $gte = greater than or equal
            if max_amount is not None:
                amount["$lte"] = max_amount # $lte = less than or equal

            conditions.append({"amount": amount})

        # Check datetime
        start_date = advanced_filter.get("start_date")
        end_date = advanced_filter.get("end_date")
        if start_date or end_date:

            date_query = {}
            if start_date is not None:
                date_query["$gte"] = handler_datetime(start_date) # $gte = greater than or equal
            if end_date is not None:
                date_query["$lte"] = handler_datetime(end_date) # $lte = less than or equal
            conditions.append({"date": date_query})

        # Check description:
        if "search_text" in advanced_filter:
            conditions.append({
                "description": {
                    "$regex": advanced_filter.get("search_text"),
                    "$options": "i"  # case-insensitive
                }
            })

        return self._add_user_constraint(conditions)
    
    def _add_user_constraint(self, conditions: list) -> dict:
        conditions.append({
            "user_id": ObjectId(self.user_id) if self.user_id else None
        })
        return {
            "$and": conditions
        }
    
    def _validate_category(self, category: str, transaction_type: str) -> bool:
        """
        Validate that category exists and matches the transaction type.
        
        Args:
            category: Category name
            transaction_type: 'Expense' or 'Income'
        
        Returns:
            True if valid, False otherwise
        
        Raises:
            ValueError: If category doesn't exist or type doesn't match
        """
        if not self.user_id:
            raise ValueError("User ID must be set before validating category")
        
        # Get category collection
        category_collection = self.db_manager.get_collection(config.COLLECTIONS['category'])
        
        # Check if category exists and type matches
        existing_category = category_collection.find_one({
            'user_id': self.user_id,
            'name': category,
            'type': transaction_type
        })
        
        if not existing_category:
            raise ValueError(
                f"Category '{category}' không tồn tại hoặc không khớp với transaction type '{transaction_type}'"
            )
        
        return True
    
    def add_transaction(
        self,
        transaction_type: str,
        category: str,
        amount: float,
        transaction_date: datetime,
        description: str = ""
    ) -> Optional[str]:
        """
        Add a new transaction with automatic last_modified timestamp.
        ✅ VALIDATION: Category phải tồn tại và type phải khớp với transaction_type
        
        Args:
            transaction_type: 'Expense' or 'Income'
            category: Category name
            amount: Transaction amount
            transaction_date: Transaction date
            description: Optional description
        
        Returns:
            Inserted document ID as string, or None if failed
        
        Raises:
            ValueError: If category validation fails
        """
        # ✅ VALIDATION: Category phải tồn tại và type phải khớp
        self._validate_category(category, transaction_type)
        
        if not isinstance(transaction_date, datetime):
            transaction_date = handler_datetime(transaction_date)

        transaction = {
            'type': transaction_type,
            'category': category,
            'amount': amount,
            'date': transaction_date,
            'description': description,
            'created_at': datetime.now(),
            'last_modified': datetime.now(),
            'user_id': self.user_id ## added user_id field
        }

        try:
            result = self.collection.insert_one(transaction)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error adding transaction: {e}")
            return None
    
    def update_transaction(
        self,
        transaction_id: str,
        **kwargs
    ) -> bool:
        """
        Update a transaction and set last_modified timestamp.
        ✅ VALIDATION: Nếu update category hoặc type, validate category tồn tại và khớp type
        
        Args:
            transaction_id: Transaction ID
            **kwargs: Fields to update (category, type, amount, date, description, etc.)
        
        Returns:
            True if updated successfully, False otherwise
        
        Raises:
            ValueError: If category validation fails
        """
        try:
            # ✅ VALIDATION: Nếu update category hoặc type, validate
            if 'category' in kwargs or 'type' in kwargs:
                # Get current transaction to determine transaction_type
                current_trans = self.get_transaction_by_id(transaction_id)
                if not current_trans:
                    raise ValueError(f"Transaction {transaction_id} not found")
                
                # Use new type if provided, otherwise use current type
                transaction_type = kwargs.get('type', current_trans.get('type'))
                category = kwargs.get('category', current_trans.get('category'))
                
                # Validate category exists and matches transaction type
                self._validate_category(category, transaction_type)
            
            # Add last_modified timestamp
            kwargs['last_modified'] = datetime.now()
            # Build filter and scope by user if available
            filter_ = {'_id': ObjectId(transaction_id),
                       'user_id': self.user_id} # added user_id constraint
            result = self.collection.update_one(filter_, {'$set': kwargs})
            return result.modified_count > 0
        except ValueError:
            # Re-raise ValueError (validation errors)
            raise
        except Exception as e:
            print(f"Error updating transaction: {e}")
            return False
    
    def delete_transaction(self, transaction_id: str) -> bool:
        """
        Delete a transaction.
        
        Args:
            transaction_id: Transaction ID
        
        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            filter_ = {'_id': ObjectId(transaction_id),
                       'user_id': self.user_id} # added user_id constraint
            
            result = self.collection.delete_one(filter_)
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting transaction: {e}")
            return False
    
    def get_transaction_by_id(self, transaction_id: str) -> Optional[dict]:
        """
        Get a single transaction by ID.
        
        Args:
            transaction_id: Transaction ID
        
        Returns:
            Transaction document or None
        """
        try:
            filter_ = {'_id': ObjectId(transaction_id),
                       'user_id': self.user_id} # added user_id constraint
            return self.collection.find_one(filter_)
        except Exception as e:
            print(f"Error getting transaction: {e}")
            return None
        
    def get_transactions_by_date_range(
        self,
        start_date: datetime | date | str,
        end_date: datetime | date | str
    ) -> list[dict]:
        """
        Legacy method: Get transactions in date range.
        
        Args:
            start_date: Start date
            end_date: End date
        
        Returns:
            list of transaction documents
        """
        return self.get_transactions(
            advanced_filters= {
                "start_date": start_date,
                "end_date": end_date,
            }
        )
    
    def get_all_transactions(self) -> list[dict]:
        """
        Get all transactions for the current user.
        
        Returns:
            list of transaction documents sorted by created_at descending
        """
        return self.get_transactions()
    
    def get_transactions_by_type(self, transaction_type: str) -> list[dict]:
        """
        Get transactions filtered by type (Income/Expense).
        
        Args:
            transaction_type: 'Income' or 'Expense'
        
        Returns:
            list of transaction documents
        """
        return self.get_transactions(
            advanced_filters={"transaction_type": transaction_type}
        )
    
    def get_transactions_by_category(self, category_name: str) -> list[dict]:
        """
        Get transactions filtered by category name.
        
        Args:
            category_name: Name of the category
        
        Returns:
            list of transaction documents
        """
        return self.get_transactions(
            advanced_filters={"category": category_name}
        )
    
    def get_transactions_by_user_id(self, user_id: str) -> list[dict]:
        """
        Get all transactions for a specific user (admin function).
        
        Args:
            user_id: User ID to filter by
        
        Returns:
            list of transaction documents
        """
        query = {"user_id": ObjectId(user_id)}
        cursor = self.collection.find(query).sort("created_at", -1)
        return list(cursor)
    
    def get_statistics(self) -> dict:
        """
        Get transaction statistics for the current user.
        
        Returns:
            dict with statistics: total_income, total_expense, balance, counts
        """
        all_trans = self.get_all_transactions()
        
        stats = {
            'total_income': 0.0,
            'total_expense': 0.0,
            'income_count': 0,
            'expense_count': 0,
            'total_transactions': len(all_trans),
            'balance': 0.0
        }
        
        for trans in all_trans:
            amount = trans.get('amount', 0)
            trans_type = trans.get('type', '')
            
            if trans_type == 'Income':
                stats['total_income'] += amount
                stats['income_count'] += 1
            elif trans_type == 'Expense':
                stats['total_expense'] += amount
                stats['expense_count'] += 1
        
        stats['balance'] = stats['total_income'] - stats['total_expense']
        
        return stats
