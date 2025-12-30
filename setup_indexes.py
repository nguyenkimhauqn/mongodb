"""
Setup MongoDB indexes for Finance Tracker
Chạy script này MỘT LẦN để tạo unique index cho budgets collection
"""

from dataset.database_manager import DatabaseManager
import config

def create_budget_unique_index():
    """
    Tạo compound unique index cho budgets collection
    Đảm bảo mỗi user chỉ có 1 budget cho mỗi category + month + year
    """
    db_manager = DatabaseManager()
    budgets_collection = db_manager.get_collection(config.COLLECTIONS['budget'])
    
    try:
        # Tạo compound unique index
        index_name = budgets_collection.create_index(
            [
                ('user_id', 1),
                ('category', 1),
                ('month', 1),
                ('year', 1),
                ('is_active', 1)
            ],
            unique=True,
            name='unique_user_category_month_year'
        )
        
        print(f"✅ Đã tạo unique index: {index_name}")
        
        # Liệt kê tất cả indexes
        indexes = budgets_collection.index_information()
        print("\n📋 Danh sách indexes trong collection 'budgets':")
        for idx_name, idx_info in indexes.items():
            print(f"  - {idx_name}: {idx_info['key']}")
        
        return True
    
    except Exception as e:
        print(f"❌ Lỗi khi tạo index: {e}")
        return False

def verify_indexes():
    """Kiểm tra indexes đã tạo"""
    db_manager = DatabaseManager()
    budgets_collection = db_manager.get_collection(config.COLLECTIONS['budget'])
    
    indexes = budgets_collection.index_information()
    
    print("\n🔍 KIỂM TRA INDEXES:")
    if 'unique_user_category_month_year' in indexes:
        print("✅ Unique index đã tồn tại")
        print(f"   Details: {indexes['unique_user_category_month_year']}")
    else:
        print("❌ Unique index CHƯA được tạo!")

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 SETUP MONGODB INDEXES")
    print("=" * 60)
    
    # Tạo index
    create_budget_unique_index()
    
    # Verify
    verify_indexes()
    
    print("\n✅ HOÀN THÀNH!")
    print("=" * 60)
