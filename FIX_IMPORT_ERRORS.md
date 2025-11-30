# Fixing Import Errors and Shutdown Issues

## The Actual Problem

The errors you're seeing:
```
RuntimeError: can't register atexit after shutdown
ModuleNotFoundError: Could not import module 'AutoTokenizer'
```

These happen because you pressed **Ctrl+C** to stop the app, and during shutdown, scikit-learn/joblib/transformers tried to import modules that don't work well with interrupted shutdown.

## ✅ Correct Directory Structure

Your project structure is:
```
campuspulse/
└── streamlit_app/           ← Run from HERE
    ├── app.py               ← Main entry point
    ├── data/
    ├── models/
    ├── pages/
    ├── utils/
    └── requirements.txt
```

## ✅ Correct Way to Run

```bash
# Navigate to streamlit_app directory
cd /path/to/campuspulse/streamlit_app

# Run the app
streamlit run app.py
```

**Or from project root:**
```bash
cd /path/to/campuspulse
streamlit run streamlit_app/app.py
```

---

## Solutions for Import Errors

### Solution 1: Clean Shutdown (Prevent the Error)

Instead of pressing Ctrl+C immediately:

1. **Close the browser tab first**
2. **Wait 2-3 seconds**
3. **Then press Ctrl+C** in the terminal

This gives Python time to clean up properly before shutdown.

### Solution 2: Reinstall Conflicting Packages

The error occurs due to version conflicts between scikit-learn, joblib, and transformers:

```bash
# Uninstall conflicting packages
pip3 uninstall scikit-learn joblib transformers -y

# Reinstall with compatible versions
pip3 install scikit-learn==1.3.2 joblib==1.3.2 transformers==4.36.0

# Re-run app
cd streamlit_app
streamlit run app.py
```

### Solution 3: Upgrade All Packages

```bash
# Upgrade pip first
pip3 install --upgrade pip

# Upgrade all key packages
pip3 install --upgrade scikit-learn joblib transformers torch streamlit

# Re-run app
cd streamlit_app
streamlit run app.py
```

### Solution 4: Fresh Virtual Environment (Recommended)

Create a clean environment to avoid version conflicts:

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On macOS/Linux
# Or on Windows: venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r streamlit_app/requirements.txt

# If hardware errors:
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Run app
cd streamlit_app
streamlit run app.py
```

---

## Understanding the Errors

### Error 1: RuntimeError: can't register atexit after shutdown

**What it means:**
- You pressed Ctrl+C (sent SIGINT)
- Python started shutting down
- scikit-learn's joblib tried to register cleanup handlers
- But shutdown had already begun, so registration failed

**Is it harmful?** No! It's just a messy shutdown message.

**How to avoid:** Close browser first, then Ctrl+C

### Error 2: ModuleNotFoundError: Could not import module 'AutoTokenizer'

**What it means:**
- The transformers library is having issues during import
- Could be caused by:
  - Interrupted shutdown (from Ctrl+C)
  - Version incompatibility
  - Corrupted installation

**Fix:**
```bash
pip3 uninstall transformers -y
pip3 install transformers==4.36.0
```

---

## The App DID Start Successfully!

Notice this in your output:
```
You can now view your Streamlit app in your browser.
URL: http://localhost:8501
```

**The app WAS working!** The errors only appeared because you stopped it with Ctrl+C.

### To verify the app works:

1. **Start the app:**
   ```bash
   cd streamlit_app
   streamlit run app.py
   ```

2. **Open browser to http://localhost:8501**

3. **Test the app** - click around, try features

4. **When done, close browser tab FIRST**

5. **Then press Ctrl+C to stop**

---

## Permanent Fix: Update requirements.txt

To prevent version conflicts for future users:

Create `streamlit_app/requirements.txt` with pinned versions:

```txt
streamlit==1.40.1
torch==2.5.1
torchvision==0.20.1
torchaudio==2.5.1
pandas==2.2.3
numpy==1.26.4
plotly==5.24.1
scikit-learn==1.3.2
joblib==1.3.2
transformers==4.36.0
geopy==2.4.1
bcrypt==4.2.1
```

Then install:
```bash
pip3 install -r streamlit_app/requirements.txt --no-deps
pip3 install -r streamlit_app/requirements.txt
```

---

## Quick Diagnostic

Run these to check if everything is working:

```bash
# Test imports (from streamlit_app directory)
cd streamlit_app
python3 << EOF
import streamlit as st
import torch
import pandas as pd
import plotly
import sklearn
import transformers
print("✅ All imports successful!")
EOF

# If all imports work, the app will run fine
streamlit run app.py
```

---

## Summary

| Issue | Cause | Solution |
|-------|-------|----------|
| "atexit after shutdown" | Pressed Ctrl+C | Close browser first, then Ctrl+C |
| "Could not import AutoTokenizer" | Version conflict | Reinstall transformers: `pip3 install transformers==4.36.0` |
| "No module named X" | Wrong directory | Must run from `streamlit_app/` directory |
| "illegal hardware instruction" | CPU incompatible with PyTorch | Install CPU-only PyTorch |

**Most important:** The app WAS working! The errors are just shutdown messages. Try running it again and using it before stopping.

---

## Step-by-Step Fresh Start

If nothing else works:

```bash
# 1. Go to project
cd /path/to/campuspulse/streamlit_app

# 2. Verify location
ls app.py
# Should show: app.py

# 3. Clean install
pip3 uninstall -y torch scikit-learn joblib transformers
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip3 install streamlit pandas plotly scikit-learn==1.3.2 joblib==1.3.2 transformers==4.36.0 geopy bcrypt

# 4. Run app
streamlit run app.py

# 5. Use app in browser

# 6. Close browser tab first, THEN press Ctrl+C
```

---

## Still Getting Errors on Fresh Start?

If you get errors **before** pressing Ctrl+C (i.e., the app doesn't start at all):

### Check 1: Missing Dependencies
```bash
pip3 install -r requirements.txt
```

### Check 2: Python Version
```bash
python3 --version
# Should be 3.11 or higher
```

### Check 3: Corrupted Cache
```bash
# Clear Python cache
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
rm -rf ~/.cache/pip

# Reinstall
pip3 install -r requirements.txt
```

### Check 4: Port Already in Use
```bash
# Try different port
streamlit run app.py --server.port 8502
```

---

## For Your Friend's Computer

Share these specific instructions:

1. **Clone the repo:**
   ```bash
   cd ~/Downloads
   git clone <repo-url> campuspulse
   cd campuspulse/streamlit_app
   ```

2. **Install CPU-only PyTorch** (to avoid "illegal hardware instruction"):
   ```bash
   pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
   ```

3. **Install other dependencies:**
   ```bash
   pip3 install streamlit pandas plotly scikit-learn==1.3.2 joblib==1.3.2 transformers==4.36.0 geopy bcrypt
   ```

4. **Run app:**
   ```bash
   streamlit run app.py
   ```

5. **Open http://localhost:8501 in browser**

6. **When done:** Close browser tab, wait 2 seconds, then Ctrl+C

---

**Bottom line:** Your app is working fine! The errors are just shutdown noise. Ignore them or use Solution 1 (close browser first) to avoid them.
