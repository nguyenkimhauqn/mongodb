import streamlit as st
import config
from datetime import date
import time
from language_manager import t

def _render_add_transaction(transaction_model, category_model):
    st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1.5rem; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <h3 style='color: white; margin: 0;'>{t('add_transaction')}</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.container():
        # Move transaction_type outside the form so it can trigger re-renders
        col_type, col_spacer = st.columns([2, 3])
        
        with col_type:
            # Create translated options for transaction types
            transaction_type_options = [t(tt) for tt in config.TRANSACTION_TYPES]
            selected_type_index = st.selectbox(
                t('transaction_type'),
                range(len(config.TRANSACTION_TYPES)),
                format_func=lambda x: transaction_type_options[x],
                key="transaction_type_selector",
                help=t('transaction_type')
            )
            transaction_type = config.TRANSACTION_TYPES[selected_type_index]
        
        # Get categories based on selected transaction type
        categories = category_model.get_categories_by_type(transaction_type)
        category_names = [item['name'] for item in categories]
        # Translate category names for display
        translated_category_names = [t(name, name) for name in category_names]

        # Check if categories exist before showing the form
        if not category_names:
            st.markdown(f"""
                <div style='background: #fef3c7; padding: 1.5rem; border-radius: 10px; 
                            border-left: 4px solid #f59e0b;'>
                    <h4 style='color: #92400e; margin: 0 0 0.5rem 0;'>⚠️ {t('warning')}</h4>
                    <p style='color: #78350f; margin: 0;'>
                        {t('select_category')} <strong>{transaction_type}</strong>
                    </p>
                </div>
            """, unsafe_allow_html=True)
            return 
        
        # Create form with remaining fields
        with st.form("add_new_transaction", clear_on_submit=True):
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Use index to map translated display name back to original
                category_index = st.selectbox(
                    t('category'),
                    range(len(category_names)),
                    format_func=lambda x: translated_category_names[x],
                    help=t('select_category')
                )
                category = category_names[category_index]
                
                amount = st.number_input(
                    t('amount'),  
                    min_value=0.01,
                    step=0.01,
                    help=t('amount')
                )

            with col2:
                transaction_date = st.date_input(
                    t('date'),
                    date.today(),
                    help=t('date')
                )
                
                description = st.text_input(
                    t('description'),
                    "",
                    placeholder=t('enter_description'),
                    help=t('description')
                )

            col_submit, col_spacer = st.columns([1, 4])
            
            with col_submit:
                submitted = st.form_submit_button(f"💾 {t('save')}", width='stretch', type="primary")

            if submitted:
                if amount <= 0:
                    st.error(f"❌ {t('amount')} > 0")
                else:
                    try:
                        result = transaction_model.add_transaction(
                            transaction_type=transaction_type,
                            category=category,
                            amount=amount,
                            transaction_date=transaction_date,
                            description=description
                        )
                        if result:
                            st.success(f"✅ {t('transaction_added')}")
                            st.balloons()
                            time.sleep(1.5)
                            st.rerun()
                        else:
                            st.error(f"❌ {t('error')}")
                    except ValueError as e:
                        # ✅ Handle validation errors (category doesn't exist or type mismatch)
                        st.error(f"❌ {str(e)}")
                    except Exception as e:
                        st.error(f"❌ {t('error')}: {str(e)}")


def _render_transaction_list(transaction_model):
    st.markdown(f"""
        <div style='background: white; padding: 1.5rem; border-radius: 15px; 
                    box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom: 1rem;'>
            <h3 style='color: #1f2937; margin: 0;'>{t('transactions_title')}</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Filter options
    col_filter1, col_filter2, col_filter3 = st.columns(3)
    
    with col_filter1:
        # Create filter options with translations
        filter_options = [t('all'), t('income'), t('expense')]
        filter_values = ['all', 'Income', 'Expense']
        
        filter_index = st.selectbox(
            t('filter'),
            range(len(filter_options)),
            format_func=lambda x: filter_options[x],
            key="filter_type"
        )
        filter_type = filter_values[filter_index]
    
    # Get transactions based on filter
    if filter_type == 'all':
        transactions = transaction_model.get_all_transactions()
    else:
        transactions = transaction_model.get_transactions_by_type(filter_type)
    
    if not transactions:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #e0f2fe 0%, #dbeafe 100%); 
                        padding: 2rem; border-radius: 15px; text-align: center;'>
                <h3 style='color: #0369a1; margin-bottom: 0.5rem;'>📝 {t('no_transactions')}</h3>
                <p style='color: #0c4a6e; margin: 0;'>{t('no_transactions')}</p>
            </div>
        """, unsafe_allow_html=True)
        return
    
    st.markdown(f"**{t('total')}:** {len(transactions)} {t('transactions_label')}")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Display transactions in a nice format
    for trans in transactions:
        trans_type = trans.get('type', 'Unknown')
        category = trans.get('category', 'N/A')
        # Translate category name
        translated_category = t(category, category)
        amount = trans.get('amount', 0)
        desc = trans.get('description', '')
        trans_date = trans.get('transaction_date')
        trans_id = str(trans.get('_id', ''))
        
        # Format date
        if trans_date:
            if hasattr(trans_date, 'strftime'):
                date_str = trans_date.strftime('%d %b %Y')
            else:
                date_str = str(trans_date)
        else:
            date_str = 'N/A'
        
        # Color and icon based on type
        if trans_type == 'Income':
            color = "#28a745"
            icon = "💰"
            badge_color = "#d4edda"
        else:
            color = "#dc3545"
            icon = "💸"
            badge_color = "#f8d7da"
        
        with st.container():
            st.markdown(f"""
                <div style='background: white; padding: 1.2rem; border-radius: 12px; 
                            margin-bottom: 1rem; box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                            border-left: 5px solid {color};'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <div style='flex: 0.5; font-size: 2rem;'>{icon}</div>
                        <div style='flex: 3;'>
                            <div style='font-size: 1.2rem; font-weight: 600; color: #1f2937;'>{translated_category}</div>
                            <div style='color: #6b7280; font-size: 0.9rem; margin-top: 0.3rem;'>
                                {desc if desc else t('no_transactions')}
                            </div>
                            <div style='color: #9ca3af; font-size: 0.85rem; margin-top: 0.5rem;'>
                                📅 {date_str} | <span style='background: {badge_color}; padding: 2px 8px; border-radius: 4px;'>{trans_type}</span>
                            </div>
                        </div>
                        <div style='flex: 1.5; text-align: right;'>
                            <div style='font-size: 1.5rem; font-weight: 700; color: {color};'>${amount:,.2f}</div>
                        </div>
                        <div style='flex: 0.5; text-align: center;'>
            """, unsafe_allow_html=True)
            
            if st.button("🗑️", key=f"del_{trans_id}", help=t('delete')):
                result = transaction_model.delete_transaction(trans_id)
                if result:
                    st.success(f"✅ {t('transaction_deleted')}")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error(f"❌ {t('error')}")
            
            st.markdown("""
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)


def render_transactions(transaction_model, category_model):
    # Modern header
    st.markdown("""
        <style>
        .transaction-header {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .transaction-header h1 {
            color: white;
            margin: 0;
            font-size: 2.5rem;
            font-weight: 700;
        }
        .transaction-header p {
            color: rgba(255,255,255,0.9);
            margin: 0.5rem 0 0 0;
            font-size: 1.1rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="transaction-header">
            <h1>{t('transactions_title')}</h1>
            <p>{t('app_subtitle')}</p>
        </div>
    """, unsafe_allow_html=True)

    # Add transaction form
    _render_add_transaction(transaction_model, category_model)
    
    st.markdown("---")
    
    # Display transaction list
    _render_transaction_list(transaction_model)