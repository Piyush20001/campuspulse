# Troubleshooting "Illegal Hardware Instruction" Error

## Problem
When running `streamlit run app.py`, the application crashes with:
```
zsh: illegal hardware instruction
```

**Important:** This error occurs on your friend's computer but NOT on yours, indicating a hardware/software environment difference.

---

## Root Cause
The "illegal hardware instruction" error occurs when PyTorch (or NumPy) binaries are compiled with CPU instruction sets (like AVX2, AVX512, SSE4) that your friend's CPU doesn't support.

---

## Solution 1: Install CPU-Only PyTorch (Most Common Fix)

This installs a PyTorch build optimized for older CPUs without advanced instruction sets:

```bash
# Step 1: Uninstall existing PyTorch
pip3 uninstall torch torchvision torchaudio -y

# Step 2: Install CPU-only PyTorch (compatible with older CPUs)
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Step 3: Verify installation
python3 -c "import torch; print(f'PyTorch version: {torch.__version__}')"

# Step 4: Run the app
streamlit run app.py
```

---

## Solution 2: Check CPU Compatibility

Have your friend check their CPU model and instruction set support:

```bash
# On Linux/macOS:
cat /proc/cpuinfo | grep flags | head -1

# Look for these flags:
# - sse4_1, sse4_2 (basic, most CPUs have this)
# - avx, avx2 (common on Intel CPUs from 2013+)
# - avx512 (newer Intel CPUs from 2017+)

# On macOS, alternative method:
sysctl -a | grep machdep.cpu.features
```

**Common scenarios:**
- **Older Intel CPUs (pre-2013):** Lack AVX2 → Use Solution 1
- **Older AMD CPUs (pre-Ryzen):** Lack AVX2 → Use Solution 1
- **Virtual Machines:** May have limited instruction sets → Use Solution 1
- **Apple Silicon (M1/M2):** See Solution 3 below

---

## Solution 3: Apple Silicon (M1/M2/M3 Macs)

If your friend has an Apple Silicon Mac:

```bash
# Install PyTorch with ARM64 support
pip3 uninstall torch torchvision torchaudio -y
pip3 install --upgrade torch torchvision torchaudio

# Verify it's using ARM64
python3 -c "import torch; print(torch.__version__); print(torch.backends.mps.is_available())"
```

---

## Solution 4: Rebuild NumPy from Source (If PyTorch Fix Doesn't Work)

Sometimes NumPy also causes this error:

```bash
# Uninstall prebuilt NumPy
pip3 uninstall numpy -y

# Install NumPy from source (slower but compatible)
pip3 install numpy --no-binary numpy

# Or install an older, more compatible version
pip3 install numpy==1.24.3
```

---

## Solution 5: Use Conda (Recommended for Complex Environments)

Conda handles binary compatibility better than pip:

```bash
# Install Miniconda if not already installed
# Download from: https://docs.conda.io/en/latest/miniconda.html

# Create new environment
conda create -n campuspulse python=3.11 -y
conda activate campuspulse

# Install PyTorch (conda auto-selects compatible build)
conda install pytorch torchvision torchaudio cpuonly -c pytorch -y

# Install other requirements
pip install -r requirements.txt

# Run app
streamlit run app.py
```

---

## Solution 6: Quick Fix - Use Older PyTorch Version

Install an older PyTorch version with fewer CPU requirements:

```bash
pip3 uninstall torch torchvision torchaudio -y
pip3 install torch==2.0.0 torchvision==0.15.0 torchaudio==2.0.0 --index-url https://download.pytorch.org/whl/cpu
```

---

## Diagnostic Commands

Have your friend run these to identify the exact issue:

```bash
# 1. Check Python version
python3 --version

# 2. Check PyTorch installation
python3 -c "import torch; print(torch.__version__); print(torch.__config__.show())"

# 3. Check which PyTorch variant is installed
pip3 show torch | grep "Location"

# 4. Test PyTorch without Streamlit
python3 -c "import torch; x = torch.randn(5, 5); print('PyTorch works:', x.shape)"

# 5. Check NumPy
python3 -c "import numpy as np; print('NumPy version:', np.__version__)"

# 6. Test minimal Streamlit
echo "import streamlit as st; st.write('Hello')" > test_streamlit.py
streamlit run test_streamlit.py
```

---

## Prevention: Create Compatible `requirements.txt`

To avoid this issue for other users, create a more compatible requirements file:

```txt
# requirements-compatible.txt
# CPU-only PyTorch (works on all systems)
torch>=2.0.0
torchvision>=0.15.0
torchaudio>=2.0.0

# Use --extra-index-url when installing:
# pip3 install -r requirements-compatible.txt --extra-index-url https://download.pytorch.org/whl/cpu
```

---

## Still Not Working?

If none of the above work, try these last-resort options:

### Option A: Use Docker
```bash
# On friend's computer
docker run -p 8501:8501 -v $(pwd):/app python:3.11-slim bash -c "
  cd /app &&
  pip install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu &&
  streamlit run app.py
"
```

### Option B: Completely Clean Installation
```bash
# Remove all Python packages
pip3 freeze | xargs pip3 uninstall -y

# Reinstall from scratch
pip3 install --upgrade pip
pip3 install streamlit
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip3 install pandas numpy scikit-learn plotly bcrypt geopy
```

---

## Summary

**Most likely fix for your friend:**
```bash
pip3 uninstall torch torchvision torchaudio -y
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
streamlit run app.py
```

This installs a CPU-only PyTorch build that's compatible with older CPUs and doesn't require AVX2/AVX512 instruction sets.

---

## Share This File

You can share this entire file with your friend. They should start with Solution 1 (CPU-only PyTorch) as it fixes 90% of cases.
