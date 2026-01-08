# Excel Format Guide - 3 Formats Supported

**All 3 formats are now fully supported and auto-detected!**

---

## Format 1: Headers in Row 1

### When to Use
- Template format
- Month + weekdays in single row
- Dates in second row

### File Structure
```
Row 1: JANUARY       | MON    | TUE    | WED    | THU    | FRI    | SAT    | SUN   
Row 2: (empty)       | 1      | 2      | 3      | 4      | 5      | 6      | 7     
Row 3: (empty)       | -      | -      | -      | -      | -      | -      | -     
Row 4: AL BARRARI    | 456.15 | 2339.9 | 1443.9 | 604.91 | 2574.9 | (none) | (none)
Row 5: AL FORSAN     | 1387.8 | 809.49 | 1041.2 | 451    | 567.16 | (none) | (none)
...
```

### Requirements
- Row 1: Month name in column A
- Row 1: Weekday names (MON, TUE, WED, etc.) in columns B onwards
- Row 2: Empty or date numbers
- Row 3: Empty
- Row 4+: Branch names in column A, sales data in columns B onwards

### Detection
```
System sees weekdays in row 1
→ Automatically selects Format 1
→ Parses headers from row 1
→ Extracts data from row 4
```

### Status
✅ **Fully Supported**

---

## Format 2: Headers in Row 2 ⭐ (Your January 2026 Format)

### When to Use
- Your current format (January 2026)
- Outlet/Branch names + weekdays in row 2
- Dates in row 3
- **This is the format you're using!**

### File Structure
```
Row 1: January 2025
Row 2: Outlet Name  | THU    | FRI    | SAT    | SUN   | MON    | TUE    | WED   
Row 3: (empty)      | 1      | 2      | 3      | 4     | 5      | 6      | 7     
Row 4: AL BARRARI   | 456.15 | 2339.9 | 1443.9 | 604.9 | 2574.9 | (none) | (none)
Row 5: AL FORSAN    | 1387.8 | 809.49 | 1041.2 | 451   | 567.16 | (none) | (none)
Row 6: AL SEEF      | 543.07 | 1315.3 | 595.11 | 1117  | 661.12 | (none) | (none)
...
Row 32: TOTAL       | ...    | ...    | ...    | ...   | ...    | ...    | ...
```

### Requirements
- Row 1: Month name with year (e.g., "January 2025")
- Row 2: "Outlet Name" or "Branch Name" in column A
- Row 2: Weekday names (THU, FRI, SAT, SUN, MON, TUE, WED) in columns B onwards
- Row 3: Date numbers (1, 2, 3... 31)
- Row 4+: Branch/Outlet names in column A, sales data in columns B onwards
- Optional: Last row can be "TOTAL" (will be skipped)

### Key Features
- Supports partial months (only columns with data are processed)
- Handles NaN/None values gracefully
- Automatically detects number of days from column count
- Skips TOTAL row if present

### Detection
```
System sees weekdays in row 2 (not row 1)
→ Automatically selects Format 2
→ Parses month from row 1
→ Extracts headers from row 2
→ Extracts dates from row 3
→ Parses data from row 4
```

### Example: Your January File
```
✅ Row 1: January 2025
✅ Row 2: Outlet Name | THU | FRI | SAT | SUN | MON | TUE | WED | THU | FRI | ... (31 days)
✅ Row 3: (empty) | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | ... | 31
✅ Row 4-30: Branch data (AL BARRARI, AL FORSAN, ..., PLANT UMM SUQUIEM)
✅ Branches: 27
✅ Format Detected: with_headers_row2 ✓
```

### Status
✅ **Fully Supported** (Newly Added!)

---

## Format 3: No Headers (November/December Format)

### When to Use
- Minimal formatting required
- Just month name + branch data
- Weekdays auto-generated
- Fastest to create

### File Structure
```
Row 1: November 2025
Row 2: (empty)
Row 3: (empty)
Row 4: AL BARRARI    | 456.15 | 2339.9 | 1443.9 | 604.91 | 2574.9 | ...
Row 5: AL FORSAN     | 1387.8 | 809.49 | 1041.2 | 451    | 567.16 | ...
Row 6: AL SEEF       | 543.07 | 1315.3 | 595.11 | 1117.4 | 661.12 | ...
...
Row 31: PLANT OASIS TOWER | ...
Row 32: TOTAL        | ...
```

### Requirements
- Row 1: Month name (e.g., "November 2025" or just "NOVEMBER")
- Row 2-3: Empty rows (optional)
- Row 4+: Branch names in column A, sales data in columns B onwards
- System auto-generates weekday pattern (MON, TUE, WED... repeating)
- Optional: Last row can be "TOTAL" (will be skipped)

### How It Works
```
System doesn't find weekday headers
→ Automatically selects Format 3
→ Extracts month from row 1
→ Finds first branch name (not a number)
→ Counts numeric columns to determine days
→ Auto-generates weekday sequence
→ Parses branch data
```

### Auto-Generated Weekdays
- If file has 30 days: MON, TUE, WED, THU, FRI, SAT, SUN, MON, TUE, WED, ... (4 weeks + 2 days)
- If file has 31 days: MON, TUE, WED, THU, FRI, SAT, SUN, MON, TUE, WED, ... (4 weeks + 3 days)
- If file has 29 days: MON, TUE, WED, THU, FRI, SAT, SUN, MON, TUE, WED, ... (4 weeks + 1 day)

### Status
✅ **Fully Supported**

---

## Comparison Table

| Feature | Format 1 | Format 2 ⭐ | Format 3 |
|---------|----------|-----------|----------|
| **Structure** | Month + Weekdays in Row 1 | Month in Row 1, Headers in Row 2 | Month in Row 1 only |
| **Weekdays** | Explicit in row 1 | Explicit in row 2 | Auto-generated |
| **Your File** | ❌ No | ✅ Yes | ❌ No |
| **Nov 2025** | ❌ No | ✅ Yes | ✅ Also works |
| **Dec 2025** | ❌ No | ✅ Yes | ✅ Also works |
| **Easy to Create** | Medium | Easy | Easiest |
| **Explicit Info** | Most | Medium | Least |
| **Auto-Detection** | ✅ Row 1 check | ✅ Row 2 check | ✅ Default |
| **Status** | Supported | Supported | Supported |

---

## How the System Detects Format

```
Upload Excel file
    ↓
Read row 1 and row 2
    ↓
Does row 1 have weekday keywords (MON, TUE, etc.)?
    ├─ YES → Format 1 (with_headers_row1)
    └─ NO → Next check
         ↓
    Does row 2 have weekday keywords?
        ├─ YES → Format 2 (with_headers_row2) ⭐
        └─ NO → Format 3 (without_headers)
             ↓
         [Auto-generate weekdays]
```

---

## Creating Your Own Files

### Method 1: Use Format 2 (Recommended for You)

**Steps:**
1. Create Excel file
2. Row 1: Type month (e.g., "January 2026")
3. Row 2: Column A = "Outlet Name", then weekday names (THU, FRI, SAT, SUN, MON, TUE, WED...)
4. Row 3: Column A = empty, then date numbers (1, 2, 3... 31)
5. Row 4 onwards: Branch names + sales data
6. Upload and system auto-detects Format 2 ✅

### Method 2: Use Format 3 (Easiest)

**Steps:**
1. Create Excel file
2. Row 1: Type month (e.g., "January 2026")
3. Row 2-3: Leave empty
4. Row 4 onwards: Branch names + sales data
5. Upload and system auto-detects Format 3 + generates weekdays ✅

### Method 3: Use Format 1 (Most Explicit)

**Steps:**
1. Create Excel file
2. Row 1: Column A = Month, then weekday names
3. Row 2: Column A = empty, then date numbers
4. Row 3: Leave empty
5. Row 4 onwards: Branch names + sales data
6. Upload and system auto-detects Format 1 ✅

---

## Tips & Best Practices

### ✅ DO
- Keep month name in row 1 (required)
- Use consistent branch names (avoid extra spaces)
- Enter sales figures as numbers (not text)
- Include all 27 branches (or your outlet count)
- Have one row per branch

### ❌ DON'T
- Put different data in row 1 of different columns
- Use text instead of numbers for sales
- Leave random empty rows between data
- Use special characters in branch names
- Forget to include the month name

### 💡 Pro Tips
- Format 2 is most explicit (recommended)
- Format 3 is easiest and fastest
- All formats work perfectly
- Mix formats between months if needed
- Partial months work fine (only fill in available data)

---

## Examples

### Your January File (Format 2)
```
✅ Correct:
Row 1: January 2025
Row 2: Outlet Name | THU | FRI | SAT | SUN | MON | TUE | WED | THU | ...
Row 3: | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | ...
Row 4: AL BARRARI | 456 | 2340 | 1444 | 605 | 2575 | ...
```

### November File (Format 3)
```
✅ Also correct:
Row 1: November 2025
Row 2: (empty)
Row 3: (empty)
Row 4: AL BARRARI | 456 | 2340 | 1444 | 605 | 2575 | ...
```

### Template File (Format 1)
```
✅ Also correct:
Row 1: JANUARY | MON | TUE | WED | THU | FRI | SAT | SUN
Row 2: | 1 | 2 | 3 | 4 | 5 | 6 | 7
Row 3: (empty)
Row 4: AL BARRARI | 456 | 809 | 1041 | 451 | 2575 | ...
```

---

## Troubleshooting

### Upload Error: "No branch data found"
- **Cause:** Branch names not found in row 4+
- **Fix:** Verify branch names are in column A starting row 4

### Upload Error: "No numeric data found in rows"
- **Cause:** Sales figures in wrong format or location
- **Fix:** Verify sales figures are numbers, not text

### Upload Error: "Mismatch between weekdays and dates"
- **Cause:** Column count doesn't match
- **Fix:** Verify all columns have data up to the last day

### Wrong number of days detected
- **Cause:** Empty columns in the middle
- **Fix:** Format 3 stops at first empty column - fill data or use Format 2

---

## Support

**Which format should I use?**
- **Most explicit:** Format 2 (recommended)
- **Easiest:** Format 3
- **Most detailed:** Format 1

**Can I mix formats?**
- Yes! Each month can use any format
- System auto-detects each file

**What if my format is different?**
- System will detect it as Format 3
- Weekdays auto-generate from column count
- May need to verify column alignment

**Do all 27 outlets need data?**
- Ideally yes, but system handles missing outlets
- Calculates totals from available branches

---

## Format Reference Card

Print this for quick reference:

```
FORMAT 1: EXPLICIT ROW 1
Row 1: JANUARY | MON | TUE | WED | THU | FRI | SAT | SUN
Row 2: | 1 | 2 | 3 | 4 | 5 | 6 | 7
Row 3: (empty)
Row 4+: BRANCH | sales | sales | ...

FORMAT 2: HEADERS IN ROW 2 (YOUR FORMAT) ⭐
Row 1: January 2025
Row 2: Outlet Name | THU | FRI | SAT | SUN | MON | TUE | WED
Row 3: | 1 | 2 | 3 | 4 | 5 | 6 | 7
Row 4+: BRANCH | sales | sales | ...

FORMAT 3: NO HEADERS (EASIEST)
Row 1: January 2025
Row 2: (empty)
Row 3: (empty)
Row 4+: BRANCH | sales | sales | ...

All formats auto-detected ✅
All formats fully supported ✅
Mix formats between months ✅
```

---

## Final Notes

✅ All 3 formats are equally supported  
✅ System auto-detects which format you're using  
✅ No manual format selection needed  
✅ Your January 2026 file works perfectly  
✅ Use whichever format you prefer  
✅ Change format anytime you want  

**You're all set!** Pick your favorite format and start uploading. 📊

---

*Last Updated: January 8, 2026*  
*Formats Supported: 3*  
*Auto-Detection: Fully Automated*  
*Status: Production Ready ✅*
