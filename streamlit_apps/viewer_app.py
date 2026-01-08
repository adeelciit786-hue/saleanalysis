"""
Champion Cleaners Sales Dashboard - Viewer Interface (Streamlit)
Public read-only dashboard for management team (no authentication required)
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import sys
from pathlib import Path
import traceback

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent / 'sales_app'))

try:
    from excel_loader import ExcelLoader
    from forecast import SalesForecaster
    from visualizer import SalesVisualizer
    from utils import to_float
except ImportError as e:
    st.error(f"Import Error: {str(e)}")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Management Dashboard - Champion Cleaners",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if 'data_cache' not in st.session_state:
    st.session_state.data_cache = None
if 'cache_time' not in st.session_state:
    st.session_state.cache_time = None

def load_sample_data():
    """Load sample data if no data exists"""
    # This would normally load from the Flask API or shared database
    # For now, returns None to show empty state
    return None

# Header
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("# 📊 Champion Cleaners Sales Dashboard")
    st.markdown("### Real-time Sales Analysis & Performance Monitoring")

with col2:
    st.markdown("""
    <div style='text-align: right; padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
    color: white; border-radius: 8px; font-weight: 600;'>
    👁️ Management View
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Main content
st.info("""
✨ **Live Dashboard** - This dashboard displays real-time sales data from the administration backend.  
Data updates automatically when new sales information is uploaded by the admin team.
""")

# Try to load data from sample or API
data = load_sample_data()

if data is None:
    # Empty state
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 3rem;'>
            <div style='font-size: 4rem; margin-bottom: 1rem;'>📊</div>
            <h2>No Data Available Yet</h2>
            <p style='color: #666; font-size: 1.05rem;'>
                The sales dashboard is waiting for data uploads from the administration backend.
            </p>
            <p style='color: #888; margin-top: 1.5rem; line-height: 1.8;'>
                Once historical and current month sales data are uploaded, this dashboard will display:
            </p>
            <ul style='color: #666; text-align: left; max-width: 400px; margin: 1rem auto;'>
                <li>✓ Historical sales trends and patterns</li>
                <li>✓ Weekday performance analysis</li>
                <li>✓ Sales forecasts for the current month</li>
                <li>✓ Target vs projection comparison</li>
                <li>✓ Actual vs projected daily sales</li>
                <li>✓ Real-time KPI metrics</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
else:
    try:
        # Create forecaster
        forecaster = SalesForecaster(data['historical'])
        weekday_averages = forecaster.get_weekday_averages()
        
        # Generate forecast
        forecast_data = forecaster.forecast_month(
            'JANUARY',
            data.get('target')
        )
        
        # Create visualizer
        viz = SalesVisualizer()
        
        # KPIs
        st.markdown("## 📈 Key Performance Indicators")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        today = datetime.now()
        today_sales = to_float(forecast_data.get('today_sales', 0), 0)
        total_projected = to_float(forecast_data.get('total_projected', 0), 0)
        gap = to_float(forecast_data.get('projected_vs_target', 0), 0) if data.get('target') else 0
        gap_percent = to_float(forecast_data.get('target_gap_percent', 0), 0) if data.get('target') else 0
        
        with col1:
            st.metric("📅 Today's Date", today.strftime("%d %b, %Y"))
        with col2:
            st.metric("💰 Projected Today", f"AED {today_sales:,.0f}")
        with col3:
            st.metric("📊 Monthly Projection", f"AED {total_projected:,.0f}")
        with col4:
            if data.get('target'):
                st.metric("🎯 Monthly Target", f"AED {data.get('target'):,.0f}")
            else:
                st.metric("🎯 Target", "Not Set")
        with col5:
            if data.get('target'):
                color = "🟢" if gap >= 0 else "🔴"
                st.metric("📉 Target Gap", f"{color} AED {gap:,.0f}", f"{gap_percent:.1f}%")
            else:
                st.metric("📉 Gap", "—")
        
        st.divider()
        
        # Charts section
        st.markdown("## 📊 Analytics & Visualizations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📈 Daily Sales Trend")
            st.markdown("Historical sales data showing daily patterns and trends.")
            try:
                chart1 = viz.create_historical_sales_chart(data['historical'])
                st.plotly_chart(chart1, use_container_width=True)
            except Exception as e:
                st.warning(f"Could not display chart: {str(e)}")
        
        with col2:
            st.markdown("### 📊 Weekday Performance")
            st.markdown("Average sales comparison across days of the week.")
            try:
                chart2 = viz.create_weekday_chart(weekday_averages)
                st.plotly_chart(chart2, use_container_width=True)
            except Exception as e:
                st.warning(f"Could not display chart: {str(e)}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🔮 Monthly Forecast")
            st.markdown("Projected sales for the current month based on historical patterns.")
            try:
                chart3 = viz.create_forecast_chart(forecast_data)
                st.plotly_chart(chart3, use_container_width=True)
            except Exception as e:
                st.warning(f"Could not display chart: {str(e)}")
        
        with col2:
            if data.get('target'):
                st.markdown("### 🎯 Target vs Projection")
                st.markdown("Comparison of forecasted sales against monthly targets.")
                try:
                    chart4 = viz.create_target_chart(forecast_data)
                    st.plotly_chart(chart4, use_container_width=True)
                except Exception as e:
                    st.warning(f"Could not display chart: {str(e)}")
            else:
                st.markdown("### 🎯 Target vs Projection")
                st.info("✓ Target comparison will appear once target is set in admin panel")
        
        # Actual vs Projected
        if data.get('current'):
            st.markdown("### 🟢 Actual vs Projected Sales")
            st.markdown("Daily comparison of actual uploaded sales against projections")
            try:
                chart5 = viz.create_actual_vs_projected_chart(forecast_data, data['current'])
                st.plotly_chart(chart5, use_container_width=True)
            except Exception as e:
                st.warning(f"Could not display chart: {str(e)}")
        
        st.divider()
        
        # Analysis Summary
        st.markdown("## 📋 Analysis Summary")
        
        summary_col1, summary_col2 = st.columns(2)
        
        with summary_col1:
            st.markdown("""
            #### Data Overview
            - **Historical Data Loaded**: 2 months (Nov & Dec 2025)
            - **Date Range**: Nov 1 - Dec 31, 2025
            - **Total Records**: {0} days
            - **Branches Tracked**: All
            """.format(len(data.get('historical', []))))
        
        with summary_col2:
            st.markdown("""
            #### Forecast Methodology
            - **Algorithm**: Weekday-based average analysis
            - **Pattern Recognition**: 7-day cycle (Mon-Sun)
            - **Seasonality**: Not applied (short-term forecast)
            - **Confidence**: High (based on 2-month history)
            """)
        
    except Exception as e:
        st.error(f"Error loading dashboard: {str(e)}")
        st.info("Please ensure data has been uploaded in the admin panel.")

st.divider()

# Footer
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📖 Documentation")
    st.markdown("[GitHub Repository](https://github.com/adeelciit786-hue/champion)")

with col2:
    st.markdown("### 🔧 Admin Panel")
    st.markdown("[Admin Interface](https://admin-champion.streamlit.app)")

with col3:
    st.markdown("### 📞 Support")
    st.markdown("📧 adeelciit786@gmail.com")

st.markdown("""
<div style='text-align: center; margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #eee; color: #999;'>
    <p><strong>Champion Cleaners Sales Dashboard</strong> • Version 1.0.0 • January 2026</p>
    <p>💡 <em>Real-time sales intelligence powered by advanced forecasting</em></p>
</div>
""", unsafe_allow_html=True)
