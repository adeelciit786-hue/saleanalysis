# 🚀 Streamlit Deployment Guide

## Overview: Two Separate Apps Architecture

Your Champion Cleaners dashboard consists of **2 separate Streamlit applications**:

| App | Purpose | Access | Auth | Users |
|-----|---------|--------|------|-------|
| **Admin App** | Data upload & management | Restricted | ✓ Required | Staff/Admin |
| **Viewer App** | Read-only dashboard | Public | ✗ Not needed | Management/Team |

---

## 📋 Prerequisites

Before deploying, ensure you have:

✓ GitHub account (already created: `adeelciit786-hue`)  
✓ Streamlit Community Cloud account (free, uses GitHub OAuth)  
✓ Code pushed to GitHub (see "Push to GitHub" section below)

---

## 1️⃣ Push Code to GitHub

### Step 1: Navigate to Project
```bash
cd "C:\Users\adeel\Sales projection"
```

### Step 2: Initialize Git (if not done)
```bash
git init
git remote add origin https://github.com/adeelciit786-hue/champion.git
```

### Step 3: Stage and Commit Files
```bash
git add .
git commit -m "Initial commit: Complete sales forecasting dashboard with dual interfaces"
```

### Step 4: Push to GitHub
```bash
git branch -M main
git push -u origin main
```

**Verify on GitHub:**
- Visit: https://github.com/adeelciit786-hue/champion
- Check that all files are visible

---

## 2️⃣ Deploy Admin App on Streamlit Cloud

### Step 1: Go to Streamlit Cloud
1. Visit: https://streamlit.io/cloud
2. Click **"New app"** button

### Step 2: Connect Repository
- **GitHub account**: adeelciit786-hue
- **Repository**: champion
- **Branch**: main
- **Main file path**: `streamlit_apps/admin_app.py`

### Step 3: Deploy
- Click **"Deploy"** button
- Wait 2-3 minutes for build to complete
- Your app will be at: `https://[username]-admin.streamlit.app`

### Step 4: Set Secrets (Optional - for production)
In the app's settings, add to `.streamlit/secrets.toml`:
```toml
[auth]
admin_password = "your_secure_password_here"
```

---

## 3️⃣ Deploy Viewer App on Streamlit Cloud

### Step 1: Create Second App
1. Visit: https://streamlit.io/cloud
2. Click **"New app"** again

### Step 2: Connect Same Repository
- **GitHub account**: adeelciit786-hue
- **Repository**: champion
- **Branch**: main
- **Main file path**: `streamlit_apps/viewer_app.py`

### Step 3: Deploy
- Click **"Deploy"** button
- Your app will be at: `https://[username]-viewer.streamlit.app`

---

## 📊 Your Final URLs

After deployment, you'll have:

**Admin Panel** (Secure, Password Protected)
```
https://[username]-admin.streamlit.app
Username: admin
Password: admin123
```

**Viewer Dashboard** (Public, No Password)
```
https://[username]-viewer.streamlit.app
✓ Accessible to everyone
✓ No authentication required
```

Replace `[username]` with your Streamlit username.

---

## ⚙️ Configuration Files

### `.streamlit/config.toml`
Controls app appearance and behavior. Located in project root.

```toml
[theme]
primaryColor = "#2E86AB"           # Main color (Champion blue)
backgroundColor = "#F8F9FA"        # Light background
secondaryBackgroundColor = "#FFFFFF" # White containers

[server]
port = 8501                        # Default Streamlit port
headless = true                    # Serverless deployment
```

### `requirements.txt`
Lists all Python dependencies. Automatically installed on deployment:
- Flask 3.1.2
- pandas 2.3.3
- numpy 2.4.0
- plotly 6.5.1
- openpyxl 3.1.5
- streamlit 1.28.1

---

## 🔐 Security Considerations

### Default Credentials
**CHANGE THESE IN PRODUCTION!**

Current: `admin` / `admin123`

To change, edit `streamlit_apps/admin_app.py` line 30:
```python
ADMIN_CREDENTIALS = {
    'admin': 'your_new_secure_password'
}
```

### Session Management
- Admin sessions expire after 24 hours
- Automatic logout on inactivity
- Credentials stored in memory (not saved to files)

### Viewer App
- No authentication (intentionally public)
- Read-only access (no data modification)
- Safe for public viewing

---

## 📱 Local Testing Before Deployment

### Test Admin App Locally
```bash
cd streamlit_apps
streamlit run admin_app.py
# Accessible at: http://localhost:8501
```

### Test Viewer App Locally
```bash
cd streamlit_apps
streamlit run viewer_app.py
# Accessible at: http://localhost:8502
```

---

## 🔄 Data Sharing Between Apps

Since Streamlit apps are separate, they need a way to share data:

### Current Implementation (Development)
Each app maintains its own session state. Data is not shared between instances.

### Production Recommendations

**Option A: CSV File Storage** (Simplest)
```python
# Save data to CSV after upload
df.to_csv('data/sales_data.csv', index=False)

# Load in viewer
df = pd.read_csv('data/sales_data.csv')
```

**Option B: SQLite Database** (Recommended)
```python
import sqlite3

# Save
conn = sqlite3.connect('data/sales.db')
df.to_sql('sales', conn, if_exists='replace')

# Load
df = pd.read_sql('SELECT * FROM sales', conn)
```

**Option C: Cloud Database** (Best for Production)
- Firebase Realtime Database
- PostgreSQL on Heroku
- MongoDB Atlas
- AWS DynamoDB

---

## 🐛 Troubleshooting

### App Won't Deploy
- **Check logs** in Streamlit dashboard
- **Verify requirements.txt** has all dependencies
- **Check file paths** are relative, not absolute

### Data Not Showing
- **Upload data** in admin app first
- **Check data file** exists in correct location
- **Verify file permissions** (read/write)

### Charts Not Rendering
- **Install plotly**: `pip install plotly==6.5.1`
- **Check data format**: Ensure dates are valid
- **Verify minimum 2 months** of historical data

### Login Issues (Admin App)
- **Default credentials**: admin / admin123
- **Check username/password** spelling
- **Clear browser cache** if credentials change

### Session Expired
- **24-hour timeout** is by design
- **Re-login required** after expiry
- **Normal behavior** - not an error

---

## 📈 Performance Tips

1. **Upload smaller files**: Split into monthly chunks
2. **Clear old data**: Remove unused historical files
3. **Use SQLite**: Better than CSV for 1000+ records
4. **Cache data**: Use `@st.cache_data` for heavy operations

---

## 🔄 Updates & Maintenance

### Push Updates
```bash
git add .
git commit -m "Update: [description of changes]"
git push origin main
```

Streamlit Cloud auto-redeploys on GitHub push (within 1-2 minutes).

### Monitor Deployments
1. Go to: https://share.streamlit.io/deeploy/admin
2. Check "Logs" tab for errors
3. View app status and statistics

---

## 📞 Support & Resources

### Documentation
- Streamlit Docs: https://docs.streamlit.io
- GitHub Issues: https://github.com/adeelciit786-hue/champion/issues
- Project Repo: https://github.com/adeelciit786-hue/champion

### Contact
📧 adeelciit786@gmail.com

---

## ✅ Deployment Checklist

Before considering deployment complete:

- [ ] Code pushed to GitHub
- [ ] Admin app deployed on Streamlit
- [ ] Viewer app deployed on Streamlit
- [ ] Both apps accessible via public URLs
- [ ] Admin login works correctly
- [ ] Data upload functions properly
- [ ] Charts display correctly
- [ ] Viewer shows same data as admin
- [ ] Browser back/forward navigation works
- [ ] Credentials changed from defaults (production only)

---

**Congratulations! 🎉 Your dual-interface sales forecasting system is live!**

Share these URLs with your team:
- **Admin Staff**: https://[username]-admin.streamlit.app
- **Management**: https://[username]-viewer.streamlit.app
