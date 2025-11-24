#!/usr/bin/env python3
"""
Setup Verification Script for Campus Pulse
Run this after cloning to verify all dependencies are installed correctly.
"""

import sys
import importlib
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.11+"""
    version = sys.version_info
    print(f"🔍 Checking Python version...")
    print(f"   Python {version.major}.{version.minor}.{version.micro}")

    if version.major == 3 and version.minor >= 11:
        print("   ✅ Python version is compatible (3.11+)")
        return True
    else:
        print("   ❌ Python version too old. Need 3.11+")
        return False

def check_module(module_name, display_name=None):
    """Check if a Python module is installed"""
    if display_name is None:
        display_name = module_name

    try:
        mod = importlib.import_module(module_name)
        version = getattr(mod, '__version__', 'unknown version')
        print(f"   ✅ {display_name}: {version}")
        return True
    except ImportError:
        print(f"   ❌ {display_name}: NOT INSTALLED")
        return False

def check_dependencies():
    """Check all required Python packages"""
    print(f"\n🔍 Checking Python dependencies...")

    dependencies = [
        ('streamlit', 'Streamlit'),
        ('torch', 'PyTorch'),
        ('pandas', 'Pandas'),
        ('numpy', 'NumPy'),
        ('plotly', 'Plotly'),
        ('sklearn', 'Scikit-learn'),
        ('geopy', 'Geopy'),
        ('bcrypt', 'Bcrypt'),
    ]

    results = []
    for module, name in dependencies:
        results.append(check_module(module, name))

    return all(results)

def check_files():
    """Check if required files exist"""
    print(f"\n🔍 Checking required files...")

    files = [
        ('app.py', 'Main application'),
        ('streamlit_app/models/lstm_crowd_model.pth', 'LSTM model (204KB)'),
        ('streamlit_app/data/crowd_training_data_5000.csv', 'Training data v1'),
        ('streamlit_app/data/crowd_training_data_5000_v2.csv', 'Training data v2'),
        ('requirements.txt', 'Requirements file'),
    ]

    results = []
    for filepath, description in files:
        path = Path(filepath)
        if path.exists():
            size = path.stat().st_size
            size_str = f"{size / 1024:.1f}KB" if size < 1024*1024 else f"{size / (1024*1024):.1f}MB"
            print(f"   ✅ {description}: {size_str}")
            results.append(True)
        else:
            print(f"   ❌ {description}: NOT FOUND")
            results.append(False)

    return all(results)

def test_pytorch():
    """Test PyTorch functionality"""
    print(f"\n🔍 Testing PyTorch...")

    try:
        import torch

        # Test basic tensor operations
        x = torch.randn(5, 5)
        y = x * 2

        print(f"   ✅ PyTorch tensor operations work")

        # Check for CPU
        print(f"   ℹ️  Using device: CPU")

        # Check for AVX support (if available)
        if hasattr(torch, '__config__'):
            print(f"   ℹ️  Build configuration available")

        return True

    except Exception as e:
        print(f"   ❌ PyTorch test failed: {e}")
        return False

def test_model_loading():
    """Test loading the LSTM model"""
    print(f"\n🔍 Testing LSTM model loading...")

    try:
        from streamlit_app.models.lstm_forecaster import LSTMForecaster

        forecaster = LSTMForecaster()
        print(f"   ✅ LSTM model loaded successfully")
        print(f"   ℹ️  Model type: 2-layer LSTM with 64 hidden units")
        return True

    except Exception as e:
        print(f"   ❌ Model loading failed: {e}")
        return False

def check_databases():
    """Check database status"""
    print(f"\n🔍 Checking databases...")

    db_files = [
        'campus_pulse_users.db',
        'campus_pulse_feedback.db',
        'campus_pulse_performance.db',
    ]

    any_exist = False
    for db in db_files:
        path = Path(db)
        if path.exists():
            size = path.stat().st_size / 1024
            print(f"   ✅ {db}: {size:.1f}KB (exists)")
            any_exist = True
        else:
            print(f"   ℹ️  {db}: Not created yet (will auto-create on first run)")

    if not any_exist:
        print(f"\n   📝 Note: Databases don't exist yet - this is NORMAL for fresh installs!")
        print(f"   📝 They will be automatically created when you run: streamlit run app.py")

    return True

def print_next_steps(all_passed):
    """Print next steps based on verification results"""
    print(f"\n{'='*60}")

    if all_passed:
        print("✅ ALL CHECKS PASSED! Setup is complete.")
        print(f"\n📝 Next steps:")
        print(f"   1. Run the app:     streamlit run app.py")
        print(f"   2. Open browser:    http://localhost:8501")
        print(f"   3. Create account:  Click 'Login/Signup' in sidebar")
        print(f"   4. Explore the app: Try all pages and features")
        print(f"\n🎉 Your Campus Pulse installation is ready!")
    else:
        print("❌ SOME CHECKS FAILED. Please fix the issues above.")
        print(f"\n📝 Common fixes:")
        print(f"   • Missing dependencies:  pip3 install -r requirements.txt")
        print(f"   • PyTorch hardware error: pip3 install torch --index-url https://download.pytorch.org/whl/cpu")
        print(f"   • Missing files:         Re-clone the repository")
        print(f"\n📖 See FIRST_TIME_SETUP.md for detailed setup instructions")

    print(f"{'='*60}\n")

def main():
    """Run all verification checks"""
    print("="*60)
    print("Campus Pulse - Setup Verification")
    print("="*60)

    results = []

    # Run all checks
    results.append(check_python_version())
    results.append(check_dependencies())
    results.append(check_files())
    results.append(test_pytorch())
    results.append(test_model_loading())
    results.append(check_databases())  # Informational only

    # Print summary
    all_passed = all(results[:-1])  # Exclude database check from pass/fail
    print_next_steps(all_passed)

    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
