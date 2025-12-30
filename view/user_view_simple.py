"""
Simplified User View - Using Streamlit native components
Less HTML, more Streamlit widgets for better compatibility
"""
from dataset.user_model import UserModel
import streamlit as st
import time
from language_manager import t


def render_user_profile(user_model: UserModel, user: dict):
    """
    Render user profile using Streamlit native components (simplified)
    """
    if 'user_settings_open' not in st.session_state:
        st.session_state['user_settings_open'] = False

    with st.sidebar:
        # Simple styling
        st.markdown("""
            <style>
            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #e0e7ff 0%, #f9fafb 100%);
            }
            </style>
        """, unsafe_allow_html=True)
        
        # Get user info
        name = user.get("given_name") or user.get("name") or "User"
        email = user.get("email") or ""
        avatar_url = user.get("picture")
        
        # User profile card using Streamlit components
        st.markdown("### 👤 " + name)
        st.markdown(f"**✉️** {email}")
        
        st.divider()
        
        # Settings button
        if st.button(f"⚙️ {t('account_settings')}", key="settings_toggle", use_container_width=True):
            st.session_state['user_settings_open'] = not st.session_state['user_settings_open']
        
        if st.session_state['user_settings_open']:
            _render_user_settings_simple(user_model, user.get("id"))
        
        st.divider()


def _render_user_settings_simple(user_model, user_id: str):
    """
    Simplified user settings with native Streamlit components
    """
    st.markdown("### ⚙️ Cài Đặt Tài Khoản")
    
    # Logout and Deactivate buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(f"🚪 {t('nav_logout')}", use_container_width=True, key="logout_button"):
            # For simple login, just clear session
            st.session_state['is_logged_in'] = False
            st.session_state['user_email'] = None
            st.rerun()
    
    with col2:
        if st.button(f"❌ {t('deactivate')}", use_container_width=True, key="deactivate_button"):
            if user_id:
                user_model.deactivate(user_id)
                st.success(t('account_deactivated'))
                time.sleep(1)
                st.session_state['is_logged_in'] = False
                st.rerun()
            else:
                st.error(t('error'))
    
    st.divider()
    
    # User information
    from bson.objectid import ObjectId
    user_doc = user_model.collection.find_one({"_id": ObjectId(user_id)})
    
    if user_doc:
        st.markdown("### 👤 Thông Tin Tài Khoản")
        
        email = user_doc.get('email', 'N/A')
        created_at = user_doc.get('created_at', 'N/A')
        
        if created_at != 'N/A':
            created_str = created_at.strftime("%d/%m/%Y %H:%M")
        else:
            created_str = "N/A"
        
        # Display info in a clean box
        st.info(f"""
**📧 Email:** {email}

**🆔 User ID:** `{str(user_id)[:8]}...`

**📅 Ngày Tạo:** {created_str}
        """)
        
        # Count user data for stats
        from dataset.transaction_model import TransactionModel
        from dataset.budget_model import BudgetModel
        from dataset.category_model import CategoryModel
        
        trans_model = TransactionModel()
        budget_model = BudgetModel()
        category_model = CategoryModel()
        
        user_oid = ObjectId(user_id)
        
        trans_count = trans_model.collection.count_documents({"user_id": user_oid})
        budget_count = budget_model.collection.count_documents({"user_id": user_oid})
        category_count = category_model.collection.count_documents({"user_id": user_oid})
        
        # Activity statistics
        st.markdown("### 📊 Thống Kê Hoạt Động")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("💰 Giao Dịch", trans_count)
        
        with col2:
            st.metric("🔥 Ngân Sách", budget_count)
        
        with col3:
            st.metric("📂 Danh Mục", category_count)
    
    st.divider()
    
    # Delete account section
    with st.expander(f"⚠️ {t('delete_account')}", expanded=False):
        st.warning("⚠️ Hành động này **KHÔNG THỂ HOÀN TÁC**. Tất cả dữ liệu của bạn sẽ bị xóa vĩnh viễn.")
        
        if 'confirm_delete' not in st.session_state:
            st.session_state['confirm_delete'] = False
        
        if not st.session_state['confirm_delete']:
            if st.button(f"🗑️ {t('delete_account')}", key="show_delete_confirm", use_container_width=True):
                st.session_state['confirm_delete'] = True
                st.rerun()
        else:
            # Count user data
            from dataset.transaction_model import TransactionModel
            from dataset.budget_model import BudgetModel
            from dataset.category_model import CategoryModel
            from bson.objectid import ObjectId
            
            trans_model = TransactionModel()
            budget_model = BudgetModel()
            category_model = CategoryModel()
            
            user_oid = ObjectId(user_id)
            
            trans_count = trans_model.collection.count_documents({"user_id": user_oid})
            budget_count = budget_model.collection.count_documents({"user_id": user_oid})
            category_count = category_model.collection.count_documents({"user_id": user_oid})
            total_items = trans_count + budget_count + category_count + 1
            
            st.error(f"""
**XÁC NHẬN XÓA TÀI KHOẢN**

Dữ liệu sau sẽ bị xóa vĩnh viễn:
- 💰 {trans_count} giao dịch
- 🔥 {budget_count} ngân sách
- 📂 {category_count} danh mục
- 👤 1 tài khoản

**Tổng cộng: {total_items} mục**
            """)
            
            confirm_text = st.text_input(
                "Gõ chính xác 'DELETE' để xác nhận:",
                key="delete_confirm_text",
                placeholder="DELETE"
            )
            
            col_yes, col_no = st.columns(2)
            
            with col_yes:
                delete_enabled = confirm_text == "DELETE"
                if st.button(
                    "✓ Xác Nhận Xóa",
                    key="confirm_delete_yes",
                    use_container_width=True,
                    disabled=not delete_enabled
                ):
                    result = user_model.delete_user_completely(user_id)
                    if result.get("success"):
                        st.success("✅ " + result.get("message"))
                        st.balloons()
                        time.sleep(2)
                        st.session_state['is_logged_in'] = False
                        st.rerun()
                    else:
                        st.error("❌ " + result.get("error", "Unknown error"))
            
            with col_no:
                if st.button("❌ Hủy Bỏ", key="confirm_delete_no", use_container_width=True):
                    st.session_state['confirm_delete'] = False
                    st.rerun()

