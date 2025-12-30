from dataset.user_model import UserModel
import streamlit as st
import time
from language_manager import t


def render_user_profile(user_model: UserModel, user: dict[str, any]):
    """
    Render a modern, beautiful user profile section in the sidebar.
    """
    if 'user_settings_open' not in st.session_state:
        st.session_state['user_settings_open'] = False

    # Create a more compact profile container
    with st.sidebar:
        st.markdown("""
            <style>
            /* Sidebar styling */
            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #e0e7ff 0%, #f9fafb 100%);
            }
            
            /* User profile card */
            .user-profile-container {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 1.5rem;
                border-radius: 20px;
                box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
                margin-bottom: 1.5rem;
                position: relative;
                overflow: hidden;
            }
            
            .user-profile-container::before {
                content: '';
                position: absolute;
                top: -50%;
                right: -50%;
                width: 200%;
                height: 200%;
                background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
                animation: pulse 4s ease-in-out infinite;
            }
            
            @keyframes pulse {
                0%, 100% { transform: scale(1); opacity: 0.5; }
                50% { transform: scale(1.1); opacity: 0.8; }
            }
            
            .user-avatar {
                border-radius: 50%;
                width: 60px;
                height: 60px;
                border: 3px solid white;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                object-fit: cover;
            }
            
            .user-info {
                flex: 1;
                padding-left: 1rem;
            }
            
            .user-name {
                color: white;
                font-weight: 700;
                font-size: 1.3rem;
                margin: 0;
                text-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            
            .user-email {
                color: rgba(255, 255, 255, 0.9);
                font-size: 0.85rem;
                margin-top: 0.3rem;
            }
            
            /* Settings button */
            .stButton > button[kind="secondary"] {
                background: white !important;
                color: #667eea !important;
                border: 2px solid #667eea !important;
                font-weight: 600 !important;
                border-radius: 12px !important;
                transition: all 0.3s ease !important;
                box-shadow: 0 4px 10px rgba(102, 126, 234, 0.2) !important;
            }
            
            .stButton > button[kind="secondary"]:hover {
                background: #667eea !important;
                color: white !important;
                transform: translateY(-2px) !important;
                box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
            }
            </style>
        """, unsafe_allow_html=True)
        
        # User profile card with gradient background
        avatar_url = user.get("picture")
        name = user.get("given_name") or user.get("name") or "User"
        email = user.get("email") or ""
        
        # Profile card HTML
        avatar_html = f'<img src="{avatar_url}" class="user-avatar"/>' if avatar_url else '''
            <div class="user-avatar" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                 display: flex; align-items: center; justify-content: center; font-size: 2rem;">
                👤
            </div>
        '''
        
        st.markdown(f"""
            <div class="user-profile-container">
                <div style="display: flex; align-items: center; position: relative; z-index: 1;">
                    {avatar_html}
                    <div class="user-info">
                        <div class="user-name">{name}</div>
                        <div class="user-email">✉️ {email}</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Settings button with modern style
        if st.button(t("account_settings"), key="settings_toggle", width='stretch', type="secondary"):
            st.session_state['user_settings_open'] = not st.session_state['user_settings_open']
        
        if st.session_state['user_settings_open']:
            _render_user_settings(user_model, user.get("id"))
        
        st.divider()


def _render_user_settings(user_model, user_id: str):
    """
    Render user settings options with better styling.
    """
    st.markdown("""
        <style>
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
            border: none !important;
            font-weight: 600 !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 10px rgba(16, 185, 129, 0.3) !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton > button[kind="primary"]:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(16, 185, 129, 0.5) !important;
        }
        
        div[data-testid="stButton"] button:not([kind]) {
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
            color: white !important;
            border: none !important;
            font-weight: 600 !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 10px rgba(239, 68, 68, 0.3) !important;
            transition: all 0.3s ease !important;
        }
        
        div[data-testid="stButton"] button:not([kind]):hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(239, 68, 68, 0.5) !important;
        }
        </style>
        
        <div style='background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); 
                    padding: 1.2rem; border-radius: 15px; margin: 1rem 0;
                    border-left: 4px solid #667eea; box-shadow: 0 2px 8px rgba(0,0,0,0.05);'>
            <div style='font-weight: 700; color: #1e40af; margin-bottom: 1rem; font-size: 1.1rem;'>
                ⚙️ Cài Đặt Tài Khoản
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="medium")
    
    with col1:
        if st.button(f"� {t('nav_logout')}", use_container_width=True, key="logout_button", type="primary"):
            st.logout()
    
    with col2:
        if st.button(f"❌ {t('deactivate')}", use_container_width=True, key="deactivate_button"):
            if user_id:
                user_model.deactivate(user_id)
                st.success(t('account_deactivated'))
                time.sleep(1)
                st.logout()
                st.rerun()
            else:
                st.error(t('error'))
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # User information section with beautiful cards
    st.markdown("""
        <style>
        .info-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1.5rem;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
            margin-bottom: 1.5rem;
            position: relative;
            overflow: hidden;
        }
        
        .info-card::before {
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        }
        
        .info-card-title {
            color: white;
            font-size: 1.5rem;
            font-weight: 700;
            margin: 0 0 1.5rem 0;
            position: relative;
            z-index: 1;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .info-item {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 1.2rem;
            margin-bottom: 1rem;
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: all 0.3s ease;
            position: relative;
            z-index: 1;
        }
        
        .info-item:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
            background: rgba(255, 255, 255, 0.25);
        }
        
        .info-label {
            color: rgba(255, 255, 255, 0.9);
            font-size: 0.85rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }
        
        .info-value {
            color: white;
            font-size: 1.1rem;
            font-weight: 600;
            word-break: break-all;
        }
        
        .stat-card {
            background: white;
            border-radius: 15px;
            padding: 1.5rem;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
            text-align: center;
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
            border-color: #667eea;
        }
        
        .stat-icon {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }
        
        .stat-label {
            color: #6b7280;
            font-size: 0.9rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
        
        .stat-value {
            color: #1f2937;
            font-size: 1.3rem;
            font-weight: 700;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Get user details
    from bson.objectid import ObjectId
    user_doc = user_model.collection.find_one({"_id": ObjectId(user_id)})
    
    if user_doc:
        # Beautiful info card with gradient
        email = user_doc.get('email', 'N/A')
        created_at = user_doc.get('created_at', 'N/A')
        if created_at != 'N/A':
            created_str = created_at.strftime("%d/%m/%Y %H:%M")
            days_active = (user_model.collection.database.client.admin.command('serverStatus')['localTime'] - created_at).days
        else:
            created_str = "N/A"
            days_active = 0
        
        # Display info using Streamlit components instead of complex HTML
        st.markdown("### 👤 Thông Tin Tài Khoản")
        
        # Create info box with simple styling
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 1.5rem; border-radius: 15px; margin-bottom: 1rem;'>
                <div style='color: white; margin-bottom: 1rem;'>
                    <strong>📧 Email:</strong><br/>
                    <span style='font-size: 0.95rem;'>{email}</span>
                </div>
                <div style='color: white; margin-bottom: 1rem;'>
                    <strong>🆔 User ID:</strong><br/>
                    <span style='font-size: 0.85rem; word-break: break-all;'>{str(user_id)}</span>
                </div>
                <div style='color: white;'>
                    <strong>📅 Ngày Tạo:</strong><br/>
                    <span style='font-size: 0.95rem;'>{created_str}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
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
        
        # Activity statistics with beautiful cards
        st.markdown("### 📊 Thống Kê Hoạt Động")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-icon">💰</div>
                    <div class="stat-label">Giao Dịch</div>
                    <div class="stat-value">{trans_count}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-icon">🔥</div>
                    <div class="stat-label">Ngân Sách</div>
                    <div class="stat-value">{budget_count}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-icon">📂</div>
                    <div class="stat-label">Danh Mục</div>
                    <div class="stat-value">{category_count}</div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Delete account permanently section with beautiful danger zone design
    st.markdown("""
        <style>
        .danger-zone {
            background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
            border: 2px solid #ef4444;
            border-radius: 20px;
            padding: 1.5rem;
            margin-top: 2rem;
            box-shadow: 0 4px 15px rgba(239, 68, 68, 0.2);
        }
        
        .danger-zone-title {
            color: #dc2626;
            font-size: 1.3rem;
            font-weight: 700;
            margin: 0 0 1rem 0;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .danger-warning {
            background: white;
            border-left: 4px solid #ef4444;
            border-radius: 10px;
            padding: 1rem;
            margin: 1rem 0;
            color: #991b1b;
            font-weight: 600;
        }
        
        .data-count {
            background: rgba(239, 68, 68, 0.1);
            border-radius: 10px;
            padding: 1rem;
            margin: 1rem 0;
        }
        
        .data-count-item {
            color: #7f1d1d;
            font-size: 1rem;
            margin: 0.5rem 0;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .data-count-number {
            font-weight: 700;
            color: #dc2626;
        }
        
        .confirm-input {
            margin: 1rem 0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    with st.expander(f"⚠️ {t('delete_account')}", expanded=False):
        st.markdown("""
            <div class="danger-zone">
                <div class="danger-zone-title">
                    <span>🚨</span>
                    <span>Khu Vực Nguy Hiểm</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if 'confirm_delete' not in st.session_state:
            st.session_state['confirm_delete'] = False
        
        if not st.session_state['confirm_delete']:
            st.markdown("""
                <div class="danger-warning">
                    ⚠️ Hành động này <strong>KHÔNG THỂ HOÀN TÁC</strong>. Tất cả dữ liệu của bạn sẽ bị xóa vĩnh viễn.
                </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"🗑️ {t('delete_account')}", key="show_delete_confirm", use_container_width=True, type="primary"):
                st.session_state['confirm_delete'] = True
                st.rerun()
        else:
            # Count user data using MongoDB count_documents (NO LOOP)
            from dataset.transaction_model import TransactionModel
            from dataset.budget_model import BudgetModel
            from dataset.category_model import CategoryModel
            from bson.objectid import ObjectId
            
            trans_model = TransactionModel()
            budget_model = BudgetModel()
            category_model = CategoryModel()
            
            user_oid = ObjectId(user_id)
            
            # Count using MongoDB count_documents
            trans_count = trans_model.collection.count_documents({"user_id": user_oid})
            budget_count = budget_model.collection.count_documents({"user_id": user_oid})
            category_count = category_model.collection.count_documents({"user_id": user_oid})
            total_items = trans_count + budget_count + category_count + 1
            
            # Display warning with beautiful design
            st.markdown("""
                <div class="danger-warning">
                    ⚠️ <strong>XÁC NHẬN XÓA TÀI KHOẢN</strong><br>
                    Dữ liệu sau sẽ bị xóa vĩnh viễn và không thể khôi phục:
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class="data-count">
                    <div class="data-count-item">
                        💰 <span class="data-count-number">{trans_count}</span> giao dịch
                    </div>
                    <div class="data-count-item">
                        🔥 <span class="data-count-number">{budget_count}</span> ngân sách
                    </div>
                    <div class="data-count-item">
                        📂 <span class="data-count-number">{category_count}</span> danh mục tùy chỉnh
                    </div>
                    <div class="data-count-item">
                        👤 <span class="data-count-number">1</span> tài khoản người dùng
                    </div>
                    <hr style="border-color: #ef4444; margin: 1rem 0;">
                    <div class="data-count-item" style="font-size: 1.1rem;">
                        📊 <strong>Tổng cộng: <span class="data-count-number">{total_items}</span> mục</strong>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<div class='confirm-input'>", unsafe_allow_html=True)
            st.markdown("**Gõ chính xác 'DELETE' để xác nhận:**")
            confirm_text = st.text_input(
                "Confirmation",
                key="delete_confirm_text",
                label_visibility="collapsed",
                placeholder="DELETE"
            )
            st.markdown("</div>", unsafe_allow_html=True)
            
            col_yes, col_no = st.columns(2)
            with col_yes:
                delete_enabled = confirm_text == "DELETE"
                if st.button(
                    f"✓ Xác Nhận Xóa",
                    key="confirm_delete_yes",
                    use_container_width=True,
                    type="primary",
                    disabled=not delete_enabled
                ):
                    result = user_model.delete_user_completely(user_id)
                    if result.get("success"):
                        st.success("✅ " + result.get("message"))
                        st.balloons()
                        time.sleep(2)
                        st.logout()
                        st.rerun()
                    else:
                        st.error("❌ " + result.get("error", "Unknown error"))
            
            with col_no:
                if st.button(f"❌ Hủy Bỏ", key="confirm_delete_no", use_container_width=True):
                    st.session_state['confirm_delete'] = False
                    st.rerun()
    
    st.markdown(f"<p style='text-align: center; color: #6b7280; font-size: 0.85rem; margin-top: 1rem;'>{t('app_subtitle')}</p>", unsafe_allow_html=True)