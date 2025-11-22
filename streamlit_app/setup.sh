#!/bin/bash

# Campus Pulse Setup Script
echo "🎓 Setting up Campus Pulse..."
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment (optional)
read -p "Create a virtual environment? (recommended) [y/N]: " create_venv
if [[ $create_venv =~ ^[Yy]$ ]]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✓ Virtual environment created and activated"
fi

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Dependencies installed successfully!"
else
    echo ""
    echo "✗ Error installing dependencies"
    exit 1
fi

# Create trained_models directory
mkdir -p trained_models
echo "✓ Created trained_models directory"

# Done
echo ""
echo "════════════════════════════════════════"
echo "🎉 Setup complete!"
echo "════════════════════════════════════════"
echo ""
echo "To run Campus Pulse:"
echo "  streamlit run app.py"
echo ""
echo "The app will open at http://localhost:8501"
echo ""
echo "For more information, see README.md or QUICKSTART.md"
echo ""
