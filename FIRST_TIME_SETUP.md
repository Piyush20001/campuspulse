# First Time Setup Guide for Campus Pulse

## Why is the App "Blank" After Cloning?

When you clone the Campus Pulse repository from GitHub, certain files are **intentionally excluded** for security reasons:

❌ **Not included in GitHub:**
- `campus_pulse_users.db` - User accounts and authentication data
- `campus_pulse_feedback.db` - User feedback and ratings
- `campus_pulse_performance.db` - Performance metrics
- Browser cache and session data

✅ **Included in GitHub:**
- All Python code
- ML model (`lstm_crowd_model.pth` - 204KB)
- Training data CSV files
- Documentation

---

## Complete Setup Instructions

Follow these steps on a **fresh computer** to get Campus Pulse running:

### Step 1: Install Python 3.11+

```bash
# Check if Python is installed
python3 --version

# Should show Python 3.11 or higher
# If not, install from: https://www.python.org/downloads/
```

### Step 2: Navigate to Project Directory

```bash
cd /path/to/campuspulse
```

### Step 3: Install Dependencies

**Option A: Using pip (Quick)**
```bash
# Install all required packages
pip3 install -r requirements.txt

# If you get "illegal hardware instruction" error, use CPU-only PyTorch:
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip3 install -r requirements.txt
```

**Option B: Using conda (Recommended for compatibility)**
```bash
# Create virtual environment
conda create -n campuspulse python=3.11 -y
conda activate campuspulse

# Install PyTorch (conda auto-selects compatible build)
conda install pytorch torchvision torchaudio cpuonly -c pytorch -y

# Install other dependencies
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
# Test PyTorch
python3 -c "import torch; print(f'PyTorch {torch.__version__} installed successfully')"

# Test Streamlit
python3 -c "import streamlit; print(f'Streamlit {streamlit.__version__} installed successfully')"

# Test model loading
python3 -c "from streamlit_app.models.lstm_forecaster import LSTMForecaster; print('LSTM model loaded successfully')"
```

### Step 5: Run the Application

```bash
streamlit run app.py
```

**Expected output:**
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

### Step 6: Create Your First Account

1. **Open browser** to `http://localhost:8501`
2. **Click "Login/Signup"** in the sidebar
3. **Create account:**
   - Email: your email (e.g., `user@ufl.edu`)
   - Password: at least 8 characters
   - Full name: Your name
4. **Login** with your new credentials

**What happens:** The app automatically creates empty database files:
- `campus_pulse_users.db` - Now contains YOUR account
- `campus_pulse_feedback.db` - Empty, ready for feedback
- `campus_pulse_performance.db` - Empty, will track metrics as you use the app

---

## Understanding the "Blank" State

### On First Launch, You'll See:

✅ **Working Features:**
- Real-time crowd simulation (generates live data)
- Interactive map of UF facilities
- LSTM crowd predictions (90-minute forecasts)
- Location details and amenities
- Event calendar

❌ **Empty/Blank Features:**
- No user accounts (until you create one)
- No historical performance metrics (builds over time)
- No user feedback (until users submit feedback)
- No social features (until multiple users exist)

### This is NORMAL!

The app uses **simulated real-time data** for crowd levels, so you'll immediately see:
- Live crowd counts for 10+ UF locations
- Predicted occupancy graphs
- Current status indicators (🟢 Quiet, 🟡 Moderate, 🔴 Busy)

---

## Common Issues and Solutions

### Issue 1: "illegal hardware instruction" Error

**Cause:** Your CPU doesn't support AVX2/AVX512 instructions required by PyTorch

**Solution:**
```bash
# Uninstall PyTorch
pip3 uninstall torch torchvision torchaudio -y

# Install CPU-only version (compatible with older CPUs)
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Re-run app
streamlit run app.py
```

See `TROUBLESHOOTING_ILLEGAL_INSTRUCTION.md` for detailed fixes.

---

### Issue 2: "ModuleNotFoundError" for packages

**Cause:** Missing dependencies

**Solution:**
```bash
# Ensure you're in the project directory
cd /path/to/campuspulse

# Reinstall all requirements
pip3 install -r requirements.txt

# If specific module missing (e.g., torch):
pip3 install torch torchvision torchaudio
```

---

### Issue 3: App Shows Blank Page / White Screen

**Cause:** Browser cache or port conflict

**Solutions:**

**A. Clear Browser Cache**
```
1. Open browser dev tools (F12)
2. Right-click the refresh button
3. Select "Empty Cache and Hard Reload"
```

**B. Try Different Port**
```bash
streamlit run app.py --server.port 8502
```

**C. Try Different Browser**
```
Try Chrome, Firefox, or Safari
```

---

### Issue 4: Database Permissions Error

**Cause:** No write permissions in directory

**Solution:**
```bash
# Check directory permissions
ls -la

# Make directory writable (Linux/macOS)
chmod 755 .

# On Windows, run Command Prompt as Administrator
```

---

### Issue 5: "No module named 'streamlit_app'"

**Cause:** Running from wrong directory

**Solution:**
```bash
# Must run from project root (where app.py is located)
cd /path/to/campuspulse
streamlit run app.py

# NOT from inside subdirectories
```

---

## Verifying Everything Works

### Quick Verification Checklist

Run these tests to ensure setup is complete:

```bash
# 1. Check Python version
python3 --version
# Expected: Python 3.11.x or higher

# 2. Check PyTorch
python3 -c "import torch; print(torch.__version__)"
# Expected: 2.5.x or similar

# 3. Check Streamlit
python3 -c "import streamlit; print(streamlit.__version__)"
# Expected: 1.40.x or similar

# 4. Check LSTM model exists
ls -lh streamlit_app/models/lstm_crowd_model.pth
# Expected: -rw-r--r-- ... 204K ... lstm_crowd_model.pth

# 5. Check training data exists
ls -lh streamlit_app/data/*.csv
# Expected: crowd_training_data_5000.csv, crowd_training_data_5000_v2.csv

# 6. Run app
streamlit run app.py
# Expected: Browser opens to http://localhost:8501
```

---

## What You Should See on First Run

### Home Page (Dashboard)
```
✅ Interactive map with 10+ UF locations
✅ Real-time crowd indicators (🟢 🟡 🔴)
✅ "Current Crowds" section with live data
✅ "Upcoming Events" section
✅ Quick stats (avg wait time, busiest location, etc.)
```

### Predictions Page
```
✅ Dropdown to select location
✅ Graph showing current + 90-minute forecast
✅ Predicted crowd levels with timestamps
✅ Confidence intervals
✅ Model info (LSTM neural network, 174ms inference)
```

### Map Page
```
✅ Interactive UF campus map
✅ Pins for all monitored locations
✅ Click pins to see details
✅ Color-coded by crowd level
```

### Individual Location Pages
```
✅ Location name and image
✅ Current crowd status
✅ Amenities list
✅ Operating hours
✅ Popular times graph
✅ Upcoming events
```

---

## Database Files Explained

After running the app, you'll see these new files:

### `campus_pulse_users.db` (Auto-created)
- **Purpose:** User accounts and authentication
- **Size:** Starts at ~20KB, grows with users
- **Contains:**
  - User credentials (hashed passwords)
  - Profile information
  - Settings and preferences
  - Active sessions

### `campus_pulse_feedback.db` (Auto-created)
- **Purpose:** User feedback and ratings
- **Size:** Starts at ~10KB
- **Contains:**
  - Feedback submissions
  - Ratings (1-5 stars)
  - Comments and suggestions
  - Timestamps

### `campus_pulse_performance.db` (Auto-created)
- **Purpose:** Performance monitoring
- **Size:** Grows over time
- **Contains:**
  - Response times
  - API latency measurements
  - Page load times
  - Model inference times
  - Database query performance

**IMPORTANT:** These files are in `.gitignore` and will NOT be committed to GitHub (they contain sensitive user data).

---

## Transferring Data Between Computers

If you want to transfer your data (users, feedback, metrics) from one computer to another:

### Option 1: Manual Database Transfer

```bash
# On your computer (source)
cp campus_pulse_users.db /path/to/usb/
cp campus_pulse_feedback.db /path/to/usb/
cp campus_pulse_performance.db /path/to/usb/

# On friend's computer (destination)
# After cloning the repo and installing dependencies:
cp /path/to/usb/*.db /path/to/campuspulse/
```

### Option 2: Fresh Start (Recommended)

Just let your friend:
1. Clone the repo
2. Install dependencies
3. Run the app
4. Create their own account

They'll get a fresh, clean installation with no old data.

---

## Security Notes

### Why Databases Are Excluded from Git

1. **Privacy:** User emails, names, and profiles are personal data
2. **Security:** Password hashes should never be in public repos
3. **Compliance:** FERPA/GDPR requirements for educational data
4. **File Size:** Databases can grow large (50MB+)

### Safe Practices

✅ **DO:**
- Keep `.gitignore` as-is (excludes `*.db` files)
- Use strong passwords for accounts
- Transfer databases via secure methods only

❌ **DON'T:**
- Commit `*.db` files to GitHub
- Share database files publicly
- Use production databases for testing

---

## Next Steps After Setup

1. **Explore the app** - Click through all pages
2. **Create test account** - Try login/signup flow
3. **Submit feedback** - Test the feedback form
4. **Check performance** - View the Performance Metrics page (requires admin account)
5. **Read documentation:**
   - `README.md` - Project overview
   - `DEPLOYMENT_AND_MONITORING_PLAN.md` - Deployment guide
   - `PROJECT_DESCRIPTION.md` - Detailed project description
   - `TROUBLESHOOTING_ILLEGAL_INSTRUCTION.md` - Hardware errors

---

## Still Having Issues?

### Get Help

1. **Check error messages** - Read the full error in terminal
2. **Review logs** - Streamlit shows detailed error traces
3. **Test components** - Use verification commands above
4. **Ask for help** - Provide:
   - Your OS (Windows/macOS/Linux)
   - Python version (`python3 --version`)
   - Error message (full text)
   - What you were trying to do

### Common Error Patterns

```bash
# "illegal hardware instruction" → See TROUBLESHOOTING_ILLEGAL_INSTRUCTION.md
# "ModuleNotFoundError" → Run: pip3 install -r requirements.txt
# "Permission denied" → Check directory write permissions
# "Port already in use" → Change port: streamlit run app.py --server.port 8502
# "Database locked" → Close other instances of the app
```

---

## Success Indicators

You'll know setup is complete when:

✅ App opens in browser without errors
✅ You can see the interactive map
✅ Locations show real-time crowd data
✅ Predictions graph displays forecasts
✅ You can create and login to an account
✅ No red error messages in Streamlit

---

## Summary

**Why blank after cloning?**
- Database files (users, feedback, metrics) are intentionally excluded from Git for security

**How to fix?**
1. Install dependencies: `pip3 install -r requirements.txt`
2. Run app: `streamlit run app.py`
3. Databases auto-create on first run
4. Create your first account to populate user database

**Result:**
- Fresh, working installation
- Empty databases (normal!)
- App shows simulated real-time data
- Ready for new users and feedback

---

## Quick Start (TL;DR)

```bash
# Clone repo
git clone <repo-url>
cd campuspulse

# Install dependencies
pip3 install -r requirements.txt

# If hardware error occurs:
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Run app
streamlit run app.py

# Create account in browser at http://localhost:8501
```

That's it! 🎉
