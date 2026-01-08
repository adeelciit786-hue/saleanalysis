"""
Shared Storage Module
Handles persistent storage of dashboard data for both admin and viewer apps
"""

import json
import os
from pathlib import Path
from datetime import datetime

# Use a shared data file in the streamlit_apps directory
DATA_FILE = Path(__file__).parent / "dashboard_data.json"

def save_dashboard_data(historical_data, current_month_data, target_sales):
    """
    Save dashboard data to shared storage
    
    Args:
        historical_data: List of historical data dicts
        current_month_data: List of current month data dicts
        target_sales: Target sales value
    """
    try:
        data = {
            'historical_data': historical_data or [],
            'current_month_data': current_month_data or [],
            'target_sales': target_sales,
            'last_updated': datetime.now().isoformat()
        }
        
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        
        return True
    except Exception as e:
        print(f"Error saving dashboard data: {str(e)}")
        return False

def load_dashboard_data():
    """
    Load dashboard data from shared storage
    
    Returns:
        Dict with historical_data, current_month_data, target_sales or None
    """
    try:
        if DATA_FILE.exists():
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
            return data
        return None
    except Exception as e:
        print(f"Error loading dashboard data: {str(e)}")
        return None

def clear_dashboard_data():
    """Clear all shared data"""
    try:
        if DATA_FILE.exists():
            os.remove(DATA_FILE)
        return True
    except Exception as e:
        print(f"Error clearing dashboard data: {str(e)}")
        return False

def data_exists():
    """Check if dashboard data exists"""
    return DATA_FILE.exists()
