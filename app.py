import streamlit as st
import config
from language_manager import LanguageManager, t

# import model
from dataset import (
    CategoryModel,
    TransactionModel
)
from dataset.user_model import UserModel
from dataset.budget_model import BudgetModel

# import view module
from view import (
    render_categories,
    render_transactions,
    render_home,
    render_budgets
)
from view.user_view import render_user_profile
from view.dashboard_view import render_dashboard
from analytics.analyzer import FinanceAnalyzer

# Initialize language
LanguageManager.initialize()

# initialize models
@st.cache_resource
def init_models():
    """Initialize and cached models"""
    return {
        "category": CategoryModel(),
        "transaction": TransactionModel(),
        "user": UserModel(),
        "budget": BudgetModel()
    }

# initialize session per user
if "models" not in st.session_state:
    # initialize models
    st.session_state['models'] = init_models()


models = st.session_state['models']

# Page configuration
st.set_page_config(
    page_title = t("app_title"),
    page_icon = "💰",
    layout = "wide",
    initial_sidebar_state="collapsed"
)



# =============================================
# 1. Authen User
# =============================================

def login_screen():
    # Hide sidebar and apply styles
    st.markdown("""
        <style>
        [data-testid="stSidebar"] {display: none;}
        #MainMenu, footer, header {visibility: hidden;}
        
        /* Animated gradient background - Pastel colors */
        .stApp {
            background: linear-gradient(-45deg, #ffeaa7, #fab1a0, #fd79a8, #a29bfe, #74b9ff);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
        }
        
        @keyframes gradient {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Spacing for better centering
    st.write("")
    st.write("")
    st.write("")
    
    # Centered layout
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Login box with glassmorphism
        st.markdown("""
            <div style='background: rgba(255, 255, 255, 0.25); backdrop-filter: blur(20px);
                        padding: 3rem 2rem; border-radius: 30px; 
                        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
                        border: 1px solid rgba(255, 255, 255, 0.4);'>
        """, unsafe_allow_html=True)
        
        # Logo and Title
        st.markdown(f"""
            <div style='text-align: center; margin-bottom: 2rem;'>
                <div style='font-size: 5rem; margin-bottom: 1rem;'>💰</div>
                <h1 style='color: #2d3436; font-size: 3rem; font-weight: 900; margin: 0;
                           text-shadow: 0 2px 4px rgba(255,255,255,0.5);'>
                    {t('app_name')}
                </h1>
                <p style='color: #636e72; font-size: 1.2rem; margin: 0.5rem 0; font-weight: 500;'>
                    ✨ {t('app_subtitle')} ✨
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Info box
        st.markdown("""
            <div style='background: rgba(255, 255, 255, 0.4); padding: 1rem;
                        border-radius: 15px; text-align: center; margin: 2rem 0;
                        border: 1px solid rgba(255, 255, 255, 0.6);'>
                <p style='color: #2d3436; font-weight: 600; margin: 0;'>
                    🔐 Ứng Dụng Riêng Tư - Đăng nhập để bắt đầu
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        
        # Features in 2 columns
        col_f1, col_f2 = st.columns(2)
        
        with col_f1:
            st.markdown("""
                <div style='background: rgba(255,255,255,0.35); padding: 1.5rem;
                            border-radius: 20px; margin-bottom: 1rem;
                            border: 1px solid rgba(255,255,255,0.5);
                            transition: transform 0.3s;'>
                    <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>📊</div>
                    <div style='color: #2d3436; font-weight: 700; font-size: 1.1rem;'>
                        Theo Dõi Chi Tiêu
                    </div>
                    <div style='color: #636e72; font-size: 0.9rem;'>
                        Ghi lại mọi giao dịch
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
                <div style='background: rgba(255,255,255,0.35); padding: 1.5rem;
                            border-radius: 20px; margin-bottom: 1rem;
                            border: 1px solid rgba(255,255,255,0.5);'>
                    <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>📈</div>
                    <div style='color: #2d3436; font-weight: 700; font-size: 1.1rem;'>
                        Phân Tích Thông Minh
                    </div>
                    <div style='color: #636e72; font-size: 0.9rem;'>
                        Biểu đồ chi tiết
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        with col_f2:
            st.markdown("""
                <div style='background: rgba(255,255,255,0.35); padding: 1.5rem;
                            border-radius: 20px; margin-bottom: 1rem;
                            border: 1px solid rgba(255,255,255,0.5);'>
                    <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>💵</div>
                    <div style='color: #2d3436; font-weight: 700; font-size: 1.1rem;'>
                        Quản Lý Ngân Sách
                    </div>
                    <div style='color: #636e72; font-size: 0.9rem;'>
                        Kiểm soát chi tiêu
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
                <div style='background: rgba(255,255,255,0.35); padding: 1.5rem;
                            border-radius: 20px; margin-bottom: 1rem;
                            border: 1px solid rgba(255,255,255,0.5);'>
                    <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>🔒</div>
                    <div style='color: #2d3436; font-weight: 700; font-size: 1.1rem;'>
                        Bảo Mật Cao
                    </div>
                    <div style='color: #636e72; font-size: 0.9rem;'>
                        Dữ liệu an toàn
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        st.write("")
        st.write("")
        
        # Login button with custom styling - Soft colors
        st.markdown("""
            <style>
            .stButton > button {
                width: 100% !important;
                background: linear-gradient(135deg, #74b9ff 0%, #a29bfe 100%) !important;
                color: white !important;
                border: none !important;
                padding: 1rem 2rem !important;
                font-size: 1.2rem !important;
                font-weight: 700 !important;
                border-radius: 20px !important;
                box-shadow: 0 8px 20px rgba(116, 185, 255, 0.3) !important;
                transition: all 0.3s ease !important;
                text-transform: uppercase !important;
                letter-spacing: 1px !important;
            }
            .stButton > button:hover {
                transform: translateY(-3px) !important;
                box-shadow: 0 12px 30px rgba(116, 185, 255, 0.5) !important;
            }
            </style>
        """, unsafe_allow_html=True)
        
        if st.button(f"🚀 {t('login_button')}", key="login_btn"):
            st.login()
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Footer
        st.write("")
        st.markdown("""
            <div style='text-align: center; color: #636e72; margin-top: 2rem;'>
                <p style='margin: 0.5rem 0;'>Bằng việc đăng nhập, bạn đồng ý với điều khoản sử dụng</p>
                <p style='margin: 0; font-weight: 700;'>© 2025 Finance Tracker. All Rights Reserved.</p>
            </div>
        """, unsafe_allow_html=True)


if not st.user.is_logged_in:
    login_screen()
else:
    # Get mongo_user
    user_model: UserModel = models['user']
    try:
        mongo_user_id = user_model.login(st.user.email)
    except Exception as e:
        st.error(f"Error during user login: {e}")
        st.stop()

    # set user_id for models
    # currently we have category and transaction models
    # you can optimize this by doing it in the model init function
    models['category'].set_user_id(mongo_user_id)
    models['budget'].set_user_id(mongo_user_id)
    models['transaction'].set_user_id(mongo_user_id)


    user = st.user.to_dict() # convert google_user to dict
    user.update({
        "id": mongo_user_id
    })

    # Display user profile after update user with mongo_user_id
    render_user_profile(user_model, user)

    # init analyzer
    # because transaction_model has set user_id already in line 74
    analyzer_model = FinanceAnalyzer(models['transaction'])

    # =============================================
    # 2. Navigation
    # =============================================
    
    # Create navigation options based on current language
    nav_options = [
        t("nav_home"),
        t("nav_categories"),
        t("nav_transactions"),
        t("nav_budgets")
    ]
    
    page = st.sidebar.radio(
        "Navigation",
        nav_options,
        label_visibility="collapsed"
    )
    
    # Map display names to internal names
    page_map = {
        t("nav_home"): "Home",
        t("nav_categories"): "Category",
        t("nav_transactions"): "Transaction",
        t("nav_budgets"): "Budget"
    }
    page = page_map.get(page, "Home")
    
    # Add language selector in sidebar
    LanguageManager.render_language_selector()
    
    # Add sample data button
    st.sidebar.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    if st.sidebar.button(f"🎲 {t('add_sample_data')}", width='stretch', key="add_sample_data_btn"):
        with st.spinner(t('loading')):
            from add_sample_data import add_sample_data
            add_sample_data(mongo_user_id)
            st.sidebar.success(f"✅ {t('success')}!")
            st.rerun()

    st.markdown("""
        <style>
        /* Page layout */
        .block-container {
            padding-top: 1rem !important;
        }
        </style>
    """, unsafe_allow_html=True)

    if st.session_state.get('user_settings_open', False):
        email = user.get("email") or ""
        
        st.markdown("""
            <style>
            .settings-panel {
                background: white;
                padding: 2rem;
                border-radius: 20px;
                margin-bottom: 2rem;
                box-shadow: 0 10px 40px rgba(0,0,0,0.1);
                border: 2px solid #e5e7eb;
            }
            
            .settings-header {
                display: flex;
                align-items: center;
                gap: 1rem;
                margin-bottom: 1.5rem;
                padding-bottom: 1rem;
                border-bottom: 2px solid #e5e7eb;
            }
            
            .settings-avatar {
                width: 70px;
                height: 70px;
                border-radius: 50%;
                border: 4px solid #667eea;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
            }
            
            .settings-user-info h3 {
                margin: 0;
                color: #1f2937;
                font-size: 1.3rem;
                font-weight: 700;
            }
            
            .settings-user-info p {
                margin: 0.3rem 0 0 0;
                color: #6b7280;
                font-size: 0.9rem;
            }
            
            .settings-actions {
                display: grid;
                gap: 0.8rem;
            }
            </style>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='settings-panel'>", unsafe_allow_html=True)
        
        # User info header
        avatar_url = user.get("picture")
        name = user.get("given_name") or user.get("name") or "User"
        
        if avatar_url:
            st.markdown(f"""
                <div class='settings-header'>
                    <img src='{avatar_url}' class='settings-avatar'/>
                    <div class='settings-user-info'>
                        <h3>{name}</h3>
                        <p>✉️ {email}</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class='settings-header'>
                    <div style='width: 70px; height: 70px; border-radius: 50%; 
                         background: linear-gradient(135deg, #667eea, #764ba2);
                         display: flex; align-items: center; justify-content: center;
                         font-size: 2rem; border: 4px solid #667eea;
                         box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);'>
                        👤
                    </div>
                    <div class='settings-user-info'>
                        <h3>{name}</h3>
                        <p>✉️ {email}</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        # Action buttons
        st.markdown(f"<div class='settings-actions'><h4 style='color: #667eea; margin: 0 0 0.5rem 0;'>⚙️ {t('settings')}</h4></div>", unsafe_allow_html=True)
        
        action_cols = st.columns([1, 1, 1])
        
        with action_cols[0]:
            if st.button(f"🚪 {t('nav_logout')}", key="logout_settings", use_container_width=True, type="primary"):
                st.logout()
        
        with action_cols[1]:
            if st.button(f"❌ {t('deactivate')}", key="deactivate_header", use_container_width=True):
                user_model.deactivate(user.get('id'))
                st.success(t('account_deactivated'))
                st.logout()
        
        with action_cols[2]:
            if st.button(f"🗑️ {t('delete_account')}", key="delete_account_header", use_container_width=True):
                st.session_state['confirm_delete'] = True
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button(f"✖️ {t('close')}", key="close_settings", use_container_width=True, type="secondary"):
            st.session_state['user_settings_open'] = False
            st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
    


    # =============================================
    # 3. Router
    # =============================================
    
    if page == "Home":
        render_home(transaction_model=models['transaction'], 
                   category_model=models['category'])

    elif page == "Category":
        # get category_model from models
        category_model = models['category']

        # display category views
        render_categories(category_model=category_model)

    elif page == "Transaction":
        # get category_model and transaction from models
        category_model = models['category']
        transaction_model = models['transaction']

        # display transaction views
        render_transactions(transaction_model=transaction_model, category_model=category_model)

    elif page == "Budget":
        # get budget_model, transaction_model and category_model
        budget_model = models['budget']
        transaction_model = models['transaction']
        category_model = models['category']

        # display budget views
        render_budgets(budget_model=budget_model, 
                      transaction_model=transaction_model,
                      category_model=category_model)