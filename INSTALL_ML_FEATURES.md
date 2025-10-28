# Installing ML Features - Quick Guide

## 🚀 Quick Start

To enable Machine Learning-based tag prediction in the YouTube SEO Analyzer, follow these simple steps:

### Step 1: Install ML Dependencies

Open your terminal/command prompt and run:

```bash
pip install transformers sentence-transformers torch
```

**Note**: This will download approximately 1.7GB of data for the ML models on first run.

### Step 2: Run the Application

```bash
python main.py
```

### Step 3: First-Time Model Download

The first time you analyze a video with ML features enabled:
- Models will automatically download (5-10 minutes)
- You'll see: "Loading ML models (this may take a moment on first run)..."
- Models are cached locally and won't need to be re-downloaded

### Step 4: Use ML Tag Prediction

1. Enter a YouTube URL
2. Click "Analyze Video"
3. Go to the "SEO Suggestions" tab
4. See ML-Predicted Tags at the top! 🎉

## 📋 System Requirements

### Minimum Requirements
- **Python**: 3.9 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Disk Space**: 2GB free (for models)
- **Internet**: Required for first-time model download only

### Recommended Requirements
- **Python**: 3.10+
- **RAM**: 8GB or more
- **Disk Space**: 5GB free
- **CPU**: Multi-core processor (for faster inference)

## 🔧 Installation Options

### Option 1: Install Everything (Recommended)

```bash
pip install -r requirements.txt
```

This installs all dependencies including ML features.

### Option 2: Install ML Features Only

If you already have the base application:

```bash
pip install transformers sentence-transformers torch
```

### Option 3: GPU Acceleration (Optional, for faster inference)

If you have an NVIDIA GPU with CUDA:

```bash
# Install PyTorch with CUDA support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Then install other ML libraries
pip install transformers sentence-transformers
```

**Note**: GPU acceleration is optional. The app works fine with CPU-only inference.

## 🐛 Troubleshooting

### "No module named 'transformers'"

**Solution**:
```bash
pip install transformers sentence-transformers torch
```

### "Error loading ML models"

**Possible causes**:
1. Insufficient disk space
2. Network connection issues
3. Firewall blocking downloads

**Solutions**:
1. Free up 2GB+ disk space
2. Check your internet connection
3. Temporarily disable firewall for the download
4. Try downloading from a different network

### "ML tag prediction not available"

This message appears when ML libraries are not installed. The app still works with traditional tag prediction.

**Solution**:
```bash
pip install transformers sentence-transformers torch
```

### Installation is taking too long

**On Windows**:
```powershell
# Use pip with verbose output to see progress
pip install -v transformers sentence-transformers torch
```

**On Linux/Mac**:
```bash
pip install -v transformers sentence-transformers torch
```

The installation may take 10-15 minutes depending on your internet speed.

### "Could not find a version that satisfies the requirement"

**Cause**: Python version too old

**Solution**: Upgrade Python to 3.9+
```bash
python --version  # Check current version
```

Download latest Python from: https://www.python.org/downloads/

## 🎯 Verifying Installation

To verify ML features are installed correctly:

### Test Script

Create a file `test_ml.py`:

```python
# test_ml.py
try:
    from ml_tag_predictor import MLTagPredictor
    
    predictor = MLTagPredictor()
    
    # Test with dummy data
    test_data = {
        'title': 'How to Learn Python Programming',
        'description': 'A comprehensive tutorial on Python',
        'transcript_full': 'In this video we will learn Python programming'
    }
    
    results = predictor.predict_tags(test_data, num_tags=5)
    
    print("✅ ML Features installed successfully!")
    print(f"Generated {len(results['ml_tags'])} tags")
    print(f"Tags: {', '.join(results['ml_tags'][:5])}")
    
except ImportError as e:
    print("❌ ML libraries not installed")
    print(f"Error: {e}")
    print("\nInstall with: pip install transformers sentence-transformers torch")
    
except Exception as e:
    print("⚠️ ML features partially installed")
    print(f"Error: {e}")
```

Run the test:
```bash
python test_ml.py
```

Expected output:
```
Loading ML models (this may take a moment on first run)...
ML models loaded successfully!
✅ ML Features installed successfully!
Generated 5 tags
Tags: tutorial, education, programming, python, coding
```

## 📊 Storage Information

### Where are models stored?

Models are cached in:
- **Windows**: `C:\Users\YourName\.cache\huggingface\`
- **Linux**: `~/.cache/huggingface/`
- **Mac**: `~/Library/Caches/huggingface/`

### How much space do they use?

| Model | Size | Purpose |
|-------|------|---------|
| facebook/bart-large-mnli | ~1.6GB | Category classification |
| all-MiniLM-L6-v2 | ~90MB | Semantic similarity |
| **Total** | **~1.7GB** | |

### Can I delete models?

Yes, but they'll need to be re-downloaded on next use:

**Windows**:
```powershell
rmdir /s C:\Users\YourName\.cache\huggingface\
```

**Linux/Mac**:
```bash
rm -rf ~/.cache/huggingface/
```

## 🌐 Offline Usage

After initial download, ML features work completely offline!

1. Run the app once with internet (downloads models)
2. Models are cached locally
3. Future use works without internet connection
4. Only YouTube video analysis requires internet

## 🔄 Updating ML Libraries

To update to the latest versions:

```bash
pip install --upgrade transformers sentence-transformers torch
```

**Note**: Updates may require re-downloading models.

## 🆘 Still Having Issues?

### Check Python Version
```bash
python --version
```
Must be 3.9 or higher.

### Check Pip Version
```bash
pip --version
```
Update if needed:
```bash
python -m pip install --upgrade pip
```

### Virtual Environment (Recommended)

Using a virtual environment prevents conflicts:

**Windows**:
```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

**Linux/Mac**:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Clean Install

If all else fails, try a clean installation:

```bash
# 1. Uninstall existing packages
pip uninstall transformers sentence-transformers torch -y

# 2. Clear pip cache
pip cache purge

# 3. Reinstall
pip install transformers sentence-transformers torch
```

## 📞 Getting Help

If you're still having issues:

1. **Check the error message** - It often tells you exactly what's wrong
2. **Search existing issues** on GitHub
3. **Create a new issue** with:
   - Your Python version (`python --version`)
   - Your OS (Windows/Linux/Mac)
   - Full error message
   - What you've already tried

## ✅ Success Checklist

- [ ] Python 3.9+ installed
- [ ] 2GB+ free disk space
- [ ] Internet connection available (for first run)
- [ ] ML libraries installed (`pip install transformers sentence-transformers torch`)
- [ ] Models downloaded (happens automatically on first run)
- [ ] ML tag prediction working in the app

## 🎉 You're All Set!

Once installed, you'll have:
- ✅ AI-powered tag prediction
- ✅ Zero-shot content categorization
- ✅ Semantic similarity analysis
- ✅ Clustering-based tag discovery
- ✅ Tag quality metrics
- ✅ All running locally on your computer!

Enjoy using ML-powered tag prediction! 🚀

---

**Note**: The ML features are completely optional. The app works fine without them using traditional NLP methods.

