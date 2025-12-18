import streamlit as st
import config
from language_manager import t

# function to render category list
def _render_category_list(category_model, category_type: str):
    icon = "💸" if category_type == "Expense" else "💵"
    color = "#dc2626" if category_type == "Expense" else "#16a34a"
    bg_color = "#fef2f2" if category_type == "Expense" else "#f0fdf4"
    
    category_label = t('income_categories') if category_type == 'Income' else t('expense_categories')
    st.markdown(f"""
        <div style='background: {bg_color}; padding: 1.5rem; border-radius: 15px; 
                    margin-bottom: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.08);'>
            <h3 style='color: {color}; margin: 0;'>{icon} {category_label}</h3>
        </div>
    """, unsafe_allow_html=True)
    
    expense_lst = category_model.get_categories_by_type(category_type = category_type)

    if expense_lst:
        st.write(f"**{t('total')}:** {len(expense_lst)} {t('categories_title').lower()}")
        st.markdown("<br>", unsafe_allow_html=True)

        cols = st.columns(3, gap="medium")

        for idx, item in enumerate(expense_lst):
            col_idx = idx % 3 # remaining fraction

            with cols[col_idx]:
                category_name = item.get('name')
                # Translate category name
                translated_name = t(category_name, category_name)
                created_date = item.get('created_at').strftime('%d/%m/%Y')
                
                st.markdown(f"""
                    <div style='background: white; padding: 1.2rem; border-radius: 12px; 
                                box-shadow: 0 2px 8px rgba(0,0,0,0.08); 
                                border-left: 4px solid {color}; margin-bottom: 1rem;'>
                        <div style='font-size: 1.1rem; font-weight: 600; color: #1f2937; margin-bottom: 0.5rem;'>
                            📌 {translated_name}
                        </div>
                        <div style='color: #6b7280; font-size: 0.85rem;'>
                            📅 {created_date}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Edit and Delete buttons
                col_edit, col_del = st.columns(2)
                with col_edit:
                    if st.button(f"✏️ {t('edit_category')}", key=f"edit_{item['_id']}", use_container_width=True):
                        st.session_state[f'editing_{item["_id"]}'] = True
                
                with col_del:
                    if st.button(f"❌ {t('delete')}", key=f"del_{item['_id']}", use_container_width=True):
                        st.session_state[f'deleting_{item["_id"]}'] = True
                
                # Show edit form if editing
                if st.session_state.get(f'editing_{item["_id"]}', False):
                    with st.form(key=f"edit_form_{item['_id']}"):
                        st.markdown(f"**{t('rename_category')}**")
                        new_name = st.text_input(
                            t('new_name'),
                            value=category_name,
                            key=f"new_name_{item['_id']}"
                        )
                        
                        col_save, col_cancel = st.columns(2)
                        with col_save:
                            save_btn = st.form_submit_button(f"💾 {t('save')}", use_container_width=True, type="primary")
                        with col_cancel:
                            cancel_btn = st.form_submit_button(f"❌ {t('cancel')}", use_container_width=True)
                        
                        if save_btn and new_name:
                            success, message = category_model.update_category(
                                old_name=category_name,
                                new_name=new_name,
                                category_type=category_type
                            )
                            if success:
                                st.success(f"✅ {t('category_updated')}")
                                del st.session_state[f'editing_{item["_id"]}']
                                st.rerun()
                            else:
                                st.error(f"❌ {message}")
                        
                        if cancel_btn:
                            del st.session_state[f'editing_{item["_id"]}']
                            st.rerun()
                
                # Show delete confirmation if deleting
                if st.session_state.get(f'deleting_{item["_id"]}', False):
                    # Count related data
                    from dataset.transaction_model import TransactionModel
                    from dataset.budget_model import BudgetModel
                    trans_model = TransactionModel()
                    budget_model = BudgetModel()
                    
                    trans_count = len(trans_model.get_transactions_by_category(category_name))
                    budget_count = len(budget_model.get_budgets_by_category(category_name))
                    
                    st.warning(f"⚠️ {t('related_data_found')}:")
                    st.info(f"- {trans_count} {t('category_has_transactions')}\n- {budget_count} {t('category_has_budgets')}")
                    
                    with st.form(key=f"delete_form_{item['_id']}"):
                        st.markdown(f"**{t('delete_category_options')}**")
                        
                        action = st.radio(
                            t('select'),
                            options=['move_to_others', 'delete_all', 'cancel'],
                            format_func=lambda x: t(x),
                            key=f"action_{item['_id']}"
                        )
                        
                        col_confirm, col_cancel = st.columns(2)
                        with col_confirm:
                            confirm_btn = st.form_submit_button(f"✓ {t('confirm')}", use_container_width=True, type="primary")
                        with col_cancel:
                            cancel_btn = st.form_submit_button(f"❌ {t('cancel')}", use_container_width=True)
                        
                        if confirm_btn:
                            if action == 'cancel':
                                del st.session_state[f'deleting_{item["_id"]}']
                                st.rerun()
                            else:
                                success, message, counts = category_model.delete_category_with_handling(
                                    category_type=category_type,
                                    category_name=category_name,
                                    action=action
                                )
                                
                                if success:
                                    st.success(f"✅ {message}")
                                    if counts:
                                        st.info(f"📊 {t('deletion_summary')}:\n" + 
                                               f"- {counts.get('transactions_moved', 0)} {t('transactions_moved')}\n" +
                                               f"- {counts.get('transactions_deleted', 0)} {t('transactions_deleted')}\n" +
                                               f"- {counts.get('budgets_deleted', 0)} {t('budgets_deleted')}")
                                    del st.session_state[f'deleting_{item["_id"]}']
                                    st.rerun()
                                else:
                                    st.error(f"❌ {message}")
                        
                        if cancel_btn:
                            del st.session_state[f'deleting_{item["_id"]}']
                            st.rerun()

def _render_category_detail(category_model):
    st.markdown(f"""
        <div style='background: white; padding: 1.5rem; border-radius: 15px; 
                    box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom: 2rem;'>
            <h3 style='color: #1f2937; margin: 0;'>{t('categories_title')}</h3>
        </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs([f"💸 {t('expense')}", f"💰 {t('income')}"])

    with tab1:
        _render_category_list(category_model, "Expense")

    with tab2:
        _render_category_list(category_model, "Income")

#TODO
def _render_add_category(category_model):
    st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1.5rem; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <h3 style='color: white; margin: 0;'>{t('add_category')}</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.form("add_category_name", clear_on_submit=True):
        col1, col2, col3 = st.columns([2, 2, 1]) # col1 and col2 is double size of col1

    # category type
    with col1:
        # Translate transaction types
        type_options = [t(tt) for tt in config.TRANSACTION_TYPES]
        type_index = st.selectbox(
            t('category_type'),
            range(len(config.TRANSACTION_TYPES)),
            format_func=lambda x: type_options[x],
            help=t('select_category')
        )
        category_type = config.TRANSACTION_TYPES[type_index]
    
    # category input
    with col2:
        category_name = st.text_input(
            t('category_name'),
            placeholder=t('enter_category_name'),
            help=t('category_name')
        )
    
    with col3:
        st.write("")  # Spacing
        st.write("")
        submitted = st.form_submit_button(f"➞ {t('add_category')}", width='stretch', type="primary")
    
    if submitted:
        if not category_name:
            st.error(f"❌ {t('enter_category_name')}")
        elif not category_type:
            st.error(f"❌ {t('select_category')}")          
        else:
            result = category_model.upsert_category(category_type = category_type, category_name = category_name)
            if result:
                st.success(f"✅ {t('category_added')}")
                st.balloons()
                st.rerun()  # Refresh the page to show new category
            else:
                st.error(f"❌ {t('error')}")


# public function
def render_categories(category_model):
    # Modern header
    st.markdown("""
        <style>
        .category-header {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .category-header h1 {
            color: white;
            margin: 0;
            font-size: 2.5rem;
            font-weight: 700;
        }
        .category-header p {
            color: rgba(255,255,255,0.9);
            margin: 0.5rem 0 0 0;
            font-size: 1.1rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="category-header">
            <h1>{t('categories_title')}</h1>
            <p>{t('app_subtitle')}</p>
        </div>
    """, unsafe_allow_html=True)

    # Display existing category list
    _render_category_detail(category_model)

    st.divider()

    # Add category section
    _render_add_category(category_model)