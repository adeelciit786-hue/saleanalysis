"""
Sales Forecasting Dashboard Application
Main Flask application for enterprise sales forecasting
"""

from flask import Flask, render_template, request, jsonify, send_file, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json
from datetime import datetime, timedelta
from functools import wraps
from excel_loader import ExcelLoader
from forecast import SalesForecaster
from visualizer import SalesVisualizer
from utils import to_float, ensure_numeric_array, safe_sum
import pandas as pd

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'data')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload
app.config['SECRET_KEY'] = 'champion-cleaners-sales-dashboard-2026-secret'  # Change this in production!
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)  # Session expires after 24 hours

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Admin credentials (in production, use a proper database)
ADMIN_CREDENTIALS = {
    'admin': generate_password_hash('admin123')
}

# Store uploaded data in memory for demo
UPLOADED_DATA = {}
HISTORICAL_DATA = []
CLOSED_MONTHS = []
TARGET_SALES = {}

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login page"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            return render_template('login.html', error='Please enter both username and password')
        
        # Check credentials
        if username in ADMIN_CREDENTIALS and check_password_hash(ADMIN_CREDENTIALS[username], password):
            session.permanent = True
            session['user'] = username
            session['login_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"✓ Admin '{username}' logged in at {session['login_time']}")
            return redirect(url_for('index'))
        else:
            print(f"✗ Failed login attempt with username: {username}")
            return render_template('login.html', error='Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Admin logout"""
    username = session.get('user', 'Unknown')
    session.clear()
    print(f"✓ Admin '{username}' logged out")
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    """Main upload page"""
    return render_template('index.html', username=session.get('user', 'Admin'))

@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    """Handle Excel file upload"""
    
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file provided'}), 400
    
    file = request.files['file']
    month_type = request.form.get('month_type', 'current')
    
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400
    
    if not file.filename.endswith(('.xlsx', '.xls')):
        return jsonify({'success': False, 'error': 'Please upload an Excel file (.xlsx or .xls)'}), 400
    
    try:
        # Save uploaded file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        # Load and parse Excel
        loader = ExcelLoader(filepath)
        
        if not loader.load():
            error_msg = ' | '.join(loader.errors) if loader.errors else 'Failed to load Excel file'
            # Clean up
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'success': False, 'error': error_msg}), 400
        
        # Validate data
        if not loader.branches:
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'success': False, 'error': 'No branches found in Excel file'}), 400
        
        if not loader.dates or len(loader.dates) == 0:
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'success': False, 'error': 'No date data found in Excel file'}), 400
        
        if len(loader.weekdays) != len(loader.dates):
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'success': False, 'error': 'Mismatch between weekdays and dates'}), 400
        
        # Process data
        month_key = loader.month_name.upper()
        
        # Create format description
        format_desc = {
            'with_headers_row1': 'Format 1: Headers in Row 1',
            'with_headers_row2': 'Format 2: Headers in Row 2 (Outlet Name + Weekdays)',
            'without_headers': 'Format 3: No Headers (Auto-generated weekdays)'
        }
        
        data_dict = {
            'month': month_key,
            'dates': loader.dates,
            'weekdays': loader.weekdays,
            'totals': ensure_numeric_array(loader.daily_totals),
            'branches': loader.branches,
            'branch_data': loader.data.to_dict(),
            'format_type': loader.format_type,
            'format_description': format_desc.get(loader.format_type, 'Unknown'),
            'timestamp': datetime.now().isoformat()
        }
        
        # Store data
        if month_type == 'historical':
            # Check if already uploaded
            if any(d['month'] == month_key for d in HISTORICAL_DATA):
                if os.path.exists(filepath):
                    os.remove(filepath)
                return jsonify({'success': False, 'error': f'{month_key} already uploaded. Remove it first.'}), 400
            
            HISTORICAL_DATA.append(data_dict)
            message = f"Historical data for {month_key} uploaded successfully"
        else:
            UPLOADED_DATA[month_key] = data_dict
            message = f"Current month data ({month_key}) uploaded successfully"
        
        # Clean up uploaded file
        if os.path.exists(filepath):
            os.remove(filepath)
        
        return jsonify({
            'success': True,
            'message': message,
            'month': month_key,
            'total_branches': len(loader.branches),
            'total_days': len(loader.dates),
            'format_detected': loader.format_type,
            'format_description': data_dict['format_description'],
            'format_info': loader.get_format_info()
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': f'Error processing file: {str(e)}'}), 500

@app.route('/dashboard')
def dashboard():
    """Display forecasting dashboard"""
    
    if not HISTORICAL_DATA:
        return render_template('dashboard.html', 
                             error='Please upload historical data (November and December) first',
                             has_data=False)
    
    current_month = None
    for month_data in UPLOADED_DATA.values():
        current_month = month_data
        break
    
    try:
        # Initialize forecaster with historical data
        forecaster = SalesForecaster(HISTORICAL_DATA)
        weekday_averages = forecaster.get_weekday_averages()
        
        # Get target if available - ensure it's numeric
        current_month_name = current_month['month'] if current_month else 'JANUARY'
        target = to_float(TARGET_SALES.get(current_month_name), default=None) if TARGET_SALES.get(current_month_name) else None
        
        # Generate forecast for running month - with detailed error logging
        try:
            forecast_data = forecaster.forecast_month(current_month_name, target)
        except TypeError as type_err:
            # Catch type errors specifically for "int + str" debug
            error_msg = f"TypeError in forecast_month: {str(type_err)}\nContext: month={current_month_name}, target={target} (type: {type(target).__name__ if target is not None else 'None'})"
            print(f"ERROR DETAIL: {error_msg}")
            import traceback
            traceback.print_exc()
            raise Exception(error_msg) from type_err
        
        # Generate visualizations
        viz = SalesVisualizer()
        
        chart1 = viz.create_historical_sales_chart(HISTORICAL_DATA)
        chart2 = viz.create_weekday_chart(weekday_averages)
        chart3 = viz.create_forecast_chart(forecast_data)
        chart4 = viz.create_target_chart(forecast_data) if target else None
        
        # Create actual vs projected chart if current month data exists
        chart5 = None
        if current_month and current_month.get('dates') and current_month.get('totals'):
            chart5 = viz.create_actual_vs_projected_chart(forecast_data, current_month)
        
        # Convert charts to HTML
        chart1_html = chart1.to_html(full_html=False, include_plotlyjs='cdn') if chart1 else ''
        chart2_html = chart2.to_html(full_html=False, include_plotlyjs=False) if chart2 else ''
        chart3_html = chart3.to_html(full_html=False, include_plotlyjs=False) if chart3 else ''
        chart4_html = chart4.to_html(full_html=False, include_plotlyjs=False) if chart4 else ''
        chart5_html = chart5.to_html(full_html=False, include_plotlyjs=False) if chart5 else ''
        
        # Calculate KPIs - ensure all are floats
        today = datetime.now()
        today_sales = to_float(forecast_data['today_sales'], default=0.0)
        total_projected = to_float(forecast_data['total_projected'], default=0.0)
        gap = to_float(forecast_data.get('projected_vs_target', 0), default=0.0)
        
        kpis = {
            'today_date': f"{today.strftime('%A, %B %d, %Y')}",
            'today_sales': f"{today_sales:,.0f}",
            'projected_total': f"{total_projected:,.0f}",
            'target': f"{to_float(target, 0.0):,.0f}" if target else 'No Target Set',
            'gap': f"{gap:,.0f}" if target else '-',
            'gap_percent': f"{to_float(forecast_data.get('target_gap_percent', 0), 0.0):.1f}%" if target else '-'
        }
        
        return render_template('dashboard.html',
                             chart1=chart1_html,
                             chart2=chart2_html,
                             chart3=chart3_html,
                             chart4=chart4_html,
                             chart5=chart5_html,
                             kpis=kpis,
                             has_data=True,
                             current_month=current_month_name)
    
    except Exception as e:
        # Print detailed error info for debugging
        print(f"\n{'='*60}")
        print(f"DASHBOARD ERROR: {str(e)}")
        print(f"Error Type: {type(e).__name__}")
        print(f"{'='*60}")
        import traceback
        traceback.print_exc()
        print(f"{'='*60}\n")
        
        return render_template('dashboard.html',
                             error=f'Error generating forecast: {str(e)}',
                             has_data=False)

@app.route('/viewer')
def viewer():
    """Display read-only viewer dashboard for management"""
    
    try:
        # Check if historical data exists
        if not HISTORICAL_DATA:
            print("VIEWER: No historical data available")
            return render_template('viewer.html', has_data=False)
        
        print(f"VIEWER: Loading with {len(HISTORICAL_DATA)} historical records")
        
        current_month = None
        for month_data in UPLOADED_DATA.values():
            current_month = month_data
            break
        
        # Initialize forecaster with historical data
        forecaster = SalesForecaster(HISTORICAL_DATA)
        weekday_averages = forecaster.get_weekday_averages()
        
        # Get target if available
        current_month_name = current_month['month'] if current_month else 'JANUARY'
        target = to_float(TARGET_SALES.get(current_month_name), default=None) if TARGET_SALES.get(current_month_name) else None
        
        # Generate forecast for running month
        forecast_data = forecaster.forecast_month(current_month_name, target)
        
        # Generate visualizations
        viz = SalesVisualizer()
        
        chart1 = viz.create_historical_sales_chart(HISTORICAL_DATA)
        chart2 = viz.create_weekday_chart(weekday_averages)
        chart3 = viz.create_forecast_chart(forecast_data)
        chart4 = viz.create_target_chart(forecast_data) if target else None
        
        # Create actual vs projected chart if current month data exists
        chart5 = None
        if current_month and current_month.get('dates') and current_month.get('totals'):
            chart5 = viz.create_actual_vs_projected_chart(forecast_data, current_month)
        
        # Convert charts to HTML
        chart1_html = chart1.to_html(full_html=False, include_plotlyjs='cdn') if chart1 else ''
        chart2_html = chart2.to_html(full_html=False, include_plotlyjs=False) if chart2 else ''
        chart3_html = chart3.to_html(full_html=False, include_plotlyjs=False) if chart3 else ''
        chart4_html = chart4.to_html(full_html=False, include_plotlyjs=False) if chart4 else ''
        chart5_html = chart5.to_html(full_html=False, include_plotlyjs=False) if chart5 else ''
        
        # Calculate KPIs
        today = datetime.now()
        today_sales = to_float(forecast_data['today_sales'], default=0.0)
        total_projected = to_float(forecast_data['total_projected'], default=0.0)
        gap = to_float(forecast_data.get('projected_vs_target', 0), default=0.0)
        
        kpis = {
            'today_date': f"{today.strftime('%A, %B %d, %Y')}",
            'today_sales': f"{today_sales:,.0f}",
            'projected_total': f"{total_projected:,.0f}",
            'target': f"{to_float(target, 0.0):,.0f}" if target else 'No Target Set',
            'gap': f"{gap:,.0f}" if target else '-',
            'gap_percent': f"{to_float(forecast_data.get('target_gap_percent', 0), 0.0):.1f}%" if target else '-'
        }
        
        # Prepare data summary for viewer - with safe error handling
        try:
            if HISTORICAL_DATA and len(HISTORICAL_DATA) > 0:
                first_date = HISTORICAL_DATA[0].get('date')
                last_date = HISTORICAL_DATA[-1].get('date')
                if first_date and last_date:
                    date_range = f"{first_date.strftime('%b %d, %Y')} - {last_date.strftime('%b %d, %Y')}"
                else:
                    date_range = "Data Available"
            else:
                date_range = "N/A"
                
            branches = ', '.join(set(d.get('branch', 'Main') for d in HISTORICAL_DATA if 'branch' in d))
            if not branches:
                branches = 'All Branches'
        except Exception as summary_err:
            print(f"VIEWER: Error preparing data summary: {summary_err}")
            date_range = "Data Available"
            branches = "All Branches"
        
        data_summary = {
            'historical_months': len(CLOSED_MONTHS) if CLOSED_MONTHS else 2,
            'date_range': date_range,
            'branches': branches if branches else 'All Branches',
            'current_month_status': f"{current_month_name} - {len(current_month.get('dates', []))} days logged" if current_month else "Not Started"
        }
        
        print("VIEWER: Successfully generated dashboard with data")
        return render_template('viewer.html',
                             chart1=chart1_html,
                             chart2=chart2_html,
                             chart3=chart3_html,
                             chart4=chart4_html,
                             chart5=chart5_html,
                             kpis=kpis,
                             data_summary=data_summary,
                             has_data=True,
                             current_month=current_month_name)
    
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"VIEWER ERROR: {str(e)}")
        print(f"Error Type: {type(e).__name__}")
        print(f"{'='*60}")
        import traceback
        traceback.print_exc()
        
        return render_template('viewer.html',
                             error=f'Error loading dashboard: {str(e)}',
                             has_data=False)

@app.route('/api/set-target', methods=['POST'])
@login_required
def set_target():
    """Set monthly sales target"""
    try:
        data = request.get_json()
        month = data.get('month', '').upper()
        target = float(data.get('target', 0))
        
        if not month or target <= 0:
            return jsonify({'success': False, 'error': 'Invalid month or target'}), 400
        
        TARGET_SALES[month] = target
        return jsonify({'success': True, 'message': f'Target set for {month}: {target:,.0f}'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/close-month', methods=['POST'])
@login_required
def close_month():
    """Mark a month as closed"""
    try:
        data = request.get_json()
        month = data.get('month', '').upper()
        
        if not month:
            return jsonify({'success': False, 'error': 'Invalid month'}), 400
        
        if month in CLOSED_MONTHS:
            return jsonify({'success': False, 'error': f'{month} is already closed'}), 400
        
        CLOSED_MONTHS.append(month)
        return jsonify({'success': True, 'message': f'{month} closed successfully'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/data-summary')
def data_summary():
    """Get summary of uploaded data"""
    summary = {
        'historical': [{'month': d['month'], 'days': len(d['dates']), 'branches': len(d['branches'])} 
                       for d in HISTORICAL_DATA],
        'current': [],
        'closed': CLOSED_MONTHS,
        'targets': TARGET_SALES
    }
    
    for month, data in UPLOADED_DATA.items():
        summary['current'].append({
            'month': month,
            'days': len(data['dates']),
            'branches': len(data['branches'])
        })
    
    return jsonify(summary)

@app.route('/api/remove-historical', methods=['POST'])
@login_required
def remove_historical():
    """Remove a historical month from uploaded data"""
    try:
        data = request.get_json()
        month = data.get('month', '').upper()
        
        if not month:
            return jsonify({'success': False, 'error': 'Invalid month'}), 400
        
        global HISTORICAL_DATA
        original_count = len(HISTORICAL_DATA)
        HISTORICAL_DATA = [d for d in HISTORICAL_DATA if d['month'] != month]
        
        if len(HISTORICAL_DATA) == original_count:
            return jsonify({'success': False, 'error': f'{month} not found in uploaded data'}), 400
        
        return jsonify({'success': True, 'message': f'{month} removed successfully', 'remaining': len(HISTORICAL_DATA)})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/remove-current', methods=['POST'])
@login_required
def remove_current():
    """Remove current month data"""
    try:
        data = request.get_json()
        month = data.get('month', '').upper()
        
        if not month:
            return jsonify({'success': False, 'error': 'Invalid month'}), 400
        
        global UPLOADED_DATA
        if month not in UPLOADED_DATA:
            return jsonify({'success': False, 'error': f'{month} not found in uploaded data'}), 400
        
        del UPLOADED_DATA[month]
        return jsonify({'success': True, 'message': f'{month} removed successfully'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/validation-report')
def validation_report():
    """Get validation report for uploaded data"""
    if not HISTORICAL_DATA:
        return jsonify({
            'status': 'warning',
            'message': 'No historical data uploaded',
            'historical_data': [],
            'current_data': []
        })
    
    try:
        forecaster = SalesForecaster(HISTORICAL_DATA)
        
        report = {
            'status': 'success' if forecaster.has_sufficient_data() else 'warning',
            'validation': forecaster.get_validation_report(),
            'historical_data': [
                {
                    'month': d['month'],
                    'days': len(d['dates']),
                    'branches': len(d['branches']),
                    'total_sales': safe_sum(d['totals']),
                    'format': d.get('format_type', 'unknown')
                }
                for d in HISTORICAL_DATA
            ],
            'current_data': [
                {
                    'month': m,
                    'days': len(d['dates']),
                    'branches': len(d['branches']),
                    'total_sales': safe_sum(d['totals']),
                    'format': d.get('format_type', 'unknown')
                }
                for m, d in UPLOADED_DATA.items()
            ]
        }
        
        return jsonify(report)
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'validation': []
        }), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'running', 'app': 'Sales Forecasting Dashboard'})

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Page not found'}), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
