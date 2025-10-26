"""
Example usage of YouTube SEO Analyzer modules
This file demonstrates how to use the analyzer programmatically
"""

from youtube_analyzer import YouTubeAnalyzer
from seo_engine import SEOEngine
from trend_analyzer import TrendAnalyzer

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
    
    # Step 2: Analyze SEO
    print("\nStep 2: Analyzing SEO...")
    seo_results = seo.analyze_seo(video_data)
    print(f"✓ Title Score: {seo_results['title_score']}/100")
    print(f"✓ Description Score: {seo_results['description_score']}/100")
    print(f"✓ Tag Score: {seo_results['tag_score']}/100")
    print(f"✓ Generated {len(seo_results['suggested_tags'])} tag suggestions")
    
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
    
    # Top suggested tags
    print("\n🏷️  Top 15 Suggested Tags:")
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
    
    print("\n" + "=" * 60)
    print("\n✨ Tip: For GUI interface, run: python main.py")
    print("=" * 60 + "\n")

