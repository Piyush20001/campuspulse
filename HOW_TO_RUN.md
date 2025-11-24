# How to Run Campus Pulse - IMPORTANT

## ❌ Common Mistake: Running from Wrong Directory

Many users get errors because they run the app from the wrong location.

### ❌ WRONG - Running from inside streamlit_app directory:
```bash
cd campuspulse/streamlit_app
streamlit run app.py          # ❌ This will cause import errors!
```

### ✅ CORRECT - Running from project root:
```bash
cd campuspulse                # Make sure you're in the ROOT directory
streamlit run app.py          # ✅ This works!
```

---

## Step-by-Step Instructions

### 1. Navigate to the Correct Directory

```bash
# Find your project
cd /path/to/campuspulse

# Verify you're in the right place - you should see:
ls
# Expected output:
# app.py  README.md  requirements.txt  streamlit_app/  ...
```

**Important:** The directory should contain:
- ✅ `app.py` (at the root level)
- ✅ `streamlit_app/` folder (subdirectory)
- ✅ `requirements.txt`
- ✅ `README.md`

If you don't see `app.py` in the current directory, you're in the wrong place!

### 2. Check Your Location

```bash
# Print current directory
pwd

# Should show something like:
# /Users/yourname/Downloads/campuspulse
# NOT: /Users/yourname/Downloads/campuspulse/streamlit_app
```

### 3. Run the Application

```bash
streamlit run app.py
```

**Not:**
- ❌ `streamlit run streamlit_app/app.py`
- ❌ `cd streamlit_app && streamlit run app.py`
- ❌ `python app.py`

---

## Fixing Import Errors

If you see errors like:
```
ModuleNotFoundError: No module named 'data'
ModuleNotFoundError: No module named 'models'
ModuleNotFoundError: Could not import module 'AutoTokenizer'
RuntimeError: can't register atexit after shutdown
```

These are usually caused by:
1. **Wrong directory** (most common - see above)
2. **Missing dependencies** (see below)
3. **Interrupted shutdown** (harmless, see below)

### Fix 1: Ensure Correct Directory

```bash
# Go to project root
cd /path/to/campuspulse

# Verify app.py exists HERE
ls app.py
# Should show: app.py

# Now run
streamlit run app.py
```

### Fix 2: Reinstall Dependencies

If you still get import errors after fixing the directory:

```bash
# Reinstall all dependencies
pip3 install -r requirements.txt

# If you get "illegal hardware instruction" error:
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Then reinstall other requirements
pip3 install streamlit pandas plotly scikit-learn geopy bcrypt transformers
```

### Fix 3: "can't register atexit after shutdown" Error

This error appears when you press Ctrl+C to stop Streamlit. It's **harmless** and can be ignored.

**Why it happens:**
1. You press Ctrl+C
2. Python starts shutting down
3. During cleanup, scikit-learn tries to register shutdown handlers
4. But shutdown already started, so it fails

**How to avoid it:**
- Close the browser tab first
- Wait 2-3 seconds
- Then press Ctrl+C in the terminal

Or just ignore it - it doesn't affect the app's functionality.

---

## Complete Fresh Start

If nothing works, do a complete clean installation:

```bash
# 1. Navigate to Downloads or wherever you want the project
cd ~/Downloads

# 2. Remove old installation
rm -rf campuspulse campuspulse_2

# 3. Clone fresh copy
git clone <your-repo-url> campuspulse

# 4. Navigate into project ROOT
cd campuspulse

# 5. Verify location
ls
# Should see: app.py  README.md  requirements.txt  streamlit_app/

# 6. Install dependencies
pip3 install -r requirements.txt

# If hardware errors occur:
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip3 install -r requirements.txt

# 7. Run app
streamlit run app.py
```

---

## Verification Before Running

Run these checks before starting the app:

```bash
# Check 1: Correct directory?
pwd
# Should end with "campuspulse", NOT "campuspulse/streamlit_app"

# Check 2: app.py exists in current directory?
ls app.py
# Should show: app.py (not an error)

# Check 3: streamlit_app folder exists as subdirectory?
ls streamlit_app/
# Should show: pages/  models/  data/  ...

# Check 4: Python dependencies installed?
python3 -c "import streamlit, torch, pandas, plotly; print('Dependencies OK')"
# Should show: Dependencies OK

# All checks passed? Run the app:
streamlit run app.py
```

---

## Directory Structure Explained

```
campuspulse/                    ← YOU MUST BE HERE when running
├── app.py                      ← Main entry point
├── requirements.txt
├── README.md
├── streamlit_app/              ← Don't run from inside here!
│   ├── __init__.py
│   ├── pages/
│   │   ├── 1_📊_Dashboard.py
│   │   ├── 2_🎉_Events.py
│   │   └── ...
│   ├── models/
│   │   ├── lstm_forecaster.py
│   │   └── ...
│   ├── data/
│   │   ├── simulator.py
│   │   └── ...
│   └── utils/
└── ...
```

**Key Points:**
- `app.py` is at the ROOT (top level)
- `streamlit_app/` is a FOLDER containing the app code
- You run `streamlit run app.py` from the ROOT
- The app's internal code lives in `streamlit_app/`

---

## Platform-Specific Instructions

### macOS

```bash
# Find project
cd ~/Downloads/campuspulse

# Verify location
pwd
# Should show: /Users/yourname/Downloads/campuspulse

# Run app
streamlit run app.py
```

### Linux

```bash
# Find project
cd ~/campuspulse

# Verify location
pwd
# Should show: /home/yourname/campuspulse

# Run app
streamlit run app.py
```

### Windows

```bash
# Find project
cd C:\Users\YourName\Downloads\campuspulse

# Verify location
cd
# Should show: C:\Users\YourName\Downloads\campuspulse

# Run app
streamlit run app.py
```

---

## Still Getting Errors?

### Error: "No module named 'streamlit_app'"

**Cause:** Running from wrong directory

**Fix:**
```bash
# Go UP one level if you're in streamlit_app/
cd ..

# Verify you see app.py
ls app.py

# Run
streamlit run app.py
```

### Error: "No such file or directory: 'app.py'"

**Cause:** You're in the wrong directory or app.py doesn't exist

**Fix:**
```bash
# Find where app.py is
find ~ -name "app.py" -path "*/campuspulse/*" 2>/dev/null

# Navigate to that directory's parent
cd /path/to/campuspulse

# Run
streamlit run app.py
```

### Error: "ModuleNotFoundError: No module named 'data'"

**Cause:** Running from inside `streamlit_app/` directory

**Fix:**
```bash
# Go to parent directory
cd ..

# Verify you're in the right place
ls
# Should see both: app.py  streamlit_app/

# Run
streamlit run app.py
```

---

## Quick Reference

**✅ Correct way to run:**
```bash
cd /path/to/campuspulse     # Go to ROOT directory (where app.py is)
streamlit run app.py         # Run from ROOT
```

**❌ Incorrect ways:**
```bash
cd campuspulse/streamlit_app && streamlit run app.py  # Wrong directory
streamlit run streamlit_app/app.py                     # Wrong path
python app.py                                          # Wrong command
python3 streamlit_app/app.py                          # Wrong everything
```

---

## Pro Tip: Create an Alias

To make running easier, create an alias:

### Bash/Zsh (macOS/Linux)

Add to `~/.bashrc` or `~/.zshrc`:
```bash
alias campuspulse='cd /path/to/campuspulse && streamlit run app.py'
```

Then just type:
```bash
campuspulse
```

### Windows (PowerShell)

Add to PowerShell profile:
```powershell
function Start-CampusPulse {
    cd C:\path\to\campuspulse
    streamlit run app.py
}
Set-Alias campuspulse Start-CampusPulse
```

---

## Summary

1. **Always run from project ROOT** (where `app.py` is located)
2. **Never run from inside `streamlit_app/`** directory
3. **Use `streamlit run app.py`** (not python app.py)
4. **Check location with `pwd` and `ls`** before running
5. **Ignore "atexit" errors** when stopping with Ctrl+C

**Golden Rule:** If you can see `app.py` when you type `ls`, you're in the right place! 🎉
