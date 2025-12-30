import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from analytics.visualizer import FinanceVisualizer
from language_manager import t

def render_home(transaction_model, category_model):
    """Render home page with dashboard"""
    
    # Modern header with gradient background
    st.markdown("""
        <style>
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .main-header h1 {
            color: white;
            margin: 0;
            font-size: 2.5rem;
            font-weight: 700;
        }
        .main-header p {
            color: rgba(255,255,255,0.9);
            margin: 0.5rem 0 0 0;
            font-size: 1.1rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="main-header">
            <h1>{t('dashboard_title')}</h1>
            <p>{t('app_subtitle')}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Get statistics
    stats = transaction_model.get_statistics()
    
    # Display key metrics with modern styling
    st.markdown("""
        <style>
        div[data-testid="stMetricValue"] {
            font-size: 2rem;
            font-weight: 700;
        }
        div[data-testid="stMetricLabel"] {
            font-size: 1rem;
            font-weight: 600;
        }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4, gap="large")
    
    with col1:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%); 
                        padding: 1.5rem; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
        """, unsafe_allow_html=True)
        st.metric(
            label=t('total_income'),
            value=f"${stats['total_income']:,.2f}",
            delta=f"{stats['income_count']} {t('transactions_label')}",
            delta_color="normal"
        )
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); 
                        padding: 1.5rem; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
        """, unsafe_allow_html=True)
        st.metric(
            label=t('total_expense'),
            value=f"${stats['total_expense']:,.2f}",
            delta=f"{stats['expense_count']} {t('transactions_label')}",
            delta_color="normal"
        )
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        balance_delta = stats['total_income'] - stats['total_expense']
        st.markdown("""
            <div style='background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); 
                        padding: 1.5rem; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
        """, unsafe_allow_html=True)
        st.metric(
            label=t('net_balance'),
            value=f"${stats['balance']:,.2f}",
            delta=f"${balance_delta:,.2f}",
            delta_color="normal" if balance_delta >= 0 else "inverse"
        )
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); 
                        padding: 1.5rem; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
        """, unsafe_allow_html=True)
        st.metric(
            label=t('total_transactions'),
            value=stats['total_transactions']
        )
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Recent Transactions
    col_left, col_right = st.columns([2, 1], gap="large")
    
    with col_left:
        st.markdown(f"""
            <div style='background: white; padding: 1.5rem; border-radius: 15px; 
                        box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom: 1rem;'>
                <h3 style='margin: 0; color: #1f2937;'>{t('recent_transactions')}</h3>
            </div>
        """, unsafe_allow_html=True)
        
        recent_trans = transaction_model.get_all_transactions()[:10]
        
        if recent_trans:
            for trans in recent_trans:
                trans_type = trans.get('type', 'Unknown')
                category = trans.get('category', 'N/A')
                # Translate category name
                translated_category = t(category, category)
                amount = trans.get('amount', 0)
                desc = trans.get('description', '')
                trans_date = trans.get('transaction_date', datetime.now())
                
                # Format date
                if isinstance(trans_date, datetime):
                    date_str = trans_date.strftime('%d %b %Y')
                else:
                    date_str = str(trans_date)
                
                # Color based on type
                if trans_type == 'Income':
                    color = "#28a745"
                    icon = "📈"
                else:
                    color = "#dc3545"
                    icon = "📉"
                
                st.markdown(f"""
                    <div style='background: white; padding: 1rem; border-radius: 10px; 
                                margin-bottom: 0.8rem; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                                border-left: 4px solid {color};'>
                        <div style='display: flex; justify-content: space-between; align-items: center;'>
                            <div style='flex: 1;'>
                                <div style='font-size: 1.1rem; font-weight: 600; color: #1f2937;'>
                                    {icon} {translated_category}
                                </div>
                                <div style='color: #6b7280; font-size: 0.9rem; margin-top: 0.3rem;'>
                                    {desc if desc else t('no_transactions')}
                                </div>
                            </div>
                            <div style='text-align: center; padding: 0 1.5rem;'>
                                <div style='color: #6b7280; font-size: 0.85rem;'>📅 {date_str}</div>
                            </div>
                            <div style='text-align: right;'>
                                <div style='font-size: 1.3rem; font-weight: 700; color: {color};'>
                                    ${amount:,.2f}
                                </div>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #e0f2fe 0%, #dbeafe 100%); 
                            padding: 2rem; border-radius: 15px; text-align: center; margin-top: 1rem;'>
                    <h3 style='color: #0369a1; margin-bottom: 0.5rem;'>📝 {t('no_transactions')}</h3>
                    <p style='color: #0c4a6e; margin: 0;'>Bắt đầu thêm giao dịch đầu tiên của bạn!</p>
                </div>
            """, unsafe_allow_html=True)
    
    with col_right:
        st.markdown(f"""
            <div style='background: white; padding: 1.5rem; border-radius: 15px; 
                        box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom: 1rem;'>
                <h3 style='margin: 0; color: #1f2937;'>{t('spending_by_category')}</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Get all transactions
        all_trans = transaction_model.get_all_transactions()
        
        if all_trans:
            # Create dataframe for analysis
            df = pd.DataFrame(all_trans)
            
            # Group by category and sum amounts
            if 'category' in df.columns and 'amount' in df.columns:
                category_summary = df.groupby(['type', 'category'])['amount'].sum().reset_index()
                
                # Display Expense categories
                st.markdown("""
                    <div style='background: #fef2f2; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;'>
                        <h4 style='color: #dc2626; margin: 0 0 0.8rem 0;'>💸 Chi Tiêu</h4>
                    </div>
                """, unsafe_allow_html=True)
                
                expense_summary = category_summary[category_summary['type'] == 'Expense']
                if not expense_summary.empty:
                    for _, row in expense_summary.iterrows():
                        st.markdown(f"""
                            <div style='background: white; padding: 0.8rem; border-radius: 8px; 
                                        margin-bottom: 0.5rem; border-left: 3px solid #dc2626;'>
                                <div style='display: flex; justify-content: space-between;'>
                                    <span style='font-weight: 600; color: #374151;'>{row['category']}</span>
                                    <span style='font-weight: 700; color: #dc2626;'>${row['amount']:,.2f}</span>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.caption("Chưa có giao dịch chi tiêu")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Display Income categories
                st.markdown("""
                    <div style='background: #f0fdf4; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;'>
                        <h4 style='color: #16a34a; margin: 0 0 0.8rem 0;'>💵 Thu Nhập</h4>
                    </div>
                """, unsafe_allow_html=True)
                
                income_summary = category_summary[category_summary['type'] == 'Income']
                if not income_summary.empty:
                    for _, row in income_summary.iterrows():
                        st.markdown(f"""
                            <div style='background: white; padding: 0.8rem; border-radius: 8px; 
                                        margin-bottom: 0.5rem; border-left: 3px solid #16a34a;'>
                                <div style='display: flex; justify-content: space-between;'>
                                    <span style='font-weight: 600; color: #374151;'>{row['category']}</span>
                                    <span style='font-weight: 700; color: #16a34a;'>${row['amount']:,.2f}</span>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.caption("Chưa có giao dịch thu nhập")
        else:
            st.markdown("""
                <div style='background: #f3f4f6; padding: 1.5rem; border-radius: 10px; text-align: center;'>
                    <p style='color: #6b7280; margin: 0;'>📊 Chưa có dữ liệu</p>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Charts Section
    if all_trans:
        st.markdown("""
            <div style='background: white; padding: 1.5rem; border-radius: 15px; 
                        box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom: 2rem;'>
                <h3 style='color: #1f2937; margin: 0;'>📈 Biểu Đồ Phân Tích</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Prepare data for visualization
        visualizer = FinanceVisualizer()
        
        # Row 1: Pie Charts
        chart_col1, chart_col2 = st.columns(2, gap="large")
        
        with chart_col1:
            # Expense Pie Chart
            expense_df = df[df['type'] == 'Expense']
            if not expense_df.empty:
                expense_summary = expense_df.groupby('category')['amount'].sum().reset_index()
                expense_summary.columns = ['Category', 'Total']
                expense_summary = expense_summary.sort_values('Total', ascending=False)
                
                fig = visualizer.plot_expense_pie_chart(expense_summary)
                if fig:
                    st.plotly_chart(fig, width='stretch')
            else:
                st.info("Chưa có dữ liệu chi tiêu")
        
        with chart_col2:
            # Income Donut Chart
            income_df = df[df['type'] == 'Income']
            if not income_df.empty:
                income_summary = income_df.groupby('category')['amount'].sum().reset_index()
                income_summary.columns = ['Category', 'Total']
                income_summary = income_summary.sort_values('Total', ascending=False)
                
                fig = visualizer.plot_donut_chart(income_summary, title="Thu Nhập Theo Danh Mục")
                if fig:
                    st.plotly_chart(fig, width='stretch')
            else:
                st.info("Chưa có dữ liệu thu nhập")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Row 2: Bar Charts
        chart_col3, chart_col4 = st.columns(2, gap="large")
        
        with chart_col3:
            # Category Spending Bar Chart
            if not expense_df.empty:
                expense_summary = expense_df.groupby('category')['amount'].sum().reset_index()
                expense_summary.columns = ['Category', 'Total']
                expense_summary['Count'] = expense_df.groupby('category').size().values
                expense_summary['Average'] = expense_summary['Total'] / expense_summary['Count']
                
                fig = visualizer.plot_category_spending(expense_summary)
                if fig:
                    st.plotly_chart(fig, width='stretch')
        
        with chart_col4:
            # Income vs Expense Comparison
            if not expense_df.empty or not income_df.empty:
                total_expense = expense_df['amount'].sum() if not expense_df.empty else 0
                total_income = income_df['amount'].sum() if not income_df.empty else 0
                
                fig = visualizer.plot_comparison_bar(total_income, total_expense)
                if fig:
                    st.plotly_chart(fig, width='stretch')
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Row 3: Trend Line Chart
        st.subheader("📊 Xu Hướng Thu Chi Theo Thời Gian")
        
        # Convert date to datetime if needed
        if 'date' in df.columns:
            df['transaction_date'] = pd.to_datetime(df['date'])
        else:
            df['transaction_date'] = pd.to_datetime(df.get('transaction_date', df.index))
        
        # Group by month for better visualization
        df['month'] = df['transaction_date'].dt.to_period('M')
        monthly_data = df.groupby(['month', 'type'])['amount'].sum().unstack(fill_value=0)
        monthly_data.index = monthly_data.index.to_timestamp()
        
        if not monthly_data.empty:
            fig = visualizer.plot_monthly_trend(monthly_data)
            if fig:
                st.plotly_chart(fig, width='stretch')
        else:
            st.info("Chưa đủ dữ liệu để hiển thị xu hướng")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1.5rem; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <h3 style='color: white; margin: 0 0 1rem 0;'>{t('quick_actions')}</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <style>
        /* Quick action buttons styling */
        div[data-testid="column"] > div > div.stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border: none !important;
            padding: 1.2rem 1rem !important;
            font-size: 1.05rem !important;
            font-weight: 600 !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3) !important;
            transition: all 0.3s ease !important;
            width: 100% !important;
            height: 60px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }
        div[data-testid="column"] > div > div.stButton > button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 8px 16px rgba(102, 126, 234, 0.4) !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    col_action1, col_action2, col_action3 = st.columns(3, gap="medium")
    
    with col_action1:
        if st.button(t("quick_add_transaction"), key="quick_add_trans", use_container_width=True):
            st.info(t("quick_add_info"))
    
    with col_action2:
        if st.button(t("quick_manage_categories"), key="quick_categories", use_container_width=True):
            st.info(t("quick_category_info"))
    
    with col_action3:
        if st.button(t("quick_view_analytics"), key="quick_analytics", use_container_width=True):
            st.info(t("quick_analytics_info"))
