from dataset.database_manager import DatabaseManager
import config
from datetime import datetime
from typing import Optional, List
from bson.objectid import ObjectId


collection_name = config.COLLECTIONS['budget']


class BudgetModel:
    def __init__(self, user_id: Optional[str] = None):
        self.db_manager = DatabaseManager()
        self.collection = self.db_manager.get_collection(collection_name=collection_name)
        self.user_id = ObjectId(user_id) if user_id else None

    def set_user_id(self, user_id: str):
        """Set the current user id for scoped queries"""
        self.user_id = ObjectId(user_id) if user_id is not None else None

    def create_budget(
        self,
        category: str,
        amount: float,
        month: int,  # 1-12
        year: int,   # e.g., 2025
    ) -> Optional[str]:
        """
        Create a new budget for a category in a specific month
        
        Args:
            category: Category name
            amount: Budget amount
            month: Month (1-12)
            year: Year (e.g., 2025)
        
        Returns:
            Inserted budget ID as string, or None if failed
        """
        if not self.user_id:
            raise ValueError("User ID must be set before creating budget")

        # Check if budget already exists for this user-category-month (UNIQUE CONSTRAINT)
        existing = self.collection.find_one({
            'user_id': self.user_id,
            'category': category,
            'month': month,
            'year': year,
            'is_active': True
        })

        if existing:
            # Update existing budget instead (only 1 budget per user-category-month)
            return self.update_budget(str(existing['_id']), amount=amount)

        budget = {
            'user_id': self.user_id,
            'category': category,
            'amount': amount,
            'month': month,
            'year': year,
            'is_active': True,
            'created_at': datetime.now(),
            'last_modified': datetime.now()
        }

        try:
            result = self.collection.insert_one(budget)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error creating budget: {e}")
            return None

    def update_budget(
        self,
        budget_id: str,
        **kwargs
    ) -> bool:
        """
        Update an existing budget
        
        Args:
            budget_id: Budget ID
            **kwargs: Fields to update (amount, period, is_active, etc.)
        
        Returns:
            True if updated successfully, False otherwise
        """
        try:
            kwargs['last_modified'] = datetime.now()
            
            filter_ = {
                '_id': ObjectId(budget_id),
                'user_id': self.user_id
            }
            
            result = self.collection.update_one(filter_, {'$set': kwargs})
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating budget: {e}")
            return False

    def delete_budget(self, budget_id: str) -> bool:
        """
        Delete a budget (soft delete by setting is_active=False)
        
        Args:
            budget_id: Budget ID
        
        Returns:
            True if deleted successfully, False otherwise
        """
        return self.update_budget(budget_id, is_active=False)

    def get_budget_by_id(self, budget_id: str) -> Optional[dict]:
        """Get a single budget by ID"""
        try:
            filter_ = {
                '_id': ObjectId(budget_id),
                'user_id': self.user_id
            }
            return self.collection.find_one(filter_)
        except Exception as e:
            print(f"Error getting budget: {e}")
            return None

    def get_all_budgets(self, include_inactive: bool = False) -> List[dict]:
        """
        Get all budgets for current user
        
        Args:
            include_inactive: Whether to include inactive budgets
        
        Returns:
            List of budget documents
        """
        query = {'user_id': self.user_id}
        
        if not include_inactive:
            query['is_active'] = True
        
        cursor = self.collection.find(query).sort([('year', -1), ('month', -1)])
        return list(cursor)

    def get_budget_by_category_month(self, category: str, month: int, year: int) -> Optional[dict]:
        """Get active budget for a specific category and month"""
        query = {
            'user_id': self.user_id,
            'category': category,
            'month': month,
            'year': year,
            'is_active': True
        }
        return self.collection.find_one(query)

    def get_budgets_by_month(self, month: int, year: int) -> List[dict]:
        """Get all active budgets for a specific month"""
        query = {
            'user_id': self.user_id,
            'month': month,
            'year': year,
            'is_active': True
        }
        cursor = self.collection.find(query).sort('created_at', -1)
        return list(cursor)
    
    def get_budgets_by_category(self, category_name: str) -> List[dict]:
        """Get all budgets for a specific category"""
        query = {
            'user_id': self.user_id,
            'category': category_name,
            'is_active': True
        }
        cursor = self.collection.find(query).sort('created_at', -1)
        return list(cursor)
    
    def get_budgets_by_user_id(self, user_id: str) -> List[dict]:
        """Get all budgets for a specific user (admin function)"""
        query = {
            'user_id': ObjectId(user_id),
            'is_active': True
        }
        cursor = self.collection.find(query).sort('created_at', -1)
        return list(cursor)

    def check_budget_status(self, category: str, month: int, year: int, spent_amount: float) -> dict:
        """
        Check budget status for a category in a specific month
        
        Args:
            category: Category name
            month: Month (1-12)
            year: Year
            spent_amount: Amount already spent
        
        Returns:
            Dictionary with budget status information
        """
        budget = self.get_budget_by_category_month(category, month, year)
        
        if not budget:
            return {
                'has_budget': False,
                'budget_amount': 0,
                'spent_amount': spent_amount,
                'remaining': 0,
                'percentage': 0,
                'status': 'no_budget',
                'month': month,
                'year': year
            }

        budget_amount = budget.get('amount', 0)
        remaining = budget_amount - spent_amount
        percentage = (spent_amount / budget_amount * 100) if budget_amount > 0 else 0

        # Determine status
        if percentage < 50:
            status = 'safe'
        elif percentage < 80:
            status = 'warning'
        elif percentage < 100:
            status = 'danger'
        else:
            status = 'exceeded'

        return {
            'has_budget': True,
            'budget_id': str(budget['_id']),
            'budget_amount': budget_amount,
            'spent_amount': spent_amount,
            'remaining': remaining,
            'percentage': percentage,
            'status': status,
            'month': month,
            'year': year
        }

    def get_budget_summary(self, transaction_model, month: int = None, year: int = None) -> List[dict]:
        """
        Get comprehensive budget summary with spending data for a specific month
        
        Args:
            transaction_model: TransactionModel instance to get spending data
            month: Month to get summary for (default: current month)
            year: Year to get summary for (default: current year)
        
        Returns:
            List of budget summaries with actual spending
        """
        # Use current month/year if not specified
        if month is None or year is None:
            now = datetime.now()
            month = month or now.month
            year = year or now.year
        
        # Get budgets for this month
        budgets = self.get_budgets_by_month(month, year)
        summary = []

        for budget in budgets:
            category = budget.get('category')
            budget_amount = budget.get('amount', 0)
            budget_month = budget.get('month')
            budget_year = budget.get('year')

            # Get actual spending for this category IN THIS MONTH
            from datetime import date
            start_date = date(budget_year, budget_month, 1)
            # Get last day of month
            if budget_month == 12:
                end_date = date(budget_year + 1, 1, 1)
            else:
                end_date = date(budget_year, budget_month + 1, 1)
            
            transactions = transaction_model.get_transactions(
                advanced_filters={
                    'category': category, 
                    'transaction_type': 'Expense',
                    'start_date': start_date,
                    'end_date': end_date
                }
            )

            spent_amount = sum(t.get('amount', 0) for t in transactions)
            
            status = self.check_budget_status(category, budget_month, budget_year, spent_amount)

            summary.append({
                'budget_id': str(budget['_id']),
                'category': category,
                'budget_amount': budget_amount,
                'spent_amount': spent_amount,
                'remaining': status['remaining'],
                'percentage': status['percentage'],
                'status': status['status'],
                'month': budget_month,
                'year': budget_year,
                'created_at': budget.get('created_at')
            })

        return summary
