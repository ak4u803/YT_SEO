"""
Test Script for ML Tag Prediction Installation
This script verifies that ML features are properly installed and working
"""

import sys
import io

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def test_imports():
    """Test if all required libraries can be imported"""
    print("\n" + "=" * 60)
    print("Testing ML Library Imports")
    print("=" * 60 + "\n")
    
    required_libs = {
        'transformers': 'Hugging Face Transformers',
        'sentence_transformers': 'Sentence Transformers',
        'torch': 'PyTorch',
        'sklearn': 'Scikit-learn',
        'numpy': 'NumPy',
        'nltk': 'NLTK'
    }
    
    all_imported = True
    
    for lib, name in required_libs.items():
        try:
            __import__(lib)
            print(f"[OK] {name:30s} - INSTALLED")
        except ImportError as e:
            print(f"[FAIL] {name:30s} - MISSING")
            print(f"   Error: {e}")
            all_imported = False
    
    return all_imported


def test_ml_predictor():
    """Test if ML Tag Predictor can be initialized"""
    print("\n" + "=" * 60)
    print("Testing ML Tag Predictor Module")
    print("=" * 60 + "\n")
    
    try:
        from ml_tag_predictor import MLTagPredictor
        print("[OK] ML Tag Predictor module imported successfully")
        
        print("\nInitializing ML Tag Predictor...")
        print("(This may take a moment on first run as models download)")
        print("-" * 60)
        
        predictor = MLTagPredictor()
        
        if predictor.models_loaded:
            print("[OK] ML models loaded successfully!")
            print(f"   Zero-shot classifier: {'Available' if predictor.zero_shot_classifier else 'Not available'}")
            print(f"   Sentence model: {'Available' if predictor.sentence_model else 'Not available'}")
            return True, predictor
        else:
            print("[WARN] ML Predictor initialized but models not loaded")
            print("   This is normal if transformers library is not installed")
            return False, predictor
            
    except Exception as e:
        print(f"[FAIL] Error initializing ML Tag Predictor: {e}")
        return False, None


def test_tag_prediction(predictor):
    """Test tag prediction with sample data"""
    print("\n" + "=" * 60)
    print("Testing Tag Prediction")
    print("=" * 60 + "\n")
    
    # Sample video data
    test_data = {
        'title': 'How to Learn Python Programming for Beginners',
        'description': 'A comprehensive tutorial on Python programming for complete beginners. '
                      'Learn variables, functions, loops, and more!',
        'transcript_full': 'Hello everyone! In this video we will learn Python programming. '
                          'Python is a powerful and easy to learn programming language. '
                          'We will cover variables, data types, functions, and control flow. '
                          'Python is great for beginners and is used in web development, '
                          'data science, machine learning, and automation.'
    }
    
    print("Test Video Data:")
    print(f"  Title: {test_data['title']}")
    print(f"  Description: {test_data['description'][:60]}...")
    print(f"  Transcript: {test_data['transcript_full'][:60]}...\n")
    
    print("Running ML tag prediction...\n")
    
    try:
        results = predictor.predict_tags(test_data, num_tags=15)
        
        print("[OK] Tag prediction completed successfully!\n")
        
        # Display results
        print("Results:")
        print("-" * 60)
        
        ml_tags = results.get('ml_tags', [])
        if ml_tags:
            print(f"\n📊 Generated {len(ml_tags)} ML tags:")
            for i, tag in enumerate(ml_tags[:10], 1):
                print(f"   {i:2d}. {tag}")
        
        # Category scores
        category_scores = results.get('category_scores', {})
        if category_scores:
            print(f"\n[INFO] Content Categories (Top 5):")
            sorted_categories = sorted(category_scores.items(), key=lambda x: x[1], reverse=True)
            for category, score in sorted_categories[:5]:
                print(f"   • {category:20s} - {score:.1%} confidence")
        
        # Quality metrics
        quality = predictor.analyze_tag_quality(ml_tags)
        print(f"\n📈 Tag Quality Metrics:")
        print(f"   • Quality Score: {quality.get('quality_score', 0):.1f}/100")
        print(f"   • Diversity Score: {quality.get('diversity_score', 0):.1f}%")
        print(f"   • Average Words per Tag: {quality.get('avg_words', 0):.1f}")
        
        # Method used
        method = results.get('method_used', 'Unknown')
        print(f"\n[INFO] Method: {method}")
        
        return True
        
    except Exception as e:
        print(f"[FAIL] Error during tag prediction: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_seo_engine_integration():
    """Test integration with SEO Engine"""
    print("\n" + "=" * 60)
    print("Testing SEO Engine Integration")
    print("=" * 60 + "\n")
    
    try:
        from seo_engine import SEOEngine
        
        print("[OK] SEO Engine imported successfully")
        
        seo = SEOEngine()
        
        if hasattr(seo, 'ml_predictor') and seo.ml_enabled:
            print("[OK] ML Predictor integrated into SEO Engine")
            print(f"   ML enabled: {seo.ml_enabled}")
            return True
        else:
            print("[WARN] SEO Engine initialized without ML support")
            print("   This is normal if ML libraries are not installed")
            return False
            
    except Exception as e:
        print(f"[FAIL] Error testing SEO Engine: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 70)
    print(" " * 15 + "ML FEATURE INSTALLATION TEST")
    print("=" * 70)
    
    # Test 1: Imports
    imports_ok = test_imports()
    
    if not imports_ok:
        print("\n" + "=" * 70)
        print("[WARN] SOME LIBRARIES ARE MISSING")
        print("=" * 70)
        print("\nTo install missing libraries, run:")
        print("  pip install transformers sentence-transformers torch")
        print("\nOr install all requirements:")
        print("  pip install -r requirements.txt")
        return False
    
    # Test 2: ML Predictor
    predictor_ok, predictor = test_ml_predictor()
    
    # Test 3: Tag Prediction
    if predictor_ok and predictor:
        prediction_ok = test_tag_prediction(predictor)
    else:
        print("\n[WARN] Skipping tag prediction test (models not loaded)")
        prediction_ok = False
    
    # Test 4: SEO Engine Integration
    integration_ok = test_seo_engine_integration()
    
    # Final Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"\n{'Library Imports:':<30} {'[PASS]' if imports_ok else '[FAIL]'}")
    print(f"{'ML Predictor Initialization:':<30} {'[PASS]' if predictor_ok else '[PARTIAL]'}")
    print(f"{'Tag Prediction:':<30} {'[PASS]' if prediction_ok else '[SKIP]'}")
    print(f"{'SEO Engine Integration:':<30} {'[PASS]' if integration_ok else '[PARTIAL]'}")
    
    if imports_ok and predictor_ok and prediction_ok and integration_ok:
        print("\n" + "=" * 70)
        print("[SUCCESS] ALL TESTS PASSED!")
        print("=" * 70)
        print("\nML features are fully installed and working!")
        print("\nYou can now:")
        print("  • Run the GUI: python main.py")
        print("  • Use ML tag prediction on YouTube videos")
        print("  • Get AI-powered tag suggestions")
        print("\nFor more information, see ML_TAG_PREDICTION.md")
        return True
    elif imports_ok:
        print("\n" + "=" * 70)
        print("[WARN] PARTIAL SUCCESS")
        print("=" * 70)
        print("\nBasic libraries are installed, but ML models may not be fully loaded.")
        print("This could be due to:")
        print("  • First-time model download in progress")
        print("  • Network connectivity issues")
        print("  • Insufficient disk space")
        print("\nThe application will still work with traditional tag prediction.")
        print("Try running the main application to download models:")
        print("  python main.py")
        return False
    else:
        print("\n" + "=" * 70)
        print("[FAIL] TESTS FAILED")
        print("=" * 70)
        print("\nPlease install the required ML libraries:")
        print("  pip install transformers sentence-transformers torch")
        print("\nFor detailed installation instructions, see INSTALL_ML_FEATURES.md")
        return False


if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

