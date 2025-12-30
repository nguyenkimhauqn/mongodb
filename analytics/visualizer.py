# Only import plotly - all visualizations use plotly, not matplotlib
import plotly.express as px
import plotly.graph_objects as go

class FinanceVisualizer:
    """Class for visualizing financial data using various charts"""
    
    @staticmethod
    def plot_category_spending(category_data):
        """Plot spending by category as a bar chart"""
        if category_data.empty:
            return
        
        fig = px.bar(
            category_data,
            x='Category',
            y='Total',
            title='Spending by Category',
            labels={'Total': 'Amount ($)', 'Category': 'Category'},
            color='Total',
            color_continuous_scale='reds'
        )
        
        fig.update_layout(
            xaxis_tickangle=-45,
            height=500
        )
        
        return fig
    
    @staticmethod
    def plot_income_by_category(category_data):
        """Plot income by category as a bar chart"""
        if category_data.empty:
            return
        
        fig = px.bar(
            category_data,
            x='Category',
            y='Total',
            title='Income by Category',
            labels={'Total': 'Amount ($)', 'Category': 'Category'},
            color='Total',
            color_continuous_scale='Greens'
        )
        
        fig.update_layout(
            xaxis_tickangle=-45,
            height=500
        )
        
        return fig
    
    @staticmethod
    def plot_expense_pie_chart(category_data):
        """Plot expense distribution as pie chart with percentages"""
        if category_data.empty:
            return
        
        # Calculate percentages
        total = category_data['Total'].sum()
        category_data['Percentage'] = (category_data['Total'] / total * 100).round(1)
        
        fig = go.Figure(data=[go.Pie(
            labels=category_data['Category'],
            values=category_data['Total'],
            text=category_data['Percentage'].apply(lambda x: f'{x}%'),
            textposition='inside',
            textfont=dict(size=14, color='white', family='Arial Black'),
            marker=dict(
                colors=px.colors.sequential.Reds,
                line=dict(color='white', width=2)
            ),
            hovertemplate='<b>%{label}</b><br>' +
                         'Amount: $%{value:,.2f}<br>' +
                         'Percentage: %{percent}<br>' +
                         '<extra></extra>'
        )])
        
        fig.update_layout(
            title=dict(
                text='Chi Tiêu Theo Danh Mục',
                font=dict(size=20, color='#1f2937', family='Arial')
            ),
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.02,
                font=dict(size=12)
            ),
            height=550,
            annotations=[
                dict(
                    text=f'Tổng Chi<br>${total:,.0f}',
                    x=0.5, y=0.5,
                    font=dict(size=16, color='#dc2626'),
                    showarrow=False,
                    xref="paper",
                    yref="paper"
                )
            ]
        )
        
        return fig
    
    @staticmethod
    def plot_monthly_trend(monthly_data):
        """Plot monthly income vs expense trend"""
        if monthly_data.empty:
            return
        
        fig = go.Figure()
        
        if 'Expense' in monthly_data.columns:
            fig.add_trace(go.Scatter(
                x=monthly_data.index,
                y=monthly_data['Expense'],
                mode='lines+markers',
                name='Expense',
                line=dict(color='#dc2626', width=3),
                marker=dict(size=8)
            ))
        
        if 'Income' in monthly_data.columns:
            fig.add_trace(go.Scatter(
                x=monthly_data.index,
                y=monthly_data['Income'],
                mode='lines+markers',
                name='Income',
                line=dict(color='#16a34a', width=3),
                marker=dict(size=8)
            ))
        
        fig.update_layout(
            title='Monthly Income vs Expense Trend',
            xaxis_title='Month',
            yaxis_title='Amount ($)',
            hovermode='x unified',
            height=500
        )
        
        return fig
    
    @staticmethod
    def plot_daily_spending(daily_data):
        """Plot daily spending pattern"""
        if daily_data.empty:
            return
        
        fig = px.line(
            daily_data,
            x=daily_data.index,
            y='amount',
            title='Daily Spending Pattern',
            labels={'amount': 'Amount ($)', 'index': 'Date'}
        )
        
        fig.update_traces(line_color='#dc2626', line_width=2)
        fig.update_layout(height=400)
        
        return fig
    
    @staticmethod
    def plot_balance_trend(balance_data):
        """Plot balance over time"""
        if balance_data.empty:
            return
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=balance_data.index,
            y=balance_data['balance'],
            mode='lines',
            name='Balance',
            fill='tozeroy',
            line=dict(color='#667eea', width=3)
        ))
        
        fig.update_layout(
            title='Balance Over Time',
            xaxis_title='Date',
            yaxis_title='Balance ($)',
            hovermode='x',
            height=400
        )
        
        return fig
    
    @staticmethod
    def create_summary_metrics(stats):
        """Create summary visualization with metrics"""
        fig = go.Figure()
        
        categories = ['Income', 'Expense', 'Balance']
        values = [
            stats.get('total_income', 0),
            stats.get('total_expense', 0),
            stats.get('net_balance', 0)
        ]
        colors = ['#16a34a', '#dc2626', '#667eea']
        
        fig.add_trace(go.Bar(
            x=categories,
            y=values,
            marker_color=colors,
            text=[f'${v:,.2f}' for v in values],
            textposition='auto'
        ))
        
        fig.update_layout(
            title='Financial Summary',
            yaxis_title='Amount ($)',
            height=400,
            showlegend=False
        )
        
        return fig
    
    @staticmethod
    def plot_spending_heatmap(transaction_data):
        """Plot spending heatmap by day of week and hour"""
        if transaction_data.empty:
            return
        
        # Create pivot table for heatmap
        transaction_data['weekday'] = transaction_data['date'].dt.day_name()
        transaction_data['hour'] = transaction_data['date'].dt.hour
        
        heatmap_data = transaction_data.pivot_table(
            values='amount',
            index='weekday',
            columns='hour',
            aggfunc='sum',
            fill_value=0
        )
        
        fig = px.imshow(
            heatmap_data,
            labels=dict(x="Hour of Day", y="Day of Week", color="Amount ($)"),
            title="Spending Pattern Heatmap",
            color_continuous_scale='Reds'
        )
        
        fig.update_layout(height=500)
        
        return fig
    
    @staticmethod
    def plot_comparison_bar(income_total, expense_total):
        """Simple income vs expense comparison"""
        fig = go.Figure(data=[
            go.Bar(name='Income', x=['Income'], y=[income_total], marker_color='#16a34a'),
            go.Bar(name='Expense', x=['Expense'], y=[expense_total], marker_color='#dc2626')
        ])
        
        fig.update_layout(
            title='Income vs Expense Comparison',
            yaxis_title='Amount ($)',
            height=400,
            showlegend=True
        )
        
        return fig
    
    @staticmethod
    def plot_cumulative_spending(daily_data):
        """Plot cumulative spending over time"""
        if daily_data.empty:
            return
        
        daily_data_sorted = daily_data.sort_index()
        daily_data_sorted['cumulative'] = daily_data_sorted['amount'].cumsum()
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=daily_data_sorted.index,
            y=daily_data_sorted['cumulative'],
            mode='lines',
            name='Cumulative Spending',
            fill='tozeroy',
            line=dict(color='#f59e0b', width=3)
        ))
        
        fig.update_layout(
            title='Cumulative Spending Over Time',
            xaxis_title='Date',
            yaxis_title='Cumulative Amount ($)',
            hovermode='x',
            height=400
        )
        
        return fig
    
    @staticmethod
    def plot_category_comparison(expense_data, income_data):
        """Compare top categories for income and expense"""
        fig = go.Figure()
        
        if not expense_data.empty:
            top_expenses = expense_data.nlargest(5, 'Total')
            fig.add_trace(go.Bar(
                x=top_expenses['Category'],
                y=top_expenses['Total'],
                name='Top Expenses',
                marker_color='#dc2626'
            ))
        
        if not income_data.empty:
            top_income = income_data.nlargest(5, 'Total')
            fig.add_trace(go.Bar(
                x=top_income['Category'],
                y=top_income['Total'],
                name='Top Income',
                marker_color='#16a34a'
            ))
        
        fig.update_layout(
            title='Top 5 Categories: Income vs Expense',
            xaxis_title='Category',
            yaxis_title='Amount ($)',
            barmode='group',
            height=500
        )
        
        return fig
    
    @staticmethod
    def plot_donut_chart(category_data, title="Phân Bố"):
        """Create a donut chart with clear percentages"""
        if category_data.empty:
            return
        
        total = category_data['Total'].sum()
        category_data['Percentage'] = (category_data['Total'] / total * 100).round(1)
        
        fig = go.Figure(data=[go.Pie(
            labels=category_data['Category'],
            values=category_data['Total'],
            hole=0.5,
            marker=dict(
                colors=px.colors.qualitative.Set3,
                line=dict(color='white', width=3)
            ),
            textposition='outside',
            texttemplate='%{label}<br>%{percent}',
            textfont=dict(size=13, family='Arial'),
            hovertemplate='<b>%{label}</b><br>' +
                         'Số tiền: $%{value:,.2f}<br>' +
                         'Tỷ lệ: %{percent}<br>' +
                         '<extra></extra>'
        )])
        
        fig.update_layout(
            title=dict(
                text=title,
                font=dict(size=20, color='#1f2937')
            ),
            height=550,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            ),
            annotations=[
                dict(
                    text=f'<b>Tổng</b><br>${total:,.0f}',
                    x=0.5, y=0.5,
                    font=dict(size=18, color='#374151'),
                    showarrow=False
                )
            ]
        )
        
        return fig
    
    @staticmethod
    def plot_weekly_average(transaction_data):
        """Plot average spending by day of week"""
        if transaction_data.empty:
            return
        
        transaction_data['weekday'] = transaction_data['date'].dt.day_name()
        
        # Define order of weekdays
        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        weekly_avg = transaction_data.groupby('weekday')['amount'].mean().reindex(weekday_order)
        
        fig = px.bar(
            x=weekly_avg.index,
            y=weekly_avg.values,
            title='Average Spending by Day of Week',
            labels={'x': 'Day of Week', 'y': 'Average Amount ($)'},
            color=weekly_avg.values,
            color_continuous_scale='Blues'
        )
        
        fig.update_layout(height=400)
        
        return fig
    
    @staticmethod
    def plot_budget_gauge(spent, budget):
        """Create a gauge chart for budget tracking"""
        percentage = (spent / budget * 100) if budget > 0 else 0
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=spent,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Budget Usage"},
            delta={'reference': budget, 'increasing': {'color': "red"}},
            gauge={
                'axis': {'range': [None, budget]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, budget * 0.5], 'color': "lightgreen"},
                    {'range': [budget * 0.5, budget * 0.8], 'color': "yellow"},
                    {'range': [budget * 0.8, budget], 'color': "orange"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': budget
                }
            }
        ))
        
        fig.update_layout(height=400)
        
        return fig
    
    @staticmethod
    def plot_transaction_count_trend(transaction_data):
        """Plot number of transactions over time"""
        if transaction_data.empty:
            return
        
        daily_count = transaction_data.groupby(transaction_data['date'].dt.date).size()
        
        fig = px.line(
            x=daily_count.index,
            y=daily_count.values,
            title='Number of Transactions Per Day',
            labels={'x': 'Date', 'y': 'Transaction Count'}
        )
        
        fig.update_traces(line_color='#8b5cf6', line_width=2)
        fig.update_layout(height=400)
        
        return fig
    
    @staticmethod
    def plot_expense_sunburst(category_data):
        """Create a sunburst chart for hierarchical expense view"""
        if category_data.empty:
            return
        
        # Add a root level
        labels = ['Total Expenses'] + list(category_data['Category'])
        parents = [''] + ['Total Expenses'] * len(category_data)
        values = [category_data['Total'].sum()] + list(category_data['Total'])
        
        fig = go.Figure(go.Sunburst(
            labels=labels,
            parents=parents,
            values=values,
            branchvalues="total",
            marker=dict(
                colorscale='Reds',
                cmid=category_data['Total'].mean()
            )
        ))
        
        fig.update_layout(
            title='Expense Breakdown - Sunburst Chart',
            height=600
        )
        
        return fig
    
    @staticmethod
    def plot_3d_pie_chart(category_data, title="Distribution"):
        """Create an advanced 3D-style pie chart"""
        if category_data.empty:
            return
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', 
                  '#F7DC6F', '#BB8FCE', '#85C1E2', '#F8B739', '#52BE80']
        
        fig = go.Figure(data=[go.Pie(
            labels=category_data['Category'],
            values=category_data['Total'],
            hole=0.3,
            pull=[0.05] + [0] * (len(category_data) - 1),  # Pull out the largest slice
            marker=dict(
                colors=colors[:len(category_data)],
                line=dict(color='white', width=2)
            ),
            textposition='auto',
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>Amount: $%{value:,.2f}<br>Percentage: %{percent}<extra></extra>'
        )])
        
        fig.update_layout(
            title=dict(
                text=title,
                font=dict(size=20, color='#2c3e50')
            ),
            height=550,
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.05
            )
        )
        
        return fig
    
    @staticmethod
    def plot_nested_pie_chart(expense_data, income_data):
        """Create a nested pie chart comparing income and expense categories"""
        fig = go.Figure()
        
        # Outer ring - Expense
        if not expense_data.empty:
            fig.add_trace(go.Pie(
                labels=expense_data['Category'],
                values=expense_data['Total'],
                name='Expenses',
                marker=dict(colors=px.colors.sequential.Reds),
                domain=dict(x=[0.2, 0.8], y=[0.2, 0.8]),
                hole=0.5,
                textposition='auto',
                hovertemplate='<b>Expense: %{label}</b><br>$%{value:,.2f}<extra></extra>'
            ))
        
        # Inner ring - Income
        if not income_data.empty:
            fig.add_trace(go.Pie(
                labels=income_data['Category'],
                values=income_data['Total'],
                name='Income',
                marker=dict(colors=px.colors.sequential.Greens),
                domain=dict(x=[0.35, 0.65], y=[0.35, 0.65]),
                hole=0.7,
                textposition='inside',
                hovertemplate='<b>Income: %{label}</b><br>$%{value:,.2f}<extra></extra>'
            ))
        
        fig.update_layout(
            title='Income & Expense Distribution (Nested)',
            height=600,
            showlegend=True,
            annotations=[dict(text='Financial<br>Overview', x=0.5, y=0.5, font_size=16, showarrow=False)]
        )
        
        return fig
    
    @staticmethod
    def plot_polar_bar_chart(category_data, chart_type='expense'):
        """Create a polar bar chart for categories"""
        if category_data.empty:
            return
        
        color = '#dc2626' if chart_type == 'expense' else '#16a34a'
        title = f'{chart_type.capitalize()} Distribution - Polar View'
        
        fig = go.Figure(go.Barpolar(
            r=category_data['Total'],
            theta=category_data['Category'],
            marker=dict(
                color=category_data['Total'],
                colorscale='Reds' if chart_type == 'expense' else 'Greens',
                showscale=True,
                colorbar=dict(title="Amount ($)")
            ),
            hovertemplate='<b>%{theta}</b><br>Amount: $%{r:,.2f}<extra></extra>'
        ))
        
        fig.update_layout(
            title=title,
            polar=dict(
                radialaxis=dict(visible=True, range=[0, category_data['Total'].max() * 1.1]),
                angularaxis=dict(direction="clockwise")
            ),
            height=550
        )
        
        return fig
    
    @staticmethod
    def plot_multi_level_donut(category_summary):
        """Create a multi-level donut chart"""
        if category_summary.empty:
            return
        
        # Separate by type
        expense_data = category_summary[category_summary['type'] == 'Expense']
        income_data = category_summary[category_summary['type'] == 'Income']
        
        fig = go.Figure()
        
        # Outer donut - All categories
        all_labels = list(category_summary['category'])
        all_values = list(category_summary['amount'])
        all_colors = ['#dc2626' if t == 'Expense' else '#16a34a' 
                      for t in category_summary['type']]
        
        fig.add_trace(go.Pie(
            labels=all_labels,
            values=all_values,
            hole=0.6,
            marker=dict(colors=all_colors, line=dict(color='white', width=2)),
            textposition='outside',
            textinfo='label+percent',
            domain=dict(x=[0.1, 0.9], y=[0.1, 0.9])
        ))
        
        # Inner circle - Type summary
        type_labels = ['Expense', 'Income']
        type_values = [
            expense_data['amount'].sum() if not expense_data.empty else 0,
            income_data['amount'].sum() if not income_data.empty else 0
        ]
        
        fig.add_trace(go.Pie(
            labels=type_labels,
            values=type_values,
            hole=0.8,
            marker=dict(colors=['#dc2626', '#16a34a']),
            textposition='inside',
            textinfo='label',
            domain=dict(x=[0.3, 0.7], y=[0.3, 0.7]),
            showlegend=False
        ))
        
        fig.update_layout(
            title='Multi-Level Financial Distribution',
            height=650,
            annotations=[
                dict(
                    text=f'Total<br>${sum(type_values):,.0f}',
                    x=0.5, y=0.5,
                    font_size=18,
                    showarrow=False
                )
            ]
        )
        
        return fig
        