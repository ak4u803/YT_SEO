#!/bin/bash
# YouTube SEO Analyzer - Unix/Linux/Mac Setup Script

echo "================================================"
echo "YouTube SEO Analyzer - Setup"
echo "================================================"
echo ""

# Check Python installation
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo "Please install Python 3.9 or higher"
    exit 1
fi

python3 --version
echo ""

# Verify Python version >= 3.9
echo "Verifying Python version (>= 3.9)..."
python3 - <<'EOF'
import sys
major, minor = sys.version_info[:2]
print(f"Detected Python {major}.{minor}")
sys.exit(0 if (major > 3 or (major == 3 and minor >= 9)) else 1)
EOF
if [ $? -ne 0 ]; then
    echo "[ERROR] Python 3.9+ is required (SciPy >=1.11 dependency)."
    exit 1
fi

# Upgrade pip
echo "Upgrading pip..."
python3 -m pip install --upgrade pip
echo ""

# Install requirements
echo "Installing dependencies..."
echo "This may take a few minutes..."
echo ""
python3 -m pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Failed to install dependencies"
    echo "Please check your internet connection and try again"
    exit 1
fi

echo ""
echo "================================================"
echo "Setup Complete!"
echo "================================================"
echo ""
echo "To run the application, use:"
echo "    python3 main.py"
echo ""
echo "For help, see README.md or QUICKSTART.md"
echo ""

