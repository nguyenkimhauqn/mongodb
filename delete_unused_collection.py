"""
Script để xóa collection không sử dụng
"""
from dataset.database_manager import DatabaseManager

def delete_collection(collection_name: str):
    """Xóa collection khỏi database"""
    try:
        db_manager = DatabaseManager()
        
        # Kiểm tra collection có tồn tại không
        if collection_name in db_manager.db.list_collection_names():
            # Xóa collection
            db_manager.db.drop_collection(collection_name)
            print(f"✅ Đã xóa collection '{collection_name}' thành công!")
        else:
            print(f"⚠️ Collection '{collection_name}' không tồn tại!")
            
    except Exception as e:
        print(f"❌ Lỗi khi xóa collection: {e}")
    finally:
        db_manager.close_connection()

if __name__ == "__main__":
    # Xóa collection 'user' không sử dụng
    collection_to_delete = "user"
    
    print(f"🗑️ Đang xóa collection: {collection_to_delete}")
    confirm = input(f"⚠️ Bạn có chắc chắn muốn xóa collection '{collection_to_delete}'? (yes/no): ")
    
    if confirm.lower() in ['yes', 'y']:
        delete_collection(collection_to_delete)
    else:
        print("❌ Hủy thao tác xóa!")
