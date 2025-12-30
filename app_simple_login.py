"""
Simple Login Version - Without Google OAuth
Use this if you don't want to configure Google OAuth
"""
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
from view.user_view_simple import render_user_profile
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
# 1. Simple Email Login
# =============================================

def simple_login_screen():
    """Simple login screen with email input only"""
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
        
        st.write("")
        
        # Email input form
        with st.form("login_form"):
            st.markdown("""
                <h3 style='text-align: center; color: #2d3436; margin-bottom: 1rem;'>
                    📧 Đăng Nhập Với Email
                </h3>
            """, unsafe_allow_html=True)
            
            email = st.text_input(
                "Email",
                placeholder="your.email@example.com",
                help="Nhập email của bạn để đăng nhập"
            )
            
            submitted = st.form_submit_button(
                "🚀 Đăng Nhập",
                use_container_width=True
            )
            
            if submitted:
                if email and "@" in email:
                    # Save email to session state
                    st.session_state['user_email'] = email
                    st.session_state['is_logged_in'] = True
                    st.rerun()
                else:
                    st.error("❌ Vui lòng nhập email hợp lệ")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Info
        st.markdown("""
            <div style='text-align: center; color: #636e72; margin-top: 2rem;'>
                <p style='margin: 0.5rem 0;'>💡 Chỉ cần nhập email, không cần mật khẩu</p>
                <p style='margin: 0; font-weight: 700;'>© 2025 Finance Tracker. All Rights Reserved.</p>
            </div>
        """, unsafe_allow_html=True)


# Check login status
if 'is_logged_in' not in st.session_state or not st.session_state.get('is_logged_in'):
    simple_login_screen()
else:
    # Get email from session
    email = st.session_state.get('user_email')
    
    if not email:
        st.error("❌ Email not found. Please login again.")
        st.session_state['is_logged_in'] = False
        st.rerun()
    
    # Login to MongoDB
    user_model: UserModel = models['user']
    try:
        mongo_user_id = user_model.login(email)
    except Exception as e:
        st.error(f"Error during user login: {e}")
        st.stop()

    # set user_id for models
    models['category'].set_user_id(mongo_user_id)
    models['budget'].set_user_id(mongo_user_id)
    models['transaction'].set_user_id(mongo_user_id)

    # Create user dict for display
    user = {
        "id": mongo_user_id,
        "email": email,
        "name": email.split("@")[0].title(),
        "given_name": email.split("@")[0].title(),
    }

    # Display user profile
    render_user_profile(user_model, user)

    # init analyzer
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
    
    if st.sidebar.button(f"🎲 {t('add_sample_data')}", key="add_sample_data_btn", use_container_width=True):
        with st.spinner(t('loading')):
            from add_sample_data import add_sample_data
            add_sample_data(mongo_user_id)
            st.sidebar.success(f"✅ {t('success')}!")
            st.rerun()
    
    # Logout button
    st.sidebar.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    if st.sidebar.button("🚪 Đăng Xuất", key="logout_btn", use_container_width=True, type="secondary"):
        st.session_state['is_logged_in'] = False
        st.session_state['user_email'] = None
        st.rerun()

    st.markdown("""
        <style>
        /* Page layout */
        .block-container {
            padding-top: 1rem !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # =============================================
    # 3. Router
    # =============================================
    
    if page == "Home":
        render_home(transaction_model=models['transaction'], 
                   category_model=models['category'])

    elif page == "Category":
        category_model = models['category']
        render_categories(category_model=category_model)

    elif page == "Transaction":
        category_model = models['category']
        transaction_model = models['transaction']
        render_transactions(transaction_model=transaction_model, category_model=category_model)

    elif page == "Budget":
        budget_model = models['budget']
        transaction_model = models['transaction']
        category_model = models['category']
        render_budgets(budget_model=budget_model, 
                      transaction_model=transaction_model,
                      category_model=category_model)

