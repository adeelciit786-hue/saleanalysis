"""
Data Visualization Module
Creates professional charts for sales analysis and forecasting
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime
from utils import to_float, safe_arithmetic

class SalesVisualizer:
    """Generate professional sales visualization charts"""
    
    @staticmethod
    def create_historical_sales_chart(historical_data_list):
        """
        Create line chart of historical daily sales (Nov + Dec)
        
        Args:
            historical_data_list: List of dicts with historical data
        
        Returns:
            Plotly figure object
        """
        x_labels = []
        y_values = []
        
        for data in historical_data_list:
            for date, weekday, total in zip(data['dates'], data['weekdays'], data['totals']):
                label = f"{date} ({weekday})"
                x_labels.append(label)
                # Ensure total is a float
                y_values.append(to_float(total, default=0.0))
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x_labels,
            y=y_values,
            mode='lines+markers',
            name='Daily Sales',
            line=dict(color='#2E86AB', width=3),
            marker=dict(size=6)
        ))
        
        fig.update_layout(
            title=dict(
                text='Daily Sales Trend – November & December<br><sub>Combined Sales Across All Branches</sub>',
                x=0.5,
                xanchor='center'
            ),
            xaxis_title='Date & Weekday',
            yaxis_title='Daily Sales',
            hovermode='x unified',
            plot_bgcolor='#F8F9FA',
            paper_bgcolor='white',
            font=dict(family='Arial, sans-serif', size=12),
            height=550,
            margin=dict(l=60, r=40, t=100, b=120),
            xaxis=dict(
                tickangle=-45,
                showgrid=True,
                gridwidth=1,
                gridcolor='lightgray'
            ),
            yaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='lightgray'
            )
        )
        
        return fig
    
    @staticmethod
    def create_weekday_chart(weekday_averages):
        """
        Create bar chart of average sales by weekday
        
        Args:
            weekday_averages: Dict with weekday -> average sales
        
        Returns:
            Plotly figure object
        """
        weekdays = list(weekday_averages.keys())
        # Ensure all values are floats
        values = [to_float(v, default=0.0) for v in weekday_averages.values()]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=weekdays,
            y=values,
            name='Average Sales',
            marker=dict(color='#A23B72'),
            text=[f"{v:,.0f}" for v in values],
            textposition='auto',
        ))
        
        fig.update_layout(
            title='Average Sales by Weekday (Historical Analysis)',
            xaxis_title='Weekday',
            yaxis_title='Average Daily Sales',
            plot_bgcolor='#F8F9FA',
            paper_bgcolor='white',
            font=dict(family='Arial, sans-serif', size=12),
            showlegend=False,
            height=450,
            margin=dict(l=60, r=40, t=80, b=60)
        )
        
        return fig
    
    @staticmethod
    def create_forecast_chart(forecast_data):
        """
        Create forecast visualization with actual vs projected
        
        Args:
            forecast_data: Dict from forecaster.forecast_month()
        
        Returns:
            Plotly figure object
        """
        forecast = forecast_data['forecast']
        
        dates = [f['date'] for f in forecast]
        weekdays = [f['weekday'] for f in forecast]
        # Ensure all sales values are floats
        sales = [to_float(f['projected_sales'], default=0.0) for f in forecast]
        is_past = [f['is_past'] for f in forecast]
        is_today = [f['is_today'] for f in forecast]
        
        # Create labels with date and weekday
        labels = [f"{d} ({w})" for d, w in zip(dates, weekdays)]
        
        # Separate past, today, and future
        past_labels = [labels[i] for i, p in enumerate(is_past) if p]
        today_labels = [labels[i] for i, t in enumerate(is_today) if t]
        future_labels = [labels[i] for i, p in enumerate(is_past) if not p and not is_today[i]]
        
        past_sales = [sales[i] for i, p in enumerate(is_past) if p]
        today_sales = [sales[i] for i, t in enumerate(is_today) if t]
        future_sales = [sales[i] for i, p in enumerate(is_past) if not p and not is_today[i]]
        
        fig = go.Figure()
        
        # Add past actual data (if any)
        if past_sales:
            fig.add_trace(go.Scatter(
                x=past_labels,
                y=past_sales,
                mode='lines+markers',
                name='Actual Sales',
                line=dict(color='#06A77D', width=2),
                marker=dict(size=5)
            ))
        
        # Add today
        if today_sales:
            fig.add_trace(go.Scatter(
                x=today_labels,
                y=today_sales,
                mode='markers',
                name='Today',
                marker=dict(color='#F77F00', size=10, symbol='diamond'),
                showlegend=True
            ))
        
        # Add projected data
        if future_sales:
            fig.add_trace(go.Scatter(
                x=future_labels,
                y=future_sales,
                mode='lines+markers',
                name='Projected Sales',
                line=dict(color='#2E86AB', width=2, dash='dash'),
                marker=dict(size=5)
            ))
        
        # Add target line if provided
        if forecast_data.get('target_sales'):
            target_line_y = safe_arithmetic(to_float(forecast_data['target_sales']), len(dates), 'divide')
            fig.add_hline(
                y=target_line_y,
                line_dash="dot",
                line_color="red",
                annotation_text=f"Daily Target: {target_line_y:,.0f}",
                annotation_position="right"
            )
        
        fig.update_layout(
            title=f"Sales Projection – {forecast_data['month']} {forecast_data['year']}",
            xaxis_title='Date & Weekday',
            yaxis_title='Daily Sales',
            hovermode='x unified',
            plot_bgcolor='#F8F9FA',
            paper_bgcolor='white',
            font=dict(family='Arial, sans-serif', size=11),
            height=500,
            margin=dict(l=60, r=40, t=80, b=60)
        )
        
        return fig
    
    @staticmethod
    def create_target_chart(forecast_data):
        """
        Create cumulative forecast vs target chart
        
        Args:
            forecast_data: Dict from forecaster.forecast_month()
        
        Returns:
            Plotly figure object
        """
        if not forecast_data.get('target_sales'):
            return None
        
        forecast = forecast_data['forecast']
        
        dates = [item['date'] for item in forecast]
        weekdays = [item['weekday'] for item in forecast]
        labels = [f"{d} ({w})" for d, w in zip(dates, weekdays)]
        # Ensure cumulative values are floats
        cumulative = [to_float(item['cumulative_sales'], default=0.0) for item in forecast]
        
        # Ensure target is a float
        target_value = to_float(forecast_data['target_sales'], default=0.0)
        target_line = [target_value] * len(dates)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=labels,
            y=cumulative,
            mode='lines+markers',
            name='Projected Cumulative Sales',
            line=dict(color='#2E86AB', width=2),
            fill='tozeroy',
            fillcolor='rgba(46, 134, 171, 0.1)'
        ))
        
        fig.add_trace(go.Scatter(
            x=labels,
            y=target_line,
            mode='lines',
            name='Monthly Target',
            line=dict(color='red', width=2, dash='dash')
        ))
        
        fig.update_layout(
            title='Projected Monthly Sales vs Target',
            xaxis_title='Date & Weekday',
            yaxis_title='Cumulative Sales',
            hovermode='x unified',
            plot_bgcolor='#F8F9FA',
            paper_bgcolor='white',
            font=dict(family='Arial, sans-serif', size=11),
            height=450,
            margin=dict(l=60, r=40, t=80, b=60)
        )
        
        return fig
    
    @staticmethod
    def create_actual_vs_projected_chart(forecast_data, actual_data):
        """
        Create side-by-side comparison of actual vs projected sales
        
        Args:
            forecast_data: Dict from forecaster.forecast_month()
            actual_data: Dict with dates, weekdays, and actual daily totals from current month upload
        
        Returns:
            Plotly figure object
        """
        if not actual_data or not actual_data.get('totals'):
            return None
        
        forecast = forecast_data['forecast']
        
        # Get common dates (up to current day or available actual data)
        dates = [f['date'] for f in forecast]
        weekdays = [f['weekday'] for f in forecast]
        projected = [to_float(f['projected_sales'], default=0.0) for f in forecast]
        
        # Get actual sales (pad with None if not available)
        actual = []
        actual_dates = actual_data.get('dates', [])
        actual_totals = actual_data.get('totals', [])
        
        for i, date in enumerate(dates):
            if date <= len(actual_totals) and date <= len(actual_dates):
                idx = actual_dates.index(date) if date in actual_dates else -1
                if idx >= 0:
                    actual.append(to_float(actual_totals[idx], default=None))
                else:
                    actual.append(None)
            else:
                actual.append(None)
        
        # Create labels
        labels = [f"{d} ({w})" for d, w in zip(dates, weekdays)]
        
        fig = go.Figure()
        
        # Add projected sales
        fig.add_trace(go.Bar(
            x=labels,
            y=projected,
            name='Projected Sales',
            marker=dict(color='#FF0000'),
            opacity=0.7,
            text=[f"{v:,.0f}" for v in projected],
            textposition='auto',
        ))
        
        # Add actual sales (only non-null values)
        actual_labels = [labels[i] for i, v in enumerate(actual) if v is not None]
        actual_values = [v for v in actual if v is not None]
        
        if actual_values:
            fig.add_trace(go.Bar(
                x=actual_labels,
                y=actual_values,
                name='Actual Sales',
                marker=dict(color='#00DD00'),
                opacity=0.8,
                text=[f"{v:,.0f}" for v in actual_values],
                textposition='auto',
            ))
        
        fig.update_layout(
            title='Actual vs Projected Sales – Daily Comparison',
            xaxis_title='Date & Weekday',
            yaxis_title='Daily Sales',
            barmode='group',
            hovermode='x unified',
            plot_bgcolor='#F8F9FA',
            paper_bgcolor='white',
            font=dict(family='Arial, sans-serif', size=11),
            height=550,
            margin=dict(l=60, r=40, t=80, b=120),
            xaxis=dict(
                tickangle=-45,
                showgrid=True,
                gridwidth=1,
                gridcolor='lightgray'
            ),
            yaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='lightgray'
            ),
            legend=dict(
                x=0.5,
                y=-0.18,
                xanchor='center',
                yanchor='top',
                orientation='h',
                bgcolor='rgba(255, 255, 255, 0.95)',
                bordercolor='#cccccc',
                borderwidth=1
            )
        )
        
        return fig