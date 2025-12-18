import streamlit as st
from dataset.budget_model import BudgetModel
from dataset.transaction_model import TransactionModel
from dataset.category_model import CategoryModel
from analytics.visualizer import FinanceVisualizer
from language_manager import t


def _get_status_color(status: str) -> tuple:
    """Get color scheme based on budget status"""
    colors = {
        'safe': ('#dcfce7', '#16a34a', '✅'),
        'warning': ('#fef3c7', '#f59e0b', '⚠️'),
        'danger': ('#fee2e2', '#dc2626', '🚨'),
        'exceeded': ('#fecaca', '#991b1b', '❌'),
        'no_budget': ('#f3f4f6', '#6b7280', '📊')
    }
    return colors.get(status, colors['no_budget'])


def _render_add_budget(budget_model: BudgetModel, category_model: CategoryModel):
    """Render form to add new budget"""
    st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1.5rem; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <h3 style='color: white; margin: 0;'>{t('add_budget')}</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Info about constraint
    st.info("💡 **Mẹo:** Nếu danh mục này đã có ngân sách trong tháng, số tiền mới sẽ thay thế số tiền cũ.", icon="💡")
    
    st.markdown("<br>", unsafe_allow_html=True)

    # Get expense categories
    expense_categories = category_model.get_categories_by_type("Expense")
    category_names = [cat['name'] for cat in expense_categories]

    if not category_names:
        st.warning("⚠️ Vui lòng tạo danh mục chi tiêu trước khi thiết lập ngân sách!")
        return

    with st.form("add_budget_form", clear_on_submit=True):
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            # Translate category names
            translated_names = [t(name, name) for name in category_names]
            category_index = st.selectbox(
                t('category'),
                range(len(category_names)),
                format_func=lambda x: translated_names[x],
                help=t('select_category')
            )
            category = category_names[category_index]

        with col2:
            amount = st.number_input(
                t('budget_amount'),
                min_value=0.01,
                step=100.0,
                value=500.0,
                help=t('budget_amount')
            )

        with col3:
            from datetime import datetime
            current_month = datetime.now().month
            month = st.selectbox(
                "Tháng",
                list(range(1, 13)),
                index=current_month - 1,
                format_func=lambda x: f"Tháng {x}",
                help="Chọn tháng"
            )

        with col4:
            current_year = datetime.now().year
            year = st.selectbox(
                "Năm",
                list(range(current_year - 1, current_year + 2)),
                index=1,
                help="Chọn năm"
            )

        col_submit, col_spacer = st.columns([1, 4])
        
        with col_submit:
            submitted = st.form_submit_button(f"💾 {t('add_budget')}", width='stretch', type="primary")

        if submitted:
            if amount <= 0:
                st.error(f"❌ {t('amount')} > 0")
            else:
                # Check if budget already exists
                from bson.objectid import ObjectId
                existing = budget_model.collection.find_one({
                    'user_id': budget_model.user_id,
                    'category': category,
                    'month': month,
                    'year': year,
                    'is_active': True
                })
                
                result = budget_model.create_budget(
                    category=category,
                    amount=amount,
                    month=month,
                    year=year
                )
                
                if result:
                    translated_category = t(category, category)
                    if existing:
                        # Budget was updated
                        st.success(f"✅ Đã cập nhật ngân sách '{translated_category}' tháng {month}/{year} thành ${amount:,.2f}")
                    else:
                        # New budget created
                        st.success(f"✅ Đã tạo ngân sách '{translated_category}' tháng {month}/{year}: ${amount:,.2f}")
                        st.balloons()
                    st.rerun()
                else:
                    st.error(f"❌ {t('error')}")


def _render_budget_card(budget_info: dict, budget_model: BudgetModel):
    """Render a single budget card with progress"""
    category = budget_info['category']
    # Translate category name
    translated_category = t(category, category)
    budget_amount = budget_info['budget_amount']
    spent_amount = budget_info['spent_amount']
    remaining = budget_info['remaining']
    percentage = budget_info['percentage']
    status = budget_info['status']
    month = budget_info.get('month', 1)
    year = budget_info.get('year', 2025)
    budget_id = budget_info['budget_id']

    bg_color, text_color, icon = _get_status_color(status)

    st.markdown(f"""
        <div style='background: white; padding: 1.5rem; border-radius: 15px; 
                    box-shadow: 0 2px 8px rgba(0,0,0,0.08); border-left: 5px solid {text_color};
                    margin-bottom: 1.5rem;'>
            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;'>
                <div>
                    <h3 style='color: #1f2937; margin: 0; font-size: 1.3rem;'>
                        {icon} {translated_category}
                    </h3>
                    <span style='color: #6b7280; font-size: 0.9rem;'>📅 Tháng {month}/{year}</span>
                </div>
                <div style='text-align: right;'>
                    <div style='font-size: 1.1rem; color: #6b7280;'>
                        Ngân sách: <span style='font-weight: 700; color: #1f2937;'>${budget_amount:,.2f}</span>
                    </div>
                </div>
            </div>
    """, unsafe_allow_html=True)

    # Progress bar
    progress_percentage = min(percentage, 100)
    st.progress(progress_percentage / 100)

    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(t('spent'), f"${spent_amount:,.2f}")
    
    with col2:
        st.metric(t('remaining'), f"${remaining:,.2f}", 
                  delta=f"{remaining:,.2f}" if remaining >= 0 else f"-{abs(remaining):,.2f}",
                  delta_color="normal" if remaining >= 0 else "inverse")
    
    with col3:
        st.metric("📊 ", f"{percentage:.1f}%")
    
    with col4:
        status_labels = {
            'safe': '✅ An Toàn',
            'warning': '⚠️ Cảnh Báo',
            'danger': '🚨 Nguy Hiểm',
            'exceeded': '❌ Vượt Mức',
            'no_budget': '📊 Không Có'
        }
        st.markdown(f"""
            <div style='background: {bg_color}; padding: 0.5rem; border-radius: 8px; text-align: center;'>
                <span style='color: {text_color}; font-weight: 600;'>{status_labels[status]}</span>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Delete button
    if st.button(f"🗑️ {t('delete')}", key=f"del_budget_{budget_id}"):
        if budget_model.delete_budget(budget_id):
            st.success(f"✅ {t('budget_deleted')}")
            st.rerun()
        else:
            st.error(f"❌ {t('error')}")


def _render_budget_list(budget_model: BudgetModel, transaction_model: TransactionModel):
    """Render list of all budgets with their status"""
    
    # Month/Year selector
    col_title, col_month, col_year = st.columns([3, 1, 1])
    
    with col_title:
        st.markdown("""
            <div style='background: white; padding: 1.5rem; border-radius: 15px; 
                        box-shadow: 0 2px 8px rgba(0,0,0,0.08);'>
                <h3 style='color: #1f2937; margin: 0;'>📊 Danh Sách Ngân Sách</h3>
            </div>
        """, unsafe_allow_html=True)
    
    from datetime import datetime
    current_date = datetime.now()
    
    with col_month:
        selected_month = st.selectbox(
            "Tháng",
            list(range(1, 13)),
            index=current_date.month - 1,
            format_func=lambda x: f"T{x}",
            key="budget_list_month"
        )
    
    with col_year:
        selected_year = st.selectbox(
            "Năm",
            list(range(current_date.year - 1, current_date.year + 2)),
            index=1,
            key="budget_list_year"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)

    # Get budget summary for selected month
    budget_summary = budget_model.get_budget_summary(transaction_model, month=selected_month, year=selected_year)

    if not budget_summary:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #e0f2fe 0%, #dbeafe 100%); 
                        padding: 2rem; border-radius: 15px; text-align: center;'>
                <h3 style='color: #0369a1; margin-bottom: 0.5rem;'>💰 Chưa có ngân sách</h3>
                <p style='color: #0c4a6e; margin: 0;'>Hãy tạo ngân sách đầu tiên để quản lý chi tiêu hiệu quả!</p>
            </div>
        """, unsafe_allow_html=True)
        return

    # Summary metrics
    total_budget = sum(b['budget_amount'] for b in budget_summary)
    total_spent = sum(b['spent_amount'] for b in budget_summary)
    total_remaining = total_budget - total_spent

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("💵 Tổng Ngân Sách", f"${total_budget:,.2f}")
    
    with col2:
        st.metric("💸 Tổng Đã Chi", f"${total_spent:,.2f}")
    
    with col3:
        st.metric("💰 Tổng Còn Lại", f"${total_remaining:,.2f}",
                  delta=f"{total_remaining:,.2f}" if total_remaining >= 0 else f"-{abs(total_remaining):,.2f}",
                  delta_color="normal" if total_remaining >= 0 else "inverse")

    st.markdown("---")

    # Display each budget
    for budget_info in budget_summary:
        _render_budget_card(budget_info, budget_model)


def _render_budget_visualization(budget_model: BudgetModel, transaction_model: TransactionModel):
    """Render budget visualization charts"""
    st.markdown("""
        <div style='background: white; padding: 1.5rem; border-radius: 15px; 
                    box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom: 1.5rem;'>
            <h3 style='color: #1f2937; margin: 0;'>📈 Biểu Đồ Ngân Sách</h3>
        </div>
    """, unsafe_allow_html=True)

    from datetime import datetime
    current_date = datetime.now()
    budget_summary = budget_model.get_budget_summary(transaction_model, month=current_date.month, year=current_date.year)

    if not budget_summary:
        st.info("📊 Chưa có dữ liệu ngân sách để hiển thị biểu đồ")
        return

    visualizer = FinanceVisualizer()

    # Create gauge charts for each budget
    cols = st.columns(2)
    
    for idx, budget_info in enumerate(budget_summary):
        col = cols[idx % 2]
        
        with col:
            fig = visualizer.plot_budget_gauge(
                spent=budget_info['spent_amount'],
                budget=budget_info['budget_amount']
            )
            if fig:
                fig.update_layout(title=f"Ngân Sách: {budget_info['category']}")
                st.plotly_chart(fig, width='stretch')


def render_budgets(budget_model: BudgetModel, transaction_model: TransactionModel, category_model: CategoryModel):
    """Main render function for budget management page"""
    
    # Modern header
    st.markdown("""
        <style>
        .budget-header {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .budget-header h1 {
            color: white;
            margin: 0;
            font-size: 2.5rem;
            font-weight: 700;
        }
        .budget-header p {
            color: rgba(255,255,255,0.9);
            margin: 0.5rem 0 0 0;
            font-size: 1.1rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="budget-header">
            <h1>{t('budgets_title')}</h1>
            <p>{t('app_subtitle')}</p>
        </div>
    """, unsafe_allow_html=True)

    # Add budget form
    _render_add_budget(budget_model, category_model)

    st.markdown("---")

    # Budget list with status
    _render_budget_list(budget_model, transaction_model)

    st.markdown("---")

    # Budget visualizations
    _render_budget_visualization(budget_model, transaction_model)
