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

# Page configuration FIRST
st.set_page_config(
    page_title="Management Dashboard - Champion Cleaners",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent / 'sales_app'))

IMPORTS_OK = True
try:
    from forecast import SalesForecaster
    from visualizer import SalesVisualizer
    from utils import to_float
    from shared_storage import load_dashboard_data
except ImportError as e:
    st.error(f"Import Error: {str(e)}")
    st.warning("Modules will be available once dependencies finish installing")
    IMPORTS_OK = False

# Professional Color Scheme
PRIMARY_BLUE = "#1E88E5"
SECONDARY_GREEN = "#43A047"
ACCENT_RED = "#E53935"
LIGHT_BG = "#F5F7FA"
DARK_TEXT = "#1A237E"
BORDER_COLOR = "#E0E7FF"

# Custom CSS with Professional Styling
st.markdown(f"""
<style>
    :root {{
        --primary-blue: {PRIMARY_BLUE};
        --secondary-green: {SECONDARY_GREEN};
        --accent-red: {ACCENT_RED};
        --light-bg: {LIGHT_BG};
        --dark-text: {DARK_TEXT};
    }}
    
    .main {{
        padding: 2rem;
        background: linear-gradient(135deg, {LIGHT_BG} 0%, #FFFFFF 100%);
    }}
    
    .header-title {{
        background: linear-gradient(135deg, {PRIMARY_BLUE} 0%, #1565C0 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(30, 136, 229, 0.2);
    }}
    
    .stMetric {{
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid {PRIMARY_BLUE};
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }}
    
    .metric-positive {{
        border-left-color: {SECONDARY_GREEN};
    }}
    
    .metric-negative {{
        border-left-color: {ACCENT_RED};
    }}
    
    .stButton>button {{
        background: linear-gradient(135deg, {PRIMARY_BLUE} 0%, #1565C0 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
    }}
    
    .stButton>button:hover {{
        box-shadow: 0 4px 16px rgba(30, 136, 229, 0.4);
        transform: translateY(-2px);
    }}
    
    .stSuccess {{
        background: linear-gradient(135deg, rgba(67, 160, 71, 0.1), rgba(67, 160, 71, 0.05));
        border-left: 4px solid {SECONDARY_GREEN};
        border-radius: 8px;
    }}
    
    .stWarning {{
        background: linear-gradient(135deg, rgba(229, 57, 53, 0.1), rgba(229, 57, 53, 0.05));
        border-left: 4px solid {ACCENT_RED};
        border-radius: 8px;
    }}
    
    .stInfo {{
        background: linear-gradient(135deg, rgba(30, 136, 229, 0.1), rgba(30, 136, 229, 0.05));
        border-left: 4px solid {PRIMARY_BLUE};
        border-radius: 8px;
    }}
    
    h1, h2, h3 {{
        color: {DARK_TEXT};
        font-weight: 700;
    }}
    
    .chart-container {{
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin: 1rem 0;
    }}
    
    .empty-state {{
        text-align: center;
        padding: 3rem;
        background: white;
        border-radius: 12px;
        border: 2px dashed {BORDER_COLOR};
    }}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown(f"""
<div class='header-title'>
    <div style='display: flex; align-items: center; justify-content: space-between;'>
        <div>
            <h1 style='margin: 0; font-size: 2.5rem;'>📊 Champion Cleaners Sales Dashboard</h1>
            <p style='margin: 0.5rem 0 0 0; font-size: 1.1rem; opacity: 0.95;'>Real-time Sales Analysis & Performance Monitoring</p>
        </div>
        <div style='text-align: right;'>
            <div style='font-size: 3rem;'>👁️</div>
            <p style='margin: 0.5rem 0 0 0; font-weight: 600; font-size: 1rem;'>Management View</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Info box
st.info("""
✨ **Live Dashboard** - This dashboard displays real-time sales data from the administration backend.  
Data updates automatically when new sales information is uploaded by the admin team.
""")

# Load data from shared storage
if not IMPORTS_OK:
    st.warning("⚠️ Modules loading... Please refresh in 30 seconds")
    st.stop()

data = load_dashboard_data()

if data is None or not data.get('historical_data'):
    # Empty state
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class='empty-state'>
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
        # Extract data from shared storage
        historical_data = data.get('historical_data', [])
        current_month_data = data.get('current_month_data', [])
        target_sales = data.get('target_sales')
        last_updated = data.get('last_updated', 'Unknown')
        
        # Create forecaster
        forecaster = SalesForecaster(historical_data)
        weekday_averages = forecaster.get_weekday_averages()
        
        # Generate forecast
        forecast_data = forecaster.forecast_month('JANUARY', target_sales)
        
        # Create visualizer
        viz = SalesVisualizer()
        
        # Display last updated time
        st.markdown(f"""
        <div style='color: #666; font-size: 0.9rem; margin-bottom: 1rem;'>
            Last updated: {last_updated}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # KPIs
        st.markdown("## 📈 Key Performance Indicators")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        today = datetime.now()
        today_sales = to_float(forecast_data.get('today_sales', 0), 0)
        total_projected = to_float(forecast_data.get('total_projected', 0), 0)
        gap = to_float(forecast_data.get('projected_vs_target', 0), 0) if target_sales else 0
        
        with col1:
            st.metric("Today", today.strftime("%d %b"))
        with col2:
            st.metric("Projected Today", f"AED {today_sales:,.0f}")
        with col3:
            st.metric("Monthly Projection", f"AED {total_projected:,.0f}")
        with col4:
            st.metric("Target", f"AED {target_sales:,.0f}" if target_sales else "-")
        with col5:
            color = "🟢" if gap >= 0 else "🔴"
            st.metric("Gap", f"{color} {gap:,.0f}" if target_sales else "-")
        
        st.markdown("---")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📉 Historical Sales Trend")
            try:
                chart1 = viz.create_historical_sales_chart(historical_data)
                st.plotly_chart(chart1, use_container_width=True)
            except Exception as e:
                st.warning(f"Could not display chart: {str(e)}")
        
        with col2:
            st.markdown("### 📊 Weekday Performance")
            try:
                chart2 = viz.create_weekday_chart(weekday_averages)
                st.plotly_chart(chart2, use_container_width=True)
            except Exception as e:
                st.warning(f"Could not display chart: {str(e)}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🔮 Monthly Forecast")
            try:
                chart3 = viz.create_forecast_chart(forecast_data)
                st.plotly_chart(chart3, use_container_width=True)
            except Exception as e:
                st.warning(f"Could not display chart: {str(e)}")
        
        with col2:
            if target_sales:
                st.markdown("### 🎯 Target vs Projection")
                try:
                    chart4 = viz.create_target_chart(forecast_data)
                    st.plotly_chart(chart4, use_container_width=True)
                except Exception as e:
                    st.warning(f"Could not display chart: {str(e)}")
            else:
                st.info("ℹ️ Set a target in the admin panel to see comparison")
        
        if current_month_data and len(current_month_data) > 0:
            st.markdown("### 📊 Actual vs Projected Sales")
            try:
                current_month = current_month_data[0]
                chart5 = viz.create_actual_vs_projected_chart(forecast_data, current_month)
                st.plotly_chart(chart5, use_container_width=True)
            except Exception as e:
                st.warning(f"Could not display chart: {str(e)}")
        
    except Exception as e:
        st.error(f"Error loading dashboard: {str(e)}")
        st.info("Please make sure data has been uploaded in the admin portal")

st.markdown("---")

# Footer
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📖 Documentation")
    st.markdown("[GitHub Admin Repo](https://github.com/adeelciit786-hue/saleanalysisadmin)")

with col2:
    st.markdown("### 🔧 Admin Panel")
    st.markdown("[Admin Interface](https://saleanalysisappadm.streamlit.app)")

with col3:
    st.markdown("### 📞 Support")
    st.markdown("📧 adeelciit786@gmail.com")

st.markdown("""
<div style='text-align: center; margin-top: 2rem; padding-top: 1rem; border-top: 2px solid #E0E7FF; color: #999;'>
    <p><strong>Champion Cleaners Sales Dashboard</strong> • Version 2.0.0 • January 2026</p>
    <p>💡 <em>Real-time sales intelligence powered by advanced forecasting</em></p>
</div>
""", unsafe_allow_html=True)
