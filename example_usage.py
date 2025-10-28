"""
Example usage of YouTube SEO Analyzer modules
This file demonstrates how to use the analyzer programmatically
"""

from youtube_analyzer import YouTubeAnalyzer
from seo_engine import SEOEngine
from trend_analyzer import TrendAnalyzer
from ml_tag_predictor import MLTagPredictor

def analyze_video_programmatically(video_url):
    """
    Example of how to use the analyzer without the GUI
    """
    print("=" * 60)
    print("YouTube SEO Analyzer - Programmatic Example")
    print("=" * 60)
    
    # Initialize analyzers
    youtube = YouTubeAnalyzer()
    seo = SEOEngine()
    trends = TrendAnalyzer()
    
    print(f"\n🎥 Analyzing video: {video_url}\n")
    
    # Step 1: Extract video data
    print("Step 1: Extracting video data...")
    try:
        video_data = youtube.analyze_video(video_url)
        print(f"✓ Title: {video_data.get('title', 'N/A')}")
        print(f"✓ Channel: {video_data.get('channel', 'N/A')}")
        print(f"✓ Views: {video_data.get('views', 0):,}")
        print(f"✓ Current tags: {len(video_data.get('tags', []))}")
    except Exception as e:
        print(f"✗ Error: {e}")
        return
    
    # Step 2: Analyze SEO (includes ML predictions)
    print("\nStep 2: Analyzing SEO...")
    seo_results = seo.analyze_seo(video_data)
    print(f"✓ Title Score: {seo_results['title_score']}/100")
    print(f"✓ Description Score: {seo_results['description_score']}/100")
    print(f"✓ Tag Score: {seo_results['tag_score']}/100")
    print(f"✓ Generated {len(seo_results['suggested_tags'])} traditional tag suggestions")
    
    # ML tag predictions
    ml_tags = seo_results.get('ml_tags', [])
    if ml_tags:
        print(f"✓ Generated {len(ml_tags)} ML-predicted tags")
        ml_method = seo_results.get('ml_method', 'N/A')
        print(f"✓ ML Method: {ml_method}")
        
        # Show ML quality metrics
        ml_quality = seo_results.get('ml_quality_metrics', {})
        if ml_quality:
            print(f"✓ ML Tag Quality: {ml_quality.get('quality_score', 0):.1f}/100")
            print(f"✓ ML Tag Diversity: {ml_quality.get('diversity_score', 0):.1f}%")
    else:
        print("⚠ ML tag prediction not available (install: pip install transformers sentence-transformers torch)")
    
    # Step 3: Analyze trends
    print("\nStep 3: Analyzing trends...")
    try:
        trend_results = trends.analyze_trends(video_data, region='US', timeframe='7d')
        print(f"✓ Trend Score: {trend_results['trend_score']}/100")
        print(f"✓ Found {len(trend_results['trending_topics'])} trending topics")
        print(f"✓ Generated {len(trend_results['trend_tags'])} trend-based tags")
    except Exception as e:
        print(f"⚠ Trend analysis limited: {e}")
        trend_results = {'trend_score': 50, 'trending_topics': [], 'trend_tags': []}
    
    # Display results
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    
    # Overall score (simplified calculation)
    overall = (
        seo_results['title_score'] * 0.2 +
        seo_results['description_score'] * 0.15 +
        seo_results['tag_score'] * 0.25 +
        seo_results['content_score'] * 0.2 +
        trend_results['trend_score'] * 0.2
    )
    
    print(f"\n🎯 Overall SEO Score: {int(overall)}/100")
    
    # ML-predicted tags
    if seo_results.get('ml_tags'):
        print("\n🤖 Top 15 ML-Predicted Tags:")
        for i, tag in enumerate(seo_results['ml_tags'][:15], 1):
            print(f"   {i}. {tag}")
        
        # Show explanations for top tags
        ml_explanations = seo_results.get('ml_tag_explanations', {})
        if ml_explanations:
            print("\n   Tag Explanations (Top 3):")
            for tag, explanation in list(ml_explanations.items())[:3]:
                print(f"   • {tag}: {explanation}")
    
    # Traditional suggested tags
    print("\n🏷️  Top 15 Traditional Suggested Tags:")
    for i, tag in enumerate(seo_results['suggested_tags'][:15], 1):
        print(f"   {i}. {tag}")
    
    # Trending topics
    if trend_results['trending_topics']:
        print("\n📈 Top Trending Topics:")
        for topic in trend_results['trending_topics'][:5]:
            print(f"   • {topic['name']} (Score: {topic['score']}, {topic['trend']})")
    
    # Recommendations
    if seo_results['recommendations']:
        print("\n💡 Top Recommendations:")
        for i, rec in enumerate(seo_results['recommendations'][:3], 1):
            print(f"   {i}. {rec}")
    
    print("\n" + "=" * 60)
    print("Analysis complete!")
    print("=" * 60)


def batch_analyze_videos(video_urls):
    """
    Example of batch analysis for multiple videos
    """
    print("\n🔄 Batch Analysis Mode\n")
    
    youtube = YouTubeAnalyzer()
    seo = SEOEngine()
    
    results = []
    
    for i, url in enumerate(video_urls, 1):
        print(f"Analyzing video {i}/{len(video_urls)}...")
        try:
            video_data = youtube.analyze_video(url)
            seo_results = seo.analyze_seo(video_data)
            
            results.append({
                'url': url,
                'title': video_data.get('title', 'Unknown'),
                'title_score': seo_results['title_score'],
                'description_score': seo_results['description_score'],
                'tag_score': seo_results['tag_score'],
                'tags': seo_results['suggested_tags'][:10]
            })
            
            print(f"✓ {video_data.get('title', 'Unknown')}")
            
        except Exception as e:
            print(f"✗ Error: {e}")
            continue
    
    # Display summary
    print("\n" + "=" * 60)
    print("BATCH ANALYSIS SUMMARY")
    print("=" * 60)
    
    for result in results:
        print(f"\n📹 {result['title']}")
        print(f"   Title: {result['title_score']}/100")
        print(f"   Description: {result['description_score']}/100")
        print(f"   Tags: {result['tag_score']}/100")
        print(f"   Top tags: {', '.join(result['tags'][:5])}")


def compare_videos(url1, url2):
    """
    Example of comparing two videos
    """
    print("\n🔀 Video Comparison Mode\n")
    
    youtube = YouTubeAnalyzer()
    seo = SEOEngine()
    
    # Analyze both videos
    print("Analyzing first video...")
    data1 = youtube.analyze_video(url1)
    seo1 = seo.analyze_seo(data1)
    
    print("Analyzing second video...")
    data2 = youtube.analyze_video(url2)
    seo2 = seo.analyze_seo(data2)
    
    # Compare
    print("\n" + "=" * 60)
    print("COMPARISON RESULTS")
    print("=" * 60)
    
    print(f"\n📹 Video 1: {data1.get('title', 'Unknown')}")
    print(f"   Views: {data1.get('views', 0):,}")
    print(f"   Title Score: {seo1['title_score']}/100")
    print(f"   Tag Score: {seo1['tag_score']}/100")
    
    print(f"\n📹 Video 2: {data2.get('title', 'Unknown')}")
    print(f"   Views: {data2.get('views', 0):,}")
    print(f"   Title Score: {seo2['title_score']}/100")
    print(f"   Tag Score: {seo2['tag_score']}/100")
    
    print("\n📊 Winner:")
    if seo1['tag_score'] > seo2['tag_score']:
        print("   Video 1 has better SEO optimization")
    elif seo2['tag_score'] > seo1['tag_score']:
        print("   Video 2 has better SEO optimization")
    else:
        print("   Both videos are equally optimized")


def ml_tag_prediction_example(video_url):
    """
    Example demonstrating ML-based tag prediction
    """
    print("\n" + "=" * 60)
    print("ML TAG PREDICTION EXAMPLE")
    print("=" * 60)
    
    # Initialize analyzers
    youtube = YouTubeAnalyzer()
    ml_predictor = MLTagPredictor()
    
    print(f"\n🎥 Analyzing video: {video_url}\n")
    
    # Extract video data
    print("Step 1: Extracting video data...")
    video_data = youtube.analyze_video(video_url)
    print(f"✓ Title: {video_data.get('title', 'N/A')}")
    
    # Use ML predictor directly
    print("\nStep 2: Running ML tag prediction...")
    ml_results = ml_predictor.predict_tags(video_data, num_tags=30)
    
    # Display results
    print("\n" + "=" * 60)
    print("ML PREDICTION RESULTS")
    print("=" * 60)
    
    print(f"\n🎯 Method Used: {ml_results.get('method_used', 'N/A')}")
    
    # Category scores (zero-shot classification)
    category_scores = ml_results.get('category_scores', {})
    if category_scores:
        print("\n📊 Content Categories (Zero-Shot Classification):")
        for category, score in sorted(category_scores.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"   • {category}: {score:.1%} confidence")
    
    # Semantic tags
    semantic_tags = ml_results.get('semantic_tags', [])
    if semantic_tags:
        print(f"\n🔍 Semantic Tags ({len(semantic_tags)}):")
        print(f"   {', '.join(semantic_tags[:10])}")
    
    # Clustered tags
    clustered_tags = ml_results.get('clustered_tags', [])
    if clustered_tags:
        print(f"\n🎯 Clustered Tags ({len(clustered_tags)}):")
        print(f"   {', '.join(clustered_tags)}")
    
    # All ML tags
    ml_tags = ml_results.get('ml_tags', [])
    print(f"\n🤖 All ML-Predicted Tags ({len(ml_tags)}):")
    for i, tag in enumerate(ml_tags[:20], 1):
        print(f"   {i}. {tag}")
    
    # Quality analysis
    print("\n📈 Tag Quality Analysis:")
    quality = ml_predictor.analyze_tag_quality(ml_tags)
    print(f"   • Quality Score: {quality.get('quality_score', 0):.1f}/100")
    print(f"   • Diversity Score: {quality.get('diversity_score', 0):.1f}%")
    print(f"   • Average Words per Tag: {quality.get('avg_words', 0):.1f}")
    print(f"   • Has Categories: {'✓' if quality.get('has_categories') else '✗'}")
    print(f"   • Has Specific Tags: {'✓' if quality.get('has_specific') else '✗'}")
    
    # Get explanations
    explanations = ml_predictor.get_tag_explanations(ml_tags[:5], video_data)
    if explanations:
        print("\n💡 Tag Explanations (Top 5):")
        for tag, explanation in explanations.items():
            print(f"   • {tag}:")
            print(f"     {explanation}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    # Example 1: Single video analysis
    print("\n" + "=" * 60)
    print("EXAMPLE 1: Single Video Analysis")
    print("=" * 60)
    
    # Replace with an actual YouTube video URL
    example_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    print("\nTo use this example, replace 'example_url' with a real YouTube URL")
    print("Then uncomment the line below:\n")
    print(f"# analyze_video_programmatically('{example_url}')")
    
    # Example 2: Batch analysis
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Batch Analysis")
    print("=" * 60)
    
    print("\nTo analyze multiple videos at once:")
    print("""
# video_list = [
#     "https://www.youtube.com/watch?v=VIDEO1",
#     "https://www.youtube.com/watch?v=VIDEO2",
#     "https://www.youtube.com/watch?v=VIDEO3"
# ]
# batch_analyze_videos(video_list)
    """)
    
    # Example 3: Compare videos
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Video Comparison")
    print("=" * 60)
    
    print("\nTo compare two videos:")
    print("""
# url1 = "https://www.youtube.com/watch?v=VIDEO1"
# url2 = "https://www.youtube.com/watch?v=VIDEO2"
# compare_videos(url1, url2)
    """)
    
    # Example 4: ML Tag Prediction
    print("\n" + "=" * 60)
    print("EXAMPLE 4: ML-Based Tag Prediction (NEW!)")
    print("=" * 60)
    
    print("\nTo use ML tag prediction:")
    print("""
# example_url = "https://www.youtube.com/watch?v=YOUR_VIDEO"
# ml_tag_prediction_example(example_url)
    """)
    
    print("\nNote: Requires installation of ML libraries:")
    print("  pip install transformers sentence-transformers torch")
    
    print("\n" + "=" * 60)
    print("\n✨ Tip: For GUI interface, run: python main.py")
    print("=" * 60 + "\n")

