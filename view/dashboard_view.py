import streamlit as st
from analytics.analyzer import FinanceAnalyzer
from dataset.transaction_model import TransactionModel


def render_dashboard(analyzer_model: FinanceAnalyzer, transaction_model: TransactionModel):
    """Render dashboard with analytics"""
    st.title("📊 Dashboard")
    st.markdown("---")
    
    # Get statistics summary
    stats = analyzer_model.get_statistics_summary()
    
    if not stats or stats.get('transaction_count', 0) == 0:
        st.info("No transactions yet. Start adding your first transaction!")
        return
    
    # Display key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💵 Total Income",
            value=f"${stats['total_income']:,.2f}",
            delta=f"{stats['income_count']} transactions"
        )
    
    with col2:
        st.metric(
            label="💸 Total Expense",
            value=f"${stats['total_expense']:,.2f}",
            delta=f"{stats['expense_count']} transactions"
        )
    
    with col3:
        st.metric(
            label="💰 Net Balance",
            value=f"${stats['net_balance']:,.2f}",
            delta="Balance"
        )
    
    with col4:
        st.metric(
            label="📊 Total Transactions",
            value=stats['transaction_count']
        )
    
    st.markdown("---")
    
    # Spending by Category
    st.subheader("📊 Spending by Category")
    category_spending = analyzer_model.get_spending_by_category()
    
    if not category_spending.empty:
        st.dataframe(category_spending, width='stretch')
    else:
        st.info("No expense data available")
    
    st.markdown("---")
    
    # Monthly Trend
    st.subheader("📈 Monthly Trend")
    monthly_trend = analyzer_model.get_monthly_trend()
    
    if not monthly_trend.empty:
        st.line_chart(monthly_trend)
    else:
        st.info("Not enough data for monthly trend")
