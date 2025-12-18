"""Language manager for handling translations"""

import streamlit as st
from locales import LANGUAGES

class LanguageManager:
    """Manages language selection and translations"""
    
    @staticmethod
    def initialize():
        """Initialize language in session state"""
        if "language" not in st.session_state:
            st.session_state.language = "vi"  # Default language
    
    @staticmethod
    def get_current_language():
        """Get current selected language"""
        LanguageManager.initialize()
        return st.session_state.language
    
    @staticmethod
    def set_language(lang_code):
        """Set current language"""
        if lang_code in LANGUAGES:
            st.session_state.language = lang_code
    
    @staticmethod
    def get(key, default=None):
        """Get translation for a key"""
        LanguageManager.initialize()
        lang = st.session_state.language
        translations = LANGUAGES.get(lang, {}).get("translations", {})
        return translations.get(key, default or key)
    
    @staticmethod
    def render_language_selector():
        """Render language selector in sidebar"""
        LanguageManager.initialize()
        
        st.sidebar.markdown("---")
        
        current_lang = st.session_state.language
        current_lang_info = LANGUAGES[current_lang]
        
        # Display current language with styling
        st.sidebar.markdown(f"""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        padding: 1rem;
                        border-radius: 15px;
                        margin-bottom: 1rem;
                        text-align: center;
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                <div style='color: rgba(255,255,255,0.9); font-size: 0.85rem; font-weight: 600; margin-bottom: 0.3rem;'>
                    {LanguageManager.get('language')}
                </div>
                <div style='color: white; font-size: 1.3rem; font-weight: 700;'>
                    {current_lang_info['flag']} {current_lang_info['name']}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Create language buttons with consistent styling
        st.sidebar.markdown("""
            <style>
            /* Language button styling */
            div[data-testid="column"] div.stButton > button {
                height: 50px !important;
                font-size: 0.95rem !important;
                font-weight: 600 !important;
                border-radius: 12px !important;
                padding: 0.5rem !important;
                border: 2px solid #e5e7eb !important;
                background: white !important;
                color: #4b5563 !important;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
                transition: all 0.2s ease !important;
            }
            div[data-testid="column"] div.stButton > button:hover {
                border-color: #667eea !important;
                box-shadow: 0 4px 8px rgba(102, 126, 234, 0.2) !important;
                transform: translateY(-1px) !important;
            }
            .lang-active {
                background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%) !important;
                padding: 0.75rem !important;
                border-radius: 12px !important;
                text-align: center !important;
                font-weight: 700 !important;
                color: #2d3436 !important;
                box-shadow: 0 4px 8px rgba(132, 250, 176, 0.3) !important;
                border: 3px solid #00b894 !important;
                height: 50px !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                font-size: 0.95rem !important;
            }
            </style>
        """, unsafe_allow_html=True)
        
        cols = st.sidebar.columns(2, gap="small")
        for idx, (lang_code, lang_info) in enumerate(LANGUAGES.items()):
            with cols[idx % 2]:
                if lang_code == current_lang:
                    # Active button with consistent height
                    st.markdown(f"""
                        <div class='lang-active'>
                            ✓ {lang_info['flag']} {lang_info['name']}
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    # Inactive button
                    if st.button(
                        f"{lang_info['flag']} {lang_info['name']}", 
                        key=f"lang_{lang_code}",
                        use_container_width=True
                    ):
                        LanguageManager.set_language(lang_code)
                        st.rerun()

# Convenience function for quick access
def t(key, default=None):
    """Shorthand for getting translation"""
    return LanguageManager.get(key, default)
