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
        if st.button(f"🚺 {t('nav_logout')}", width='stretch', key="logout_button", type="primary"):
            st.logout()
    
    with col2:
        if st.button(f"❌ {t('deactivate')}", width='stretch', key="deactivate_button"):
            if user_id:
                user_model.deactivate(user_id)
                st.success(t('account_deactivated'))
                time.sleep(1)
                st.logout()
                st.rerun()
            else:
                st.error(t('error'))
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Delete account permanently section
    with st.expander(f"⚠️ {t('delete_account')}", expanded=False):
        st.warning(f"**{t('delete_account_warning')}**")
        
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
            
            trans_model = TransactionModel()
            budget_model = BudgetModel()
            category_model = CategoryModel()
            
            trans_count = len(trans_model.get_transactions_by_user_id(user_id))
            budget_count = len(budget_model.get_budgets_by_user_id(user_id))
            category_count = len(category_model.get_categories_by_user_id(user_id))
            
            st.error(f"**{t('delete_account_info')}:**")
            st.info(f"- {trans_count} {t('category_has_transactions')}\n" +
                   f"- {budget_count} {t('category_has_budgets')}\n" +
                   f"- {category_count} {t('categories_title').lower()}")
            
            st.markdown(f"**{t('delete_account_confirm')}**")
            
            col_yes, col_no = st.columns(2)
            with col_yes:
                if st.button(f"✓ {t('yes')}", key="confirm_delete_yes", use_container_width=True, type="primary"):
                    success, counts = user_model.delete_user_completely(user_id)
                    if success:
                        st.success(t('account_deleted'))
                        st.balloons()
                        time.sleep(2)
                        st.logout()
                        st.rerun()
                    else:
                        st.error(t('error'))
            
            with col_no:
                if st.button(f"❌ {t('no')}", key="confirm_delete_no", use_container_width=True):
                    st.session_state['confirm_delete'] = False
                    st.rerun()
    
    st.markdown(f"<p style='text-align: center; color: #6b7280; font-size: 0.85rem; margin-top: 1rem;'>{t('app_subtitle')}</p>", unsafe_allow_html=True)