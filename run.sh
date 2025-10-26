#!/bin/bash
# Quick run script for YouTube SEO Analyzer (Unix/Linux/Mac)

echo "Starting YouTube SEO Analyzer..."
echo ""
python3 main.py

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Failed to start the application"
    echo "Make sure you have run setup.sh first"
fi

