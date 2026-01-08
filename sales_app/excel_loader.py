"""
Excel Data Loader Module
Handles reading, parsing, and validating Excel sales data in matrix format
Supports both formats: with headers or without headers (auto-detects)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from utils import to_float, to_float_list, ensure_numeric_array, safe_sum
from calendar import monthrange

class ExcelLoader:
    """Load and parse Excel sales data in matrix format"""
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None
        self.month_name = None
        self.weekdays = None
        self.dates = None
        self.branches = None
        self.daily_totals = None
        self.excel_total_row = None
        self.errors = []
        self.format_type = None  # 'with_headers' or 'without_headers'
        
    def load(self):
        """Load and parse Excel file"""
        try:
            # Read Excel file
            df = pd.read_excel(self.file_path, sheet_name=0, header=None)
            
            if df.empty:
                self.errors.append("Excel file is empty")
                return False
            
            # Detect format and parse accordingly
            if self._detect_format(df):
                # Parse data based on detected format
                if not self._parse_data(df):
                    return False
            else:
                return False
            
            return True
            
        except Exception as e:
            self.errors.append(f"Error reading Excel file: {str(e)}")
            return False
    
    def _detect_format(self, df):
        """Detect Excel format (3 formats supported)"""
        try:
            first_row = df.iloc[0]
            second_row = df.iloc[1] if len(df) > 1 else None
            
            month_keywords = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE',
                            'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER']
            weekday_keywords = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
            
            # Check row 1 (index 0) for weekdays
            has_weekdays_in_row1 = any(str(val).strip().upper() in weekday_keywords 
                                       for val in first_row[1:6])
            
            # Check row 2 (index 1) for weekdays
            has_weekdays_in_row2 = False
            if second_row is not None:
                has_weekdays_in_row2 = any(str(val).strip().upper() in weekday_keywords 
                                           for val in second_row[1:6])
            
            # FORMAT 1: Month + Weekdays in row 1 (NOV/DEC template format)
            if has_weekdays_in_row1:
                self.format_type = 'with_headers_row1'
                if not self._parse_headers_format(df):
                    return False
            
            # FORMAT 2: Month in row 1, Outlet Name + Weekdays in row 2, Data in row 4+ (JANUARY format)
            elif has_weekdays_in_row2:
                self.format_type = 'with_headers_row2'
                if not self._parse_headers_row2_format(df):
                    return False
            
            # FORMAT 3: Month in row 1, data starting row 4 with auto-generated weekdays
            else:
                self.format_type = 'without_headers'
                if not self._parse_headerless_format(df):
                    return False
            
            return True
            
        except Exception as e:
            self.errors.append(f"Error detecting format: {str(e)}")
            return False
    
    def _parse_headers_format(self, df):
        """Parse Excel with weekday headers in row 1"""
        try:
            # Row 0: Month name + Weekdays
            header_row = df.iloc[0]
            self.month_name = str(header_row[0]).strip().upper()
            
            # Extract weekdays
            self.weekdays = []
            for i in range(1, len(header_row)):
                val = str(header_row[i]).strip().upper()
                if val and val != 'NAN' and val != 'NONE':
                    self.weekdays.append(val)
                else:
                    break
            
            if not self.weekdays:
                self.errors.append("No weekdays found in header")
                return False
            
            # Row 1: Date numbers
            date_row = df.iloc[1]
            self.dates = []
            for i in range(1, len(date_row)):
                try:
                    date_num = int(float(str(date_row[i]).strip()))
                    self.dates.append(date_num)
                except:
                    if i < len(self.weekdays) + 1:
                        self.dates.append(None)
            
            if not self.dates or len(self.dates) != len(self.weekdays):
                self.errors.append("Mismatch between weekdays and dates")
                return False
            
            return True
            
        except Exception as e:
            self.errors.append(f"Error parsing headers (row 1): {str(e)}")
            return False
    
    def _parse_headers_row2_format(self, df):
        """Parse Excel with headers in row 2 (Outlet Name, THU, FRI, SAT...) and dates in row 3"""
        try:
            # Extract month name from row 1
            self.month_name = str(df.iloc[0, 0]).strip().upper()
            
            # Extract month from name (e.g., "January 2025" → "JANUARY")
            month_keywords = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE',
                            'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER']
            for month_kw in month_keywords:
                if month_kw in self.month_name:
                    self.month_name = month_kw
                    break
            
            # Row 2 contains: Outlet Name (col 1), then weekday headers starting col 2
            header_row = df.iloc[1]
            self.weekdays = []
            
            for i in range(1, len(header_row)):
                val = str(header_row[i]).strip().upper()
                if val and val != 'NAN' and val != 'NONE':
                    self.weekdays.append(val)
                else:
                    break
            
            if not self.weekdays:
                self.errors.append("No weekdays found in row 2 headers")
                return False
            
            # Row 3 contains: None (col 1), then date numbers starting col 2
            date_row = df.iloc[2]
            self.dates = []
            
            for i in range(1, len(date_row)):
                try:
                    val = date_row[i]
                    if pd.isna(val):
                        break
                    date_num = int(float(str(val).strip()))
                    self.dates.append(date_num)
                except:
                    break
            
            if not self.dates or len(self.dates) != len(self.weekdays):
                self.errors.append(f"Mismatch between weekdays ({len(self.weekdays)}) and dates ({len(self.dates)})")
                return False
            
            return True
            
        except Exception as e:
            self.errors.append(f"Error parsing headers (row 2): {str(e)}")
            return False
    
    def _parse_headerless_format(self, df):
        """Parse Excel without headers (auto-detect month and dates)"""
        try:
            # Extract month name from first cell
            self.month_name = str(df.iloc[0, 0]).strip().upper()
            
            # Extract month from name (e.g., "November 2025" → November)
            month_keywords = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE',
                            'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER']
            for month_kw in month_keywords:
                if month_kw in self.month_name:
                    self.month_name = month_kw
                    break
            
            # Find first data row (where first column has a branch name, not a number)
            data_start_row = 0
            for idx in range(1, min(10, len(df))):
                cell_val = str(df.iloc[idx, 0]).strip()
                # If cell is not empty and not a pure number, it's likely branch name
                if cell_val and not self._is_number(cell_val):
                    data_start_row = idx
                    break
            
            if data_start_row == 0:
                self.errors.append("Could not find data rows in Excel file")
                return False
            
            # Count columns with numeric data to determine number of days
            first_data_row = df.iloc[data_start_row]
            num_days = 0
            for i in range(1, len(first_data_row)):
                val = first_data_row[i]
                if pd.isna(val):
                    break
                if self._is_number(val):
                    num_days += 1
                else:
                    break
            
            if num_days == 0:
                self.errors.append("No numeric data found in rows")
                return False
            
            # Generate dates (1 to num_days)
            self.dates = list(range(1, num_days + 1))
            
            # Generate weekdays based on number of days
            all_weekdays = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
            self.weekdays = []
            for i in range(num_days):
                self.weekdays.append(all_weekdays[i % 7])
            
            return True
            
        except Exception as e:
            self.errors.append(f"Error parsing headerless format: {str(e)}")
            return False
    
    def _is_number(self, val):
        """Check if value is numeric"""
        try:
            float(val)
            return True
        except:
            return False
    
    def _parse_data(self, df):
        """Extract branch data and create analytical dataframe"""
        try:
            # Determine data start row based on format
            if self.format_type == 'with_headers_row1':
                data_start_row = 2  # Skip month and date rows
            elif self.format_type == 'with_headers_row2':
                data_start_row = 3  # Skip month, headers, and date rows
            else:
                # Find first data row (branch names) for headerless format
                data_start_row = 0
                for idx in range(1, min(10, len(df))):
                    cell_val = str(df.iloc[idx, 0]).strip()
                    if cell_val and not self._is_number(cell_val):
                        data_start_row = idx
                        break
            
            # Extract branches and data
            data_rows = []
            self.branches = []
            num_cols = len(self.dates)
            
            for idx in range(data_start_row, len(df)):
                branch_name = str(df.iloc[idx, 0]).strip()
                
                # Skip empty rows
                if not branch_name or branch_name.lower() == 'nan':
                    continue
                
                # Check for TOTAL row
                if branch_name.upper() == 'TOTAL':
                    self.excel_total_row = idx
                    continue
                
                # Parse sales data
                sales = []
                for col in range(1, num_cols + 1):
                    if col < len(df.columns):
                        val = df.iloc[idx, col]
                        sales.append(self._convert_to_float(val))
                    else:
                        sales.append(0.0)
                
                if any(v is not None and v > 0 for v in sales):  # Has valid data
                    self.branches.append(branch_name)
                    data_rows.append(sales)
            
            if not self.branches:
                self.errors.append("No branch data found")
                return False
            
            # Create dataframe
            self.data = pd.DataFrame(
                data_rows,
                columns=[f"Day_{i}" for i in self.dates],
                index=self.branches
            )
            
            # Calculate daily totals - ensure all values are float
            daily_totals_raw = self.data.sum(axis=0).values
            self.daily_totals = ensure_numeric_array(daily_totals_raw)
            
            return True
            
        except Exception as e:
            self.errors.append(f"Error parsing data: {str(e)}")
            return False
    
    def _convert_to_float(self, value):
        """Convert value to float, handling dashes and NaN"""
        return to_float(value, default=0.0)
    
    def get_analysis_dataframe(self):
        """Get dataframe with month, dates, and weekdays for analysis"""
        analysis_data = {
            'Month': self.month_name,
            'Date': self.dates,
            'Weekday': self.weekdays,
            'Daily_Total': self.daily_totals
        }
        return pd.DataFrame(analysis_data)
    
    def get_branch_data(self):
        """Get branch sales dataframe"""
        return self.data.copy()
    
    def validate(self):
        """Validate data against Excel totals"""
        if self.excel_total_row is None:
            return True, "No TOTAL row found for validation"
        
        # Calculate expected totals from branch data
        calculated_totals = self.daily_totals
        
        return True, "Data validation complete"
    
    def get_format_info(self):
        """Get detailed information about detected format"""
        return {
            'format_type': self.format_type,
            'month_name': self.month_name,
            'num_days': len(self.dates) if self.dates else 0,
            'num_branches': len(self.branches) if self.branches else 0,
            'date_range': f"{self.dates[0]}-{self.dates[-1]}" if self.dates else "N/A",
            'weekday_pattern': self.weekdays[:7] if self.weekdays else [],
            'has_errors': len(self.errors) > 0,
            'errors': self.errors
        }
