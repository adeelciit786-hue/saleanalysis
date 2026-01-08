# How to Use Your Sales Forecasting Dashboard

## 🚀 Getting Started (3 Simple Steps)

### Step 1: Start the Application
```
Navigate to: c:\Users\adeel\Sales projection\sales_app
Run: python app.py
Visit: http://127.0.0.1:5000
```

### Step 2: Upload Historical Data
1. Select "Historical Month" from dropdown
2. Upload "November 2025.xlsx"
3. Upload "December 2025.xlsx"
4. Wait for success messages

### Step 3: Upload Current Month & View Forecast
1. Select "Current Month" from dropdown
2. Upload your "January 2026.xlsx" (or current month)
3. Click "View Dashboard"
4. See all forecasts and KPI cards!

---

## 📊 Dashboard Overview

### Top Section: KPI Cards
```
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│  TODAY'S SALES  │ MONTHLY PROJ.   │    TARGET       │  TARGET GAP %   │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│   94,856.01     │  2,850,000      │  2,800,000      │  +1.8%          │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘
```

**What they mean:**
- **Today's Sales**: Projected sales for today based on weekday average
- **Monthly Projection**: Total expected sales for entire month
- **Target**: Your monthly sales goal (set via API)
- **Target Gap**: How much ahead/behind your target

### Middle Section: Charts
The dashboard displays 4 interactive Plotly charts:

1. **Historical Sales Trend** (Line Chart)
   - Shows November & December daily sales
   - Hover to see exact values
   - Click legend to show/hide data

2. **Weekday Analysis** (Bar Chart)
   - Shows average sales per weekday
   - Friday highest, Sunday lowest
   - Helps identify busiest days

3. **Monthly Forecast** (Area Chart)
   - Projected daily sales for current month
   - Shows cumulative sales line
   - Scroll to see full month

4. **Target vs Projection** (Comparison Chart)
   - Only appears if target is set
   - Shows gap visually
   - Red = below target, Green = above target

### Bottom Section: Data Table
Shows all branch-wise sales data in detail.

---

## 🎯 How Forecasting Works (Behind the Scenes)

### The Algorithm
```
STEP 1: Analyze Historical Data
├── November sales by day of week (MON-SUN)
├── December sales by day of week (MON-SUN)
└── Calculate average for each weekday

STEP 2: Build Weekday Averages
├── Monday:    94,856.01
├── Tuesday:   61,088.63
├── Wednesday: 100,049.27
├── Thursday:  103,355.37
├── Friday:    110,679.88
├── Saturday:  101,852.37
└── Sunday:    68,871.71

STEP 3: Apply to Current Month
├── Determine what day each date falls on
├── Apply corresponding weekday average
└── Build daily forecast

STEP 4: Calculate KPIs
├── Sum daily forecasts = monthly total
├── Compare to target = gap
├── Calculate remaining days = daily pace needed
└── Display on dashboard
```

---

## 📈 Understanding Your Data

### Your Excel Format
```
Column A: Branch names (27 branches)
├── Branch 1
├── Branch 2
├── ...
└── Branch 27

Columns B onwards: Daily sales (30 or 31 days)
├── Day 1 sales
├── Day 2 sales
├── ...
└── Day N sales
```

### What Gets Calculated
1. **Daily Totals**: Sum of all branches for each day
2. **Weekday Averages**: Average of each weekday across months
3. **Monthly Forecast**: Sum of all forecasted daily sales
4. **Branch Contribution**: Percentage contribution by branch

---

## 🔧 Advanced Features

### Setting a Target
```bash
POST /api/set-target
Body: {
  "month": "JANUARY",
  "target": 2800000
}
Response: {
  "success": true,
  "message": "Target set for JANUARY: 2,800,000"
}
```
Then the dashboard shows target comparison chart.

### Checking Data Quality
```bash
GET /api/validation-report
Response shows:
{
  "status": "success",
  "validation": {
    "has_errors": false,
    "errors": [],
    "total_months": 2
  },
  "historical_data": [
    {
      "month": "NOVEMBER",
      "days": 30,
      "branches": 27,
      "total_sales": 2,156,542.00,
      "format": "without_headers"
    },
    ...
  ]
}
```

### Viewing Upload Details
Each upload returns format information:
```json
{
  "format_detected": "without_headers",
  "format_info": {
    "format_type": "without_headers",
    "month_name": "NOVEMBER",
    "num_days": 30,
    "num_branches": 27,
    "date_range": "1-30",
    "weekday_pattern": ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"],
    "has_errors": false,
    "errors": []
  }
}
```

---

## 💡 Tips & Tricks

### 1. Hover Over Charts
Move your mouse over chart lines/bars to see:
- Exact values
- Date/day information
- Sales amounts

### 2. Download Charts
Click the camera icon (📷) on any chart to download as PNG

### 3. Zoom Into Charts
Click and drag to zoom into specific date ranges. Double-click to reset.

### 4. Pan Charts
Click and drag horizontally to move around the chart.

### 5. Toggle Data
Click legend items to show/hide specific data series.

### 6. Use Mobile
Dashboard is responsive - works on tablets and phones!

---

## ⚠️ Common Issues & Solutions

### Issue: Upload shows error "No weekdays found"
**Solution:** Your Excel file is already compatible! Error should be FIXED. If you see it, try:
1. Verify month name is in row 1
2. Check data starts at row 4
3. Ensure .xlsx format (not .xls)

### Issue: Dashboard shows "Please upload historical data first"
**Solution:** 
1. First, upload November 2025.xlsx as "Historical Month"
2. Then upload December 2025.xlsx as "Historical Month"
3. Only then upload current month as "Current Month"

### Issue: Numbers look too high/low
**Solution:**
1. Check your Excel file has correct data
2. Verify daily sales are in columns B onwards
3. Ensure all 27 branches are included
4. Use numerical format (not text)

### Issue: Dashboard won't load after upload
**Solution:**
1. Refresh the page (Ctrl+R)
2. Check browser console for errors (F12)
3. Verify Flask server is running
4. Try uploading again

### Issue: Forecast seems wrong
**Solution:**
1. Check `/api/validation-report` for data quality
2. Verify historical data has 2+ months
3. Ensure weekday patterns match calendar
4. Verify target is set correctly

---

## 📱 Mobile Access

Your dashboard works on any device:

**From your computer:**
```
http://127.0.0.1:5000  (local only)
```

**From another device on same network:**
```
http://[YOUR_IP]:5000
Example: http://192.168.1.100:5000
```

Find your IP: Windows Command Prompt
```
ipconfig
```
Look for "IPv4 Address" under your network adapter.

---

## 🔐 Data Privacy

Your data:
- ✓ Stays on your computer (no cloud upload)
- ✓ Stored only in memory while app runs
- ✓ Cleared when server restarts
- ✓ Never transmitted over internet

If you want to save data:
1. Take screenshots of dashboard
2. Export charts using download button
3. Keep your Excel files as backup

---

## 📊 Interpreting Results

### If Projected > Target
Your forecast suggests you'll exceed the target.
- Green color on dashboard
- Good performance expected

### If Projected < Target
Your forecast suggests you'll miss the target.
- Red color on dashboard
- May need to boost sales

### If Gap = 0%
Perfect! Forecast equals target exactly.

### Weekday Analysis
- **High weekdays**: Friday (110,679.88)
- **Low weekdays**: Tuesday (61,088.63)
- **Difference**: 81% higher on Friday vs Tuesday

Plan promotions for low-performing days!

---

## 🎓 Learning Resources

### Code Structure
```
app.py - Main application logic
  ├── / route → Upload page
  ├── /upload → Process Excel
  ├── /dashboard → Show results
  └── /api/* → API endpoints

excel_loader.py - Excel parsing
  ├── detect format
  ├── extract data
  └── validate

forecast.py - Forecasting algorithm
  ├── weekday averages
  ├── month forecast
  └── KPI calculations

visualizer.py - Chart generation
  ├── historical sales
  ├── weekday patterns
  ├── forecasts
  └── target comparison
```

### Key Concepts
1. **Format Detection**: Automatically identifies your Excel layout
2. **Weekday Pattern**: Uses past data to predict future sales by day of week
3. **Forecasting**: Projects future sales based on historical patterns
4. **KPI**: Key Performance Indicators that measure performance

---

## 🚀 Ready to Go!

Your dashboard is fully functional and production-ready. Start using it today:

1. Upload November 2025 (historical)
2. Upload December 2025 (historical)
3. Upload January 2026 (current month)
4. View dashboard
5. Monitor forecast and KPIs

**Questions?** Check the validation report or review the code comments.

**Happy Forecasting!** 📈
