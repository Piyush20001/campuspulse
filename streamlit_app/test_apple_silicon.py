#!/usr/bin/env python3
"""
Diagnostic script for Apple Silicon (M1/M2/M3) compatibility
Run this to diagnose why the app crashes or hangs on Apple Silicon Macs
"""
import sys
import platform
import subprocess

def run_command(cmd):
    """Run shell command and return output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
        return result.stdout.strip()
    except:
        return "Error running command"

print("=" * 70)
print("Campus Pulse - Apple Silicon Compatibility Diagnostic")
print("=" * 70)

# Check 1: Architecture (MOST IMPORTANT)
arch = platform.machine()
print(f"\n1. Python Architecture: {arch}")
if arch == "arm64":
    print("   ✅ Native ARM64 (correct for M1/M2/M3)")
elif arch == "x86_64":
    print("   ❌ Intel x86_64 (CRITICAL PROBLEM)")
    print("   🔧 Your Python is running under Rosetta emulation")
    print("   🔧 This causes crashes with ML libraries like PyTorch")
    print("   🔧 Solution: Install ARM64 Python via Homebrew")
    print("      brew install python@3.11")
    print("      /opt/homebrew/bin/python3 -m venv venv_arm")
else:
    print(f"   ⚠️  Unknown architecture: {arch}")

# Check 2: System Architecture
system_arch = run_command("uname -m")
print(f"\n2. System Architecture: {system_arch}")
if system_arch == "arm64":
    print("   ✅ Terminal running in native ARM64 mode")
elif system_arch == "x86_64":
    print("   ⚠️  Terminal running in Rosetta mode")
    print("   🔧 Right-click Terminal.app → Get Info → Uncheck 'Open using Rosetta'")

# Check 3: Python Version
py_version = platform.python_version()
py_major, py_minor = map(int, py_version.split('.')[:2])
print(f"\n3. Python Version: {py_version}")
if (py_major, py_minor) >= (3, 11):
    print("   ✅ Python 3.11+ (recommended)")
elif (py_major, py_minor) >= (3, 9):
    print("   ⚠️  Python 3.9-3.10 (works but 3.11+ recommended)")
else:
    print("   ❌ Python too old, upgrade to 3.11+")

# Check 4: Python Executable Location
python_path = sys.executable
print(f"\n4. Python Location: {python_path}")
if "/opt/homebrew/" in python_path:
    print("   ✅ Homebrew Python (native ARM64)")
elif "/Library/Frameworks/Python.framework/" in python_path:
    print("   ⚠️  Python.org installation (check if universal2)")
elif "/usr/bin/python" in python_path:
    print("   ⚠️  System Python (not recommended)")
else:
    print(f"   ℹ️  Custom installation")

# Check 5: File architecture of Python binary
file_info = run_command(f"file {python_path}")
print(f"\n5. Python Binary Info:")
if "arm64" in file_info:
    print("   ✅ Python binary is ARM64 native")
elif "x86_64" in file_info:
    print("   ❌ Python binary is Intel x86_64")
    if "universal" in file_info:
        print("   ℹ️  Universal binary (contains both arm64 and x86_64)")
print(f"   {file_info}")

# Check 6: PyTorch
print(f"\n6. PyTorch Installation:")
try:
    import torch
    print(f"   Version: {torch.__version__}")
    print(f"   Location: {torch.__file__}")

    # Check MPS support
    mps_available = torch.backends.mps.is_available()
    mps_built = torch.backends.mps.is_built()

    print(f"   MPS Available: {mps_available}")
    print(f"   MPS Built: {mps_built}")

    if mps_available and mps_built:
        print("   ✅ PyTorch with Apple Silicon GPU support (MPS)")
    elif not mps_built:
        print("   ⚠️  PyTorch without MPS support")
        print("   🔧 Reinstall: pip uninstall torch -y && pip install torch")
    else:
        print("   ⚠️  MPS not available on this system")

    # Test tensor creation
    try:
        x = torch.randn(10, 10)
        y = x @ x.T
        print("   ✅ Basic PyTorch operations work")
    except Exception as e:
        print(f"   ❌ PyTorch tensor operations failed: {e}")

except ImportError:
    print("   ❌ PyTorch NOT INSTALLED")
    print("   🔧 Install: pip install torch torchvision torchaudio")
except Exception as e:
    print(f"   ❌ PyTorch ERROR: {e}")
    print("   🔧 This is likely causing the crash!")

# Check 7: NumPy
print(f"\n7. NumPy:")
try:
    import numpy as np
    print(f"   Version: {np.__version__}")

    # Test operations
    arr = np.random.randn(100, 100)
    result = arr @ arr.T
    print("   ✅ NumPy operations work")
except ImportError:
    print("   ❌ NumPy NOT INSTALLED")
except Exception as e:
    print(f"   ❌ NumPy ERROR: {e}")

# Check 8: Streamlit
print(f"\n8. Streamlit:")
try:
    import streamlit
    print(f"   Version: {streamlit.__version__}")
    print("   ✅ Streamlit installed")
except ImportError:
    print("   ❌ Streamlit NOT INSTALLED")
    print("   🔧 Install: pip install streamlit")

# Check 9: scikit-learn
print(f"\n9. scikit-learn:")
try:
    import sklearn
    print(f"   Version: {sklearn.__version__}")
    print("   ✅ scikit-learn installed")
except ImportError:
    print("   ❌ scikit-learn NOT INSTALLED")
    print("   🔧 Install: pip install scikit-learn")
except Exception as e:
    print(f"   ❌ scikit-learn ERROR: {e}")

# Check 10: transformers
print(f"\n10. transformers:")
try:
    import transformers
    print(f"    Version: {transformers.__version__}")
    print("    ✅ transformers installed")
except ImportError:
    print("    ⚠️  transformers NOT INSTALLED (optional)")
except Exception as e:
    print(f"    ❌ transformers ERROR: {e}")

# Check 11: Other dependencies
print(f"\n11. Other Dependencies:")
deps = [
    ('pandas', 'pandas'),
    ('plotly', 'plotly'),
    ('geopy', 'geopy'),
    ('bcrypt', 'bcrypt'),
]

for import_name, display_name in deps:
    try:
        module = __import__(import_name)
        version = getattr(module, '__version__', 'unknown')
        print(f"    ✅ {display_name}: {version}")
    except ImportError:
        print(f"    ❌ {display_name}: NOT INSTALLED")

# Check 12: LSTM Model Loading
print(f"\n12. LSTM Model Test:")
try:
    import os
    import sys
    # Add parent directory to path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    from models.lstm_forecaster import CrowdForecaster
    print("    Loading LSTM model...")
    forecaster = CrowdForecaster()
    print("    ✅ LSTM model loaded successfully")
except FileNotFoundError as e:
    print(f"    ❌ Model file not found: {e}")
except Exception as e:
    print(f"    ❌ LSTM model loading failed: {e}")
    print("    🔧 This is likely why the app hangs!")

# Check 13: Memory and CPU
print(f"\n13. System Resources:")
try:
    import psutil
    mem = psutil.virtual_memory()
    print(f"    Total RAM: {mem.total / (1024**3):.1f} GB")
    print(f"    Available RAM: {mem.available / (1024**3):.1f} GB")
    print(f"    CPU Count: {psutil.cpu_count()}")
except ImportError:
    print("    ℹ️  Install psutil for system info: pip install psutil")

# Summary and Recommendations
print("\n" + "=" * 70)
print("SUMMARY AND RECOMMENDATIONS")
print("=" * 70)

issues = []
fixes = []

if arch != "arm64":
    issues.append("❌ CRITICAL: Python running in x86_64/Rosetta mode")
    fixes.append("1. Install Homebrew: /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
    fixes.append("2. Install ARM64 Python: brew install python@3.11")
    fixes.append("3. Create venv: /opt/homebrew/bin/python3 -m venv venv_arm")
    fixes.append("4. Activate: source venv_arm/bin/activate")
    fixes.append("5. Install deps: pip install torch streamlit pandas plotly scikit-learn geopy bcrypt")

if arch == "arm64":
    print("\n✅ Python architecture is correct (ARM64)")

    try:
        import torch
        if not torch.backends.mps.is_built():
            issues.append("⚠️  PyTorch without MPS support")
            fixes.append("Reinstall PyTorch: pip uninstall torch -y && pip install torch")
    except:
        issues.append("❌ PyTorch not installed or broken")
        fixes.append("Install PyTorch: pip install torch torchvision torchaudio")

if not issues:
    print("\n✅ All checks passed!")
    print("\nIf app still crashes or hangs:")
    print("1. Check terminal output when running: streamlit run app.py")
    print("2. Look for specific error messages or tracebacks")
    print("3. Try: streamlit run app.py --server.port 8502")
    print("4. Try different browser (Chrome instead of Safari)")
    print("\nFor stuck white screen:")
    print("1. Hard refresh browser: Cmd+Shift+R")
    print("2. Clear browser cache")
    print("3. Check browser console for errors (Cmd+Option+I)")
else:
    print(f"\n❌ Found {len(issues)} issue(s):")
    for issue in issues:
        print(f"   {issue}")

    print(f"\n🔧 FIXES:")
    for i, fix in enumerate(fixes, 1):
        print(f"   {fix}")

print("\n" + "=" * 70)
print("Save this output and share with support if issues persist")
print("=" * 70)
