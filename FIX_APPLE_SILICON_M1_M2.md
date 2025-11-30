# Fix for Apple Silicon (M1/M2/M3) - App Stuck Loading

## Problem

On MacBook M1 Pro (or M1/M2/M3), the app:
- Shows sidebar but main content is blank/white
- Python crashes unexpectedly
- Streamlit gets stuck loading

**Why this happens:**
- Wrong Python architecture (x86_64 instead of ARM64)
- Wrong PyTorch build (Intel instead of Apple Silicon)
- Running under Rosetta 2 emulation instead of native

---

## Solution 1: Verify Python Architecture (CRITICAL)

**Check what architecture Python is using:**

```bash
# Check Python architecture
python3 -c "import platform; print(platform.machine())"

# Should show: arm64
# If shows: x86_64 ← THIS IS THE PROBLEM
```

If it shows `x86_64`, you're running Intel Python under Rosetta emulation. This causes crashes!

### Fix: Install Native ARM64 Python

```bash
# Option A: Use Homebrew (recommended)
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python (automatically ARM64 on Apple Silicon)
brew install python@3.11

# Verify it's ARM64
/opt/homebrew/bin/python3 -c "import platform; print(platform.machine())"
# Should show: arm64

# Option B: Download from python.org
# Go to https://www.python.org/downloads/macos/
# Download "macOS 64-bit universal2 installer"
# This includes ARM64 support
```

---

## Solution 2: Fresh Installation with ARM64 Python

**Complete clean installation for Apple Silicon:**

```bash
# 1. Navigate to project
cd ~/Downloads/campuspulse/streamlit_app

# 2. Use Homebrew Python (ARM64 native)
/opt/homebrew/bin/python3 -m venv venv_arm

# 3. Activate virtual environment
source venv_arm/bin/activate

# 4. Verify ARM64
python -c "import platform; print(f'Architecture: {platform.machine()}')"
# Must show: Architecture: arm64

# 5. Upgrade pip
pip install --upgrade pip

# 6. Install PyTorch for Apple Silicon
pip install torch torchvision torchaudio

# 7. Install other dependencies
pip install streamlit pandas numpy plotly scikit-learn geopy bcrypt transformers

# 8. Run app
streamlit run app.py
```

---

## Solution 3: Check for Rosetta Processes

Apple Silicon can run Intel (x86_64) apps via Rosetta 2 translation. Check if Python is running under Rosetta:

```bash
# Check if python is running under Rosetta
ps aux | grep -i python | grep -i rosetta

# If you see output, Python is using Rosetta (BAD)
# If no output, Python is native ARM64 (GOOD)

# Alternative check
file $(which python3)
# Should show: Mach-O 64-bit executable arm64
# NOT: Mach-O 64-bit executable x86_64
```

---

## Solution 4: Install PyTorch with MPS Support

Apple Silicon has Metal Performance Shaders (MPS) for GPU acceleration. Use this:

```bash
# Uninstall current PyTorch
pip uninstall torch torchvision torchaudio -y

# Install PyTorch with MPS support
pip install torch torchvision torchaudio

# Verify MPS is available
python3 << EOF
import torch
print(f"PyTorch version: {torch.__version__}")
print(f"MPS available: {torch.backends.mps.is_available()}")
print(f"MPS built: {torch.backends.mps.is_built()}")
EOF

# Should show:
# PyTorch version: 2.5.x
# MPS available: True
# MPS built: True
```

---

## Solution 5: Fix Terminal Architecture

Sometimes Terminal.app itself runs in Rosetta mode:

```bash
# Check current shell architecture
uname -m
# Should show: arm64
# If shows: x86_64, your Terminal is in Rosetta mode

# Fix:
# 1. Quit Terminal completely
# 2. Right-click Terminal.app in Applications/Utilities
# 3. Get Info
# 4. UNCHECK "Open using Rosetta"
# 5. Relaunch Terminal
# 6. Verify: uname -m should now show arm64
```

---

## Solution 6: Debug Stuck Loading

If the app starts but gets stuck (white screen), check what's hanging:

### Step 1: Check Terminal for Errors

Look at the terminal where you ran `streamlit run app.py`. You should see:
- Any Python errors
- Traceback messages
- Warning about missing modules

### Step 2: Test Individual Components

```bash
cd streamlit_app

# Test 1: Can Python import basic modules?
python3 -c "import streamlit; print('Streamlit OK')"

# Test 2: Can PyTorch load?
python3 -c "import torch; print('PyTorch OK')"

# Test 3: Can LSTM model load?
python3 -c "from models.lstm_forecaster import CrowdForecaster; print('LSTM OK')"

# Test 4: Can transformers load?
python3 -c "from transformers import AutoTokenizer; print('Transformers OK')"

# If any of these fail, that's your culprit
```

### Step 3: Disable Problematic Components

If transformers is causing the hang, temporarily disable it:

**Edit `streamlit_app/models/event_classifier_improved.py`:**

Find line 8:
```python
from transformers import AutoTokenizer, AutoModel, get_linear_schedule_with_warmup
```

Wrap in try/except:
```python
try:
    from transformers import AutoTokenizer, AutoModel, get_linear_schedule_with_warmup
    TRANSFORMERS_AVAILABLE = True
except Exception as e:
    print(f"Transformers not available: {e}")
    TRANSFORMERS_AVAILABLE = False
    AutoTokenizer = None
    AutoModel = None
```

---

## Solution 7: Increase Memory Limit

M1 Pro might have memory pressure issues:

```bash
# Run with increased memory
streamlit run app.py --server.maxUploadSize 200

# Or set environment variable
export STREAMLIT_SERVER_MAX_UPLOAD_SIZE=200
streamlit run app.py
```

---

## Solution 8: Browser Issues

Sometimes Safari has issues with Streamlit on Apple Silicon:

```bash
# Try Chrome instead
streamlit run app.py --server.browser.serverAddress=localhost

# Then manually open in Chrome:
# http://localhost:8501

# Or force different port
streamlit run app.py --server.port 8502
```

---

## Complete Diagnostic Script

Save this as `test_apple_silicon.py` in `streamlit_app/`:

```python
#!/usr/bin/env python3
"""
Diagnostic script for Apple Silicon compatibility
"""
import sys
import platform

print("=" * 60)
print("Apple Silicon Compatibility Check")
print("=" * 60)

# Check 1: Architecture
arch = platform.machine()
print(f"\n1. Python Architecture: {arch}")
if arch == "arm64":
    print("   ✅ Native ARM64 (correct)")
elif arch == "x86_64":
    print("   ❌ Intel x86_64 (PROBLEM - running under Rosetta)")
    print("   Fix: Install ARM64 Python via Homebrew")
else:
    print(f"   ⚠️  Unknown architecture: {arch}")

# Check 2: Python Version
py_version = platform.python_version()
print(f"\n2. Python Version: {py_version}")
if tuple(map(int, py_version.split('.')[:2])) >= (3, 11):
    print("   ✅ Version 3.11+ (compatible)")
else:
    print("   ⚠️  Consider upgrading to Python 3.11+")

# Check 3: PyTorch
try:
    import torch
    print(f"\n3. PyTorch: {torch.__version__}")
    print(f"   MPS Available: {torch.backends.mps.is_available()}")
    print(f"   MPS Built: {torch.backends.mps.is_built()}")

    # Test tensor creation
    x = torch.randn(5, 5)
    print("   ✅ PyTorch working")
except ImportError:
    print("\n3. PyTorch: NOT INSTALLED")
    print("   ❌ Install: pip install torch torchvision torchaudio")
except Exception as e:
    print(f"\n3. PyTorch: ERROR - {e}")
    print("   ❌ Reinstall: pip uninstall torch -y && pip install torch")

# Check 4: Streamlit
try:
    import streamlit
    print(f"\n4. Streamlit: {streamlit.__version__}")
    print("   ✅ Streamlit installed")
except ImportError:
    print("\n4. Streamlit: NOT INSTALLED")
    print("   ❌ Install: pip install streamlit")

# Check 5: NumPy
try:
    import numpy as np
    print(f"\n5. NumPy: {np.__version__}")
    # Test array operations
    arr = np.random.randn(100, 100)
    result = arr @ arr.T
    print("   ✅ NumPy working")
except Exception as e:
    print(f"\n5. NumPy: ERROR - {e}")

# Check 6: scikit-learn
try:
    import sklearn
    print(f"\n6. scikit-learn: {sklearn.__version__}")
    print("   ✅ scikit-learn installed")
except ImportError:
    print("\n6. scikit-learn: NOT INSTALLED")
    print("   ❌ Install: pip install scikit-learn")

# Check 7: transformers
try:
    import transformers
    print(f"\n7. transformers: {transformers.__version__}")
    print("   ✅ transformers installed")
except ImportError:
    print("\n7. transformers: NOT INSTALLED (optional)")

# Check 8: LSTM Model
print("\n8. Testing LSTM Model Load...")
try:
    from models.lstm_forecaster import CrowdForecaster
    forecaster = CrowdForecaster()
    print("   ✅ LSTM model loaded successfully")
except Exception as e:
    print(f"   ❌ LSTM model failed: {e}")

# Summary
print("\n" + "=" * 60)
if arch == "arm64":
    print("✅ System appears to be configured correctly")
    print("\nIf app still hangs, check terminal for specific errors")
else:
    print("❌ CRITICAL: Python is running in Rosetta (x86_64) mode")
    print("\n🔧 FIX:")
    print("   1. Install Homebrew: brew install python@3.11")
    print("   2. Use Homebrew Python: /opt/homebrew/bin/python3")
    print("   3. Create venv: python3 -m venv venv_arm")
    print("   4. Activate: source venv_arm/bin/activate")
    print("   5. Install deps: pip install -r requirements.txt")
print("=" * 60)
```

Run it:
```bash
cd streamlit_app
python3 test_apple_silicon.py
```

---

## Quick Fix for Your Friend (M1 Pro)

Send this exact sequence:

```bash
# 1. Clean up
cd ~/Downloads
rm -rf campuspulse

# 2. Fresh clone
git clone <repo-url> campuspulse
cd campuspulse/streamlit_app

# 3. Use Homebrew Python (ensures ARM64)
/opt/homebrew/bin/python3 -m venv venv_arm
source venv_arm/bin/activate

# 4. Verify ARM64
python -c "import platform; print(platform.machine())"
# MUST show: arm64

# 5. Install packages
pip install --upgrade pip
pip install torch torchvision torchaudio
pip install streamlit pandas plotly scikit-learn geopy bcrypt transformers

# 6. Run app
streamlit run app.py

# Should now load without crashes
```

---

## Why M2 Air Works But M1 Pro Doesn't

Both are Apple Silicon, so the issue is **software environment** not hardware:

| Your M2 Air (Works) | Friend's M1 Pro (Doesn't Work) |
|---------------------|--------------------------------|
| ARM64 Python | x86_64 Python (under Rosetta) |
| Native packages | Intel packages (emulated) |
| PyTorch with MPS | PyTorch without MPS or wrong build |
| Fresh environment | Mixed x86/ARM packages |

**Root cause:** Friend likely installed Python or packages that defaulted to Intel (x86_64) builds, which run under Rosetta emulation. This causes crashes with ML libraries.

---

## Prevention: Update requirements.txt

Create `streamlit_app/requirements-apple-silicon.txt`:

```txt
# Requirements for Apple Silicon (M1/M2/M3)
# Install with native ARM64 Python only

# Verify ARM64 first:
# python -c "import platform; print(platform.machine())"
# Must show: arm64

torch>=2.0.0
torchvision>=0.15.0
torchaudio>=2.0.0
streamlit>=1.40.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.0.0
scikit-learn>=1.3.0
geopy>=2.4.0
bcrypt>=4.0.0
transformers>=4.30.0
```

---

## Summary

**Problem:** M1 Pro running Intel (x86_64) Python under Rosetta → crashes
**Solution:** Use ARM64 native Python via Homebrew

**One-liner fix:**
```bash
/opt/homebrew/bin/python3 -m venv venv && source venv/bin/activate && pip install torch streamlit pandas plotly scikit-learn geopy bcrypt transformers && streamlit run app.py
```

This forces use of Homebrew's ARM64 Python, ensuring native execution without Rosetta.
