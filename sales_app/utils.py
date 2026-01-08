"""
Utility functions for data type safety
Ensures all numeric operations work correctly regardless of input types
"""

import numpy as np


def to_float(value, default=0.0):
    """
    Safely convert any value to float
    
    Args:
        value: Value to convert (can be str, int, float, numpy type, None, etc)
        default: Default value if conversion fails
    
    Returns:
        float: Converted value or default
    """
    if value is None or value == '':
        return default
    
    try:
        # Handle numpy types
        if isinstance(value, (np.integer, np.floating)):
            return float(value)
        
        # Handle regular types
        if isinstance(value, (int, float)):
            return float(value)
        
        # Handle strings
        if isinstance(value, str):
            val_str = value.strip()
            if val_str in ['-', 'nan', 'NAN', 'N/A', '']:
                return default
            return float(val_str)
        
        # Try generic conversion
        return float(value)
    
    except (ValueError, TypeError, AttributeError):
        return default


def to_float_list(values, default=0.0):
    """
    Convert a list/array of values to floats
    
    Args:
        values: List or array of values
        default: Default for each failed conversion
    
    Returns:
        list: List of floats
    """
    return [to_float(v, default) for v in values]


def ensure_numeric_array(array):
    """
    Convert array to numeric (float) type, handling all edge cases
    
    Args:
        array: Array-like object
    
    Returns:
        list: List of floats
    """
    if array is None:
        return []
    
    if isinstance(array, np.ndarray):
        return [to_float(v) for v in array]
    
    if isinstance(array, (list, tuple)):
        return [to_float(v) for v in array]
    
    # Try to convert to list
    try:
        return [to_float(v) for v in array]
    except:
        return []


def safe_sum(iterable, default=0.0):
    """
    Safely sum numeric values from iterable
    
    Args:
        iterable: Iterable of values
        default: Return value if iterable is empty
    
    Returns:
        float: Sum of all values
    """
    try:
        total = 0.0
        for val in iterable:
            total += to_float(val)
        return total
    except:
        return default


def safe_arithmetic(value1, value2, operation='add', default=0.0):
    """
    Safely perform arithmetic between two values
    
    Args:
        value1: First value
        value2: Second value
        operation: 'add', 'subtract', 'multiply', 'divide'
        default: Return value if operation fails
    
    Returns:
        float: Result of operation
    """
    try:
        v1 = to_float(value1)
        v2 = to_float(value2)
        
        if operation == 'add':
            return v1 + v2
        elif operation == 'subtract':
            return v1 - v2
        elif operation == 'multiply':
            return v1 * v2
        elif operation == 'divide':
            if v2 == 0:
                return default
            return v1 / v2
        else:
            return default
    
    except:
        return default
