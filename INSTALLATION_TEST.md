# Installation & Testing Guide

Step-by-step guide to install and test your YouTube SEO Analyzer.

## 🚀 Quick Installation

### Windows Users

1. **Double-click** `setup.bat`
2. Wait for installation to complete
3. **Double-click** `run.bat` to launch the app

### Mac/Linux Users

1. **Open Terminal** in the project folder
2. Make scripts executable:
   ```bash
   chmod +x setup.sh run.sh
   ```
3. Run setup:
   ```bash
   ./setup.sh
   ```
4. Launch the app:
   ```bash
   ./run.sh
   ```

## 📋 Manual Installation

If the automated scripts don't work:

### Step 1: Verify Python

```bash
# Windows
python --version

# Mac/Linux
python3 --version
```

**Expected output**: `Python 3.9.x` or higher

**If not installed**: Download from [python.org](https://www.python.org/downloads/)

### Step 2: Install Dependencies

```bash
# Windows
pip install -r requirements.txt

# Mac/Linux
pip3 install -r requirements.txt
```

**This installs**:
- ✓ requests (web scraping)
- ✓ beautifulsoup4 (HTML parsing)
- ✓ youtube-transcript-api (transcript extraction)
- ✓ nltk (natural language processing)
- ✓ scikit-learn (machine learning)
- ✓ pytrends (Google Trends API)
- ✓ pandas & numpy (data handling)

### Step 3: Launch Application

```bash
# Windows
python main.py

# Mac/Linux
python3 main.py
```

## 🧪 Testing the Application

### Test 1: Launch Test
**Goal**: Verify the application starts correctly

1. Run the application
2. **Expected**: GUI window opens with "YouTube SEO Analyzer" title
3. **Check**: All 5 tabs are visible (Video Analysis, SEO Suggestions, Trend Analysis, Performance Metrics, Settings)
4. **Status**: ✅ Pass if GUI loads without errors

### Test 2: Basic Analysis Test
**Goal**: Test complete analysis workflow

1. Enter this test URL: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
2. Click "Analyze Video"
3. **Expected Progress**:
   - Status shows "Extracting video data..."
   - Status shows "Analyzing SEO..."
   - Status shows "Analyzing trends..."
   - Status shows "Calculating performance metrics..."
   - Status shows "Analysis complete!"
4. **Check Results**:
   - Video Analysis tab shows video title
   - SEO Suggestions tab shows suggested tags
   - Performance Metrics shows a score (0-100)
5. **Status**: ✅ Pass if analysis completes without errors

### Test 3: Tag Copy Test
**Goal**: Verify tag copying functionality

1. After analysis, go to "SEO Suggestions" tab
2. Click "Copy Tags" button
3. Paste into a text editor (Ctrl+V / Cmd+V)
4. **Expected**: Comma-separated list of tags
5. **Status**: ✅ Pass if tags are copied correctly

### Test 4: Settings Test
**Goal**: Test settings customization

1. Go to "Settings" tab
2. Adjust "Title Optimization" slider to 50%
3. Change "Number of tags" to 20
4. Select region: "GB"
5. Click "Save Settings"
6. **Expected**: "Settings saved successfully!" message
7. Close and reopen the app
8. **Check**: Settings are preserved
9. **Status**: ✅ Pass if settings persist

### Test 5: Trend Analysis Test
**Goal**: Verify trend integration

1. Analyze a recent, popular video
2. Go to "Trend Analysis" tab
3. **Expected**: 
   - List of trending topics
   - Trend-based tag suggestions
   - Trend scores and momentum indicators
4. **Note**: May be limited due to Google Trends rate limits
5. **Status**: ✅ Pass if trend data appears (or graceful error handling)

## 🐛 Common Issues & Solutions

### Issue 1: "Python not found"
**Solution**:
```bash
# Add Python to PATH (Windows)
# 1. Search "Environment Variables" in Start Menu
# 2. Edit PATH
# 3. Add Python installation directory

# Or reinstall Python with "Add to PATH" checked
```

### Issue 2: "Module not found" errors
**Solution**:
```bash
# Reinstall all dependencies
pip install --upgrade -r requirements.txt

# Or install individually
pip install requests beautifulsoup4 youtube-transcript-api nltk scikit-learn pytrends pandas numpy
```

### Issue 3: SSL Certificate errors
**Solution**:
```bash
# Windows
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

# Or update certificates
pip install --upgrade certifi
```

### Issue 4: NLTK data errors
**Solution**:
```python
# Run in Python interactive shell
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

### Issue 5: "Invalid YouTube URL"
**Solution**:
- Copy URL directly from browser address bar
- Ensure URL starts with `https://www.youtube.com/watch?v=`
- Remove any extra parameters after the video ID

### Issue 6: "Trend analysis unavailable"
**Solution**:
- This is normal if you analyze too many videos quickly
- Wait 2-3 minutes between analyses
- Google Trends has rate limits to prevent abuse

### Issue 7: GUI doesn't appear
**Solution**:
```bash
# Check tkinter installation
python -m tkinter

# If error, reinstall Python with tk/tcl support
# Or on Linux:
sudo apt-get install python3-tk
```

## 📊 Test Results Checklist

Copy this checklist and mark completed tests:

```
Installation Tests:
[ ] Python 3.8+ is installed
[ ] All dependencies installed successfully
[ ] No import errors when running main.py

Functionality Tests:
[ ] GUI launches successfully
[ ] All 5 tabs are visible and accessible
[ ] Video URL input accepts YouTube URLs
[ ] Analysis completes without crashes
[ ] Video information is displayed correctly
[ ] SEO tags are generated
[ ] Tags can be copied to clipboard
[ ] Performance metrics show scores
[ ] Settings can be customized
[ ] Settings persist after restart

Optional Tests:
[ ] Trend analysis returns data
[ ] Multiple videos can be analyzed in sequence
[ ] Different regions and timeframes work
[ ] Programmatic usage (example_usage.py) works
```

## 🎯 Performance Benchmarks

Expected performance (may vary by system and internet speed):

| Task | Expected Time |
|------|---------------|
| Application startup | 1-3 seconds |
| Video metadata extraction | 3-5 seconds |
| Transcript retrieval | 2-4 seconds |
| SEO analysis | 1-2 seconds |
| Trend analysis | 5-10 seconds |
| **Total Analysis** | **11-24 seconds** |

**Note**: First run may be slower due to NLTK data downloads.

## 🔍 Detailed Error Diagnosis

If you encounter errors, run the diagnostic script:

```python
# Save as diagnose.py
import sys
print(f"Python version: {sys.version}")

try:
    import requests
    print("✓ requests")
except ImportError:
    print("✗ requests - Run: pip install requests")

try:
    import bs4
    print("✓ beautifulsoup4")
except ImportError:
    print("✗ beautifulsoup4 - Run: pip install beautifulsoup4")

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    print("✓ youtube-transcript-api")
except ImportError:
    print("✗ youtube-transcript-api - Run: pip install youtube-transcript-api")

try:
    import nltk
    print("✓ nltk")
except ImportError:
    print("✗ nltk - Run: pip install nltk")

try:
    import sklearn
    print("✓ scikit-learn")
except ImportError:
    print("✗ scikit-learn - Run: pip install scikit-learn")

try:
    from pytrends.request import TrendReq
    print("✓ pytrends")
except ImportError:
    print("✗ pytrends - Run: pip install pytrends")

try:
    import pandas
    print("✓ pandas")
except ImportError:
    print("✗ pandas - Run: pip install pandas")

try:
    import numpy
    print("✓ numpy")
except ImportError:
    print("✗ numpy - Run: pip install numpy")

print("\nAll required packages are installed!" if all else "Some packages are missing!")
```

Run with: `python diagnose.py`

## 📧 Getting Help

If issues persist:

1. **Check Documentation**: Review README.md and QUICKSTART.md
2. **Search Issues**: Look for similar problems in GitHub Issues
3. **Create Issue**: Provide:
   - Python version (`python --version`)
   - Operating system
   - Full error message
   - Steps to reproduce

## ✅ Success Indicators

You've successfully installed if:

1. ✅ Application launches without errors
2. ✅ You can analyze at least one YouTube video
3. ✅ Tag suggestions are generated
4. ✅ Performance score is calculated
5. ✅ Settings can be saved and loaded

**Congratulations! You're ready to optimize your YouTube content!** 🎉

---

**Next Steps**: Check out [QUICKSTART.md](QUICKSTART.md) for usage tips!

