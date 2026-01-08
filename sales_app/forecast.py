"""
Sales Forecasting Module
Generates forecasts based on weekday-wise averages
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import calendar
from utils import to_float, safe_sum, safe_arithmetic

class SalesForecaster:
    """Generate sales forecasts based on historical data"""
    
    def __init__(self, historical_data_list):
        """
        Initialize with list of historical data dicts
        Each dict contains: {'month': 'JANUARY', 'dates': [1,2,...], 'weekdays': [...], 'totals': [...]}
        """
        self.historical_data = historical_data_list
        self.weekday_averages = {}
        self.weekday_map = {
            'MON': 0, 'TUE': 1, 'WED': 2, 'THU': 3,
            'FRI': 4, 'SAT': 5, 'SUN': 6
        }
        self.errors = []
        self.validation_results = {}
        self._calculate_weekday_averages()
        self._validate_historical_data()
    
    def _validate_historical_data(self):
        """Validate that historical data is properly formatted"""
        for idx, data in enumerate(self.historical_data):
            try:
                # Check required fields
                if 'month' not in data:
                    self.errors.append(f"Historical data {idx}: Missing 'month' field")
                if 'totals' not in data:
                    self.errors.append(f"Historical data {idx}: Missing 'totals' field")
                if 'weekdays' not in data:
                    self.errors.append(f"Historical data {idx}: Missing 'weekdays' field")
                
                # Check data integrity
                if len(data.get('totals', [])) != len(data.get('weekdays', [])):
                    self.errors.append(f"Historical data {idx}: Totals-weekdays mismatch")
                    
                self.validation_results[data.get('month', f'Unknown{idx}')] = 'valid' if not self.errors else 'invalid'
            except Exception as e:
                self.errors.append(f"Historical data {idx}: Validation error - {str(e)}")
    
    
    def _calculate_weekday_averages(self):
        """Calculate average sales for each weekday from historical data"""
        weekday_sales = {i: [] for i in range(7)}
        
        for data in self.historical_data:
            for weekday, daily_total in zip(data['weekdays'], data['totals']):
                weekday_idx = self.weekday_map.get(weekday.upper(), -1)
                # Ensure daily_total is numeric
                total_value = to_float(daily_total, default=0.0)
                
                if weekday_idx >= 0 and total_value > 0:
                    weekday_sales[weekday_idx].append(total_value)
        
        # Calculate averages - ensure they are python floats, not numpy types
        for idx in range(7):
            if weekday_sales[idx]:
                self.weekday_averages[idx] = float(np.mean(weekday_sales[idx]))
            else:
                self.weekday_averages[idx] = 0.0
    
    def forecast_month(self, month_name, target_sales=None):
        """
        Generate full month forecast
        
        Args:
            month_name: Name of month (e.g., 'JANUARY')
            target_sales: Optional monthly target
        
        Returns:
            dict with forecast data
        """
        # Get month number and year
        today = datetime.now()
        months = {
            'JANUARY': 1, 'FEBRUARY': 2, 'MARCH': 3, 'APRIL': 4,
            'MAY': 5, 'JUNE': 6, 'JULY': 7, 'AUGUST': 8,
            'SEPTEMBER': 9, 'OCTOBER': 10, 'NOVEMBER': 11, 'DECEMBER': 12
        }
        
        month_num = months.get(month_name.upper(), today.month)
        year = today.year
        
        # Adjust year if month is in past
        if month_num < today.month and month_num != today.month:
            year = today.year + 1
        
        # Get days in month
        days_in_month = calendar.monthrange(year, month_num)[1]
        
        forecast = []
        running_total = 0.0
        
        for day in range(1, days_in_month + 1):
            date_obj = datetime(year, month_num, day)
            weekday_idx = date_obj.weekday()
            
            # Map Python weekday (0=Monday) to our system and ensure numeric
            projected_sales = to_float(self.weekday_averages.get(weekday_idx, 0), default=0.0)
            
            # Ensure projected_sales is definitely a float
            if not isinstance(projected_sales, float):
                projected_sales = float(projected_sales) if projected_sales is not None else 0.0
            
            is_today = (date_obj.date() == today.date())
            is_past = (date_obj.date() < today.date())
            
            # Ensure running_total is definitely a float before arithmetic
            if not isinstance(running_total, float):
                running_total = float(running_total)
            
            running_total = safe_arithmetic(running_total, projected_sales, 'add')
            
            # Validate result type
            if not isinstance(running_total, float):
                print(f"ERROR: running_total became {type(running_total).__name__}: {running_total}")
                running_total = float(running_total)
            
            forecast.append({
                'date': day,
                'weekday_idx': weekday_idx,
                'weekday': self._get_weekday_name(weekday_idx),
                'projected_sales': projected_sales,
                'cumulative_sales': running_total,
                'is_today': is_today,
                'is_past': is_past
            })
        
        # Calculate metrics
        total_projected = safe_sum(f['projected_sales'] for f in forecast)
        days_remaining = sum(1 for f in forecast if f['date'] >= today.day)
        
        result = {
            'month': month_name,
            'year': year,
            'forecast': forecast,
            'total_projected': total_projected,
            'days_remaining': days_remaining,
            'today_date': today.day,
            'today_sales': self._get_today_sales(forecast),
            'target_sales': to_float(target_sales, default=None) if target_sales else None,
        }
        
        # Add target metrics
        if result['target_sales'] is not None and result['target_sales'] > 0:
            result['projected_vs_target'] = safe_arithmetic(total_projected, result['target_sales'], 'subtract')
            result['target_gap_percent'] = safe_arithmetic(safe_arithmetic(total_projected, result['target_sales'], 'subtract'), result['target_sales'], 'divide') * 100 if result['target_sales'] > 0 else 0
            
            # Calculate required daily sales
            past_sales = safe_sum(f['projected_sales'] for f in forecast if f['date'] < today.day)
            remaining_target = safe_arithmetic(result['target_sales'], past_sales, 'subtract')
            
            if days_remaining > 0:
                result['required_daily_sales'] = safe_arithmetic(remaining_target, days_remaining, 'divide') if remaining_target > 0 else 0
            else:
                result['required_daily_sales'] = 0
        
        return result
    
    def _get_today_sales(self, forecast):
        """Get today's projected sales"""
        today = datetime.now().day
        for f in forecast:
            if f['date'] == today:
                return to_float(f['projected_sales'], default=0.0)
        return 0.0
    
    def _get_weekday_name(self, weekday_idx):
        """Convert weekday index to name"""
        names = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
        return names[weekday_idx] if 0 <= weekday_idx < 7 else 'UNK'
    
    def get_weekday_averages(self):
        """Get average sales by weekday"""
        return {
            'MON': self.weekday_averages.get(0, 0),
            'TUE': self.weekday_averages.get(1, 0),
            'WED': self.weekday_averages.get(2, 0),
            'THU': self.weekday_averages.get(3, 0),
            'FRI': self.weekday_averages.get(4, 0),
            'SAT': self.weekday_averages.get(5, 0),
            'SUN': self.weekday_averages.get(6, 0),
        }
    
    def get_validation_report(self):
        """Get detailed validation report"""
        return {
            'has_errors': len(self.errors) > 0,
            'errors': self.errors,
            'validation_results': self.validation_results,
            'total_months': len(self.historical_data),
            'weekday_data_quality': {
                'MON': len([v for k, v in enumerate(self.weekday_averages.items()) if k == 0 and v[1] > 0]),
                'all_weekdays_covered': all(self.weekday_averages.get(i, 0) > 0 for i in range(7))
            }
        }
    
    def has_sufficient_data(self):
        """Check if forecaster has sufficient historical data"""
        return len(self.historical_data) >= 2 and len(self.errors) == 0
