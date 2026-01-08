# Enterprise Sales Forecasting Dashboard

A professional web-based sales forecasting application built with Python, Flask, and Plotly. Designed for enterprise sales management with support for multi-branch operations.

## Features

✅ **Web-Based Excel Upload**
- Drag-and-drop file upload
- Support for historical data (November, December, etc.)
- Current month data import
- Automatic Excel format validation

✅ **Intelligent Data Processing**
- Auto-detection of month names, weekdays, dates
- Automatic branch identification
- TOTAL row detection and validation
- Dash (-) converted to 0
- Comprehensive error messages

✅ **Weekday-Based Forecasting**
- Calculates average sales per weekday from historical data
- Projects remaining days of current month
- Monday forecasts based on historical Mondays, etc.
- High accuracy due to consistent weekday patterns

✅ **Professional Visualizations**
- Historical daily sales trend chart
- Average sales by weekday (bar chart)
- Sales projection with past/today/future markers
- Cumulative vs target chart
- Interactive Plotly charts

✅ **KPI Dashboard**
- Today's projected sales
- Monthly projection total
- Target-based gap analysis
- Executive-level summaries

✅ **Enterprise Features**
- Monthly target management
- Month closure and archiving
- Role-based access (planned)
- Secure data handling

## Excel Format Requirements

Your Excel file must follow this exact structure:

```
ROW 1:  Month Name | MON | TUE | WED | THU | FRI | SAT | SUN
ROW 2:  (empty)    |  1  |  2  |  3  |  4  |  5  |  6  |  7
ROW 3+: Branch 1   | 1000| 1100| 950 | ...
        Branch 2   | 2000| 2100| 1950| ...
        ...
LAST:   TOTAL      | 3000| 3200| 2900| ...
```

### Key Requirements:
- Row 1: Month name + 7 weekdays (MON-SUN)
- Row 2: Date numbers (1-7, 8-14, 15-21, 22-28, etc.)
- Column A: Branch names
- Data cells: Daily sales (numeric, supports 2 decimals)
- Last row: "TOTAL" row with auto-calculated sums
- Use dash (-) for zero/no sales days

## Installation & Setup

### Prerequisites
- Python 3.8+ installed
- Windows/Mac/Linux
- 16MB disk space

### Step 1: Create Virtual Environment
```bash
cd "c:\Users\adeel\Sales projection"
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 2: Install Dependencies
```bash
cd sales_app
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
python app.py
```

The app will start on: **http://localhost:5000**

## Usage

### Upload Historical Data
1. Go to the home page
2. Upload Excel files for November and December (or any 2+ historical months)
3. System auto-validates format
4. See upload confirmation

### Upload Current Month
1. Upload the running month Excel file (e.g., January)
2. System detects current progress
3. Calculates remaining days

### Set Target (Optional)
1. Enter monthly sales target (e.g., 3,000,000)
2. Click "Set Target"
3. Dashboard shows projected vs target

### View Dashboard
1. Click "View Dashboard"
2. See:
   - KPI cards (Today's Sales, Monthly Projection, Target Gap)
   - Historical trend chart
   - Weekday performance analysis
   - Sales projection with trend lines
   - Target vs projection cumulative chart

## Project Structure

```
sales_app/
├── app.py                      # Main Flask application
├── excel_loader.py             # Excel parsing & validation
├── forecast.py                 # Sales forecasting logic
├── visualizer.py               # Chart generation
├── create_sample_excel.py      # Sample data generator
├── requirements.txt            # Python dependencies
├── static/
│   └── css/
│       └── style.css           # Professional styling
├── templates/
│   ├── index.html              # Upload page
│   └── dashboard.html          # Dashboard page
└── data/                       # Temporary data storage
```

## Forecasting Logic

### Algorithm
1. **Historical Analysis**: Analyzes past 2-3 months
2. **Weekday Grouping**: Groups sales by weekday (Monday, Tuesday, etc.)
3. **Average Calculation**: Computes average sales per weekday
4. **Projection**: Applies weekday averages to remaining days

### Example
```
Historical Data:
- Mondays (Nov, Dec): [120,000, 118,000] → Average: 119,000
- Tuesdays (Nov, Dec): [95,000, 98,000] → Average: 96,500
- ... (repeat for all 7 days)

Projection for January:
- Jan 1 (Monday) → 119,000
- Jan 2 (Tuesday) → 96,500
- Jan 8 (Monday) → 119,000
- ... (repeat pattern)
```

## Data Validation

The app validates:
- ✓ Excel file format (.xlsx, .xls)
- ✓ Header structure (month, weekdays, dates)
- ✓ Date-weekday alignment
- ✓ Numeric sales values
- ✓ TOTAL row presence
- ✓ Branch data non-empty

### Error Handling
- User-friendly error messages
- No Python tracebacks shown
- Guidance on format corrections
- File upload confirmation

## KPI Cards Explained

| KPI | Description |
|-----|-------------|
| **Today's Date** | Current date and day of week |
| **Projected Today** | Forecasted sales for today based on historical weekday average |
| **Monthly Projection** | Total projected sales for the entire month |
| **Monthly Target** | Admin-set sales goal for the month |
| **Target Gap** | Difference between projection and target (positive = exceeds target) |

## Charts Explained

### Chart 1: Historical Daily Sales Trend
- **Type**: Line chart
- **Data**: All historical days (Nov + Dec)
- **Y-Axis**: Daily total sales
- **X-Axis**: Date + weekday
- **Purpose**: Identify seasonal patterns and trends

### Chart 2: Average Sales by Weekday
- **Type**: Bar chart
- **Data**: Average per weekday across all historical months
- **Purpose**: Show which days consistently perform better
- **Labels**: Sales values on top of bars

### Chart 3: Sales Projection
- **Type**: Line chart with markers
- **Data**: Past (actual), Today (marker), Future (dashed)
- **Purpose**: Show forecast with daily precision
- **Features**: Vertical "Today" marker, target line

### Chart 4: Target vs Projection
- **Type**: Area + Line chart
- **Data**: Cumulative projected sales vs monthly target
- **Purpose**: Track progress toward monthly goal
- **Features**: Filled area under projection, dashed target line

## Month Closure Workflow

```
Current Month (Editable, Viewable)
↓
[Admin: Click "Close Month"]
↓
Closed Month (Locked, Archived, Used as Training Data)
↓
System auto-generates Next Month projection
↓
Uses last 3 closed months for forecasting
↓
Viewers see only projection, not raw data
```

## API Endpoints

### Upload
```
POST /upload
- Accepts: Excel file + month_type
- Returns: {success, message, month, stats}
```

### Dashboard
```
GET /dashboard
- Displays: KPI cards, 4 charts, analysis summary
```

### Set Target
```
POST /api/set-target
- Body: {month, target}
- Returns: {success, message}
```

### Close Month
```
POST /api/close-month
- Body: {month}
- Returns: {success, message}
```

### Data Summary
```
GET /api/data-summary
- Returns: Historical/current data, closed months, targets
```

## Customization

### Change Target Currency
In `templates/dashboard.html` and `templates/index.html`, replace "AED" with your currency code.

### Change Colors
Edit `:root` variables in `static/css/style.css`:
```css
--primary-color: #2E86AB;      /* Main blue */
--secondary-color: #A23B72;    /* Purple accents */
--success-color: #06A77D;      /* Green */
--warning-color: #F77F00;      /* Orange */
--danger-color: #E63946;       /* Red */
```

### Add More Branches
Excel format supports unlimited branches. Just add rows to your Excel file.

### Adjust Forecast Period
Modify `forecast.py` to use more/fewer historical months:
```python
# Current: uses all historical data
# Can be modified to use last N months only
```

## Troubleshooting

### Issue: "Port 5000 already in use"
```bash
# Use different port
python app.py --port 5001
```

### Issue: Excel file not accepted
- Check file is `.xlsx` or `.xls` format
- Verify row 1 has 8 columns (month + 7 days)
- Ensure row 2 has date numbers
- Check branch names in column A
- Verify TOTAL row exists

### Issue: No data appears in dashboard
- Ensure you uploaded at least 2 historical months
- Current month must be uploaded
- Check browser console (F12) for errors
- Clear browser cache and reload

### Issue: Forecasts look wrong
- Verify historical data is complete and accurate
- Check that TOTAL row matches sum of branches
- Ensure no blank cells in critical rows
- Validate weekday alignment with dates

## Performance Notes

- Dashboard loads charts on demand (may take 2-3 seconds)
- Supports up to 50 branches per month
- Excel parsing handles files up to 16MB
- In-memory data storage (data cleared on app restart)

## Security

- No authentication required (can be added)
- File uploads stored in temp folder (auto-cleaned)
- No external API calls or internet dependencies
- All processing local to server

## Future Enhancements

- [ ] User authentication & roles
- [ ] Data persistence (database)
- [ ] Export reports (PDF, Excel)
- [ ] Seasonal adjustment factors
- [ ] Multi-year forecasting
- [ ] Branch-level dashboards
- [ ] API for external integrations
- [ ] Advanced forecasting (ARIMA, Prophet)

## Support

For issues or questions:
1. Check error messages (usually self-explanatory)
2. Review Excel format against requirements
3. Check browser console (F12) for JavaScript errors
4. Review app logs in terminal

## License

Corporate Use - Proprietary

## Technical Stack

- **Backend**: Python 3.8+, Flask 3.1
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly 6.5
- **Frontend**: HTML5, CSS3, JavaScript ES6
- **Excel**: openpyxl 3.1
- **Server**: Flask development server (use Gunicorn for production)

## Version

**v1.0** - January 2026

---

**Happy Forecasting!** 📈
