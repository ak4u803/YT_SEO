"""
Trend Analyzer Module
Analyzes current trends and suggests tags based on trending topics
"""

from pytrends.request import TrendReq
import time
import random
from datetime import datetime, timedelta
import re

class TrendAnalyzer:
    def __init__(self):
        # Initialize pytrends
        self.pytrends = TrendReq(hl='en-US', tz=360)
        self.trend_cache = {}
        self.cache_duration = 3600  # Cache for 1 hour
    
    def analyze_trends(self, video_data, region='US', timeframe='7d'):
        """Main trend analysis method"""
        results = {
            'trending_topics': [],
            'trend_tags': [],
            'trend_score': 0,
            'trend_feedback': ''
        }
        
        try:
            # Extract keywords from video
            keywords = self.extract_video_keywords(video_data)
            
            if not keywords:
                results['trend_feedback'] = 'Could not extract keywords for trend analysis'
                return results
            
            # Analyze trends for keywords
            trending_topics = self.get_trending_topics(keywords, region, timeframe)
            results['trending_topics'] = trending_topics
            
            # Get related queries
            related_tags = self.get_related_trends(keywords[:3], region)
            results['trend_tags'] = related_tags
            
            # Calculate trend score
            score, feedback = self.calculate_trend_score(video_data, trending_topics, related_tags)
            results['trend_score'] = score
            results['trend_feedback'] = feedback
            
        except Exception as e:
            print(f"Error in trend analysis: {e}")
            results['trend_feedback'] = f'Trend analysis unavailable: {str(e)}'
            results['trend_score'] = 50  # Neutral score
        
        return results
    
    def extract_video_keywords(self, video_data):
        """Extract main keywords from video for trend search"""
        keywords = []
        
        # Get keywords from title
        title = video_data.get('title', '')
        if title:
            # Extract meaningful words from title
            title_words = self.extract_meaningful_words(title)
            keywords.extend(title_words[:5])
        
        # Get keywords from tags
        tags = video_data.get('tags', [])
        if tags:
            # Use first few tags as keywords
            keywords.extend(tags[:5])
        
        # Get keywords from description
        description = video_data.get('description', '')
        if description:
            desc_words = self.extract_meaningful_words(description)
            keywords.extend(desc_words[:3])
        
        # Clean and deduplicate
        cleaned_keywords = []
        seen = set()
        
        for keyword in keywords:
            keyword = keyword.strip().lower()
            if keyword and len(keyword) > 2 and keyword not in seen:
                seen.add(keyword)
                cleaned_keywords.append(keyword)
        
        return cleaned_keywords[:10]  # Return top 10 keywords
    
    def extract_meaningful_words(self, text):
        """Extract meaningful words from text"""
        if not text:
            return []
        
        # Common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                     'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
                     'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
                     'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that',
                     'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
                     'my', 'your', 'his', 'her', 'its', 'our', 'their', 'what', 'which',
                     'who', 'when', 'where', 'why', 'how', 'video', 'youtube'}
        
        # Clean text
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        words = text.split()
        
        # Filter meaningful words
        meaningful = [w for w in words 
                     if w not in stop_words 
                     and len(w) > 2 
                     and not w.isdigit()]
        
        return meaningful
    
    def get_trending_topics(self, keywords, region='US', timeframe='7d'):
        """Get trending topics related to keywords"""
        trending_topics = []
        
        try:
            # Map timeframe to pytrends format
            timeframe_map = {
                '1d': 'now 1-d',
                '7d': 'now 7-d',
                '30d': 'today 1-m',
                '90d': 'today 3-m'
            }
            
            tf = timeframe_map.get(timeframe, 'now 7-d')
            
            # Get interest over time for each keyword
            for keyword in keywords[:5]:  # Limit to prevent rate limiting
                try:
                    # Build payload
                    self.pytrends.build_payload(
                        [keyword],
                        cat=0,
                        timeframe=tf,
                        geo=region
                    )
                    
                    # Get interest over time
                    interest_df = self.pytrends.interest_over_time()
                    
                    if not interest_df.empty and keyword in interest_df.columns:
                        # Calculate average interest
                        avg_interest = interest_df[keyword].mean()
                        
                        # Get recent trend
                        recent_values = interest_df[keyword].tail(3).values
                        if len(recent_values) >= 2:
                            trend_direction = 'Rising' if recent_values[-1] > recent_values[0] else 'Falling'
                        else:
                            trend_direction = 'Stable'
                        
                        trending_topics.append({
                            'name': keyword,
                            'score': int(avg_interest),
                            'trend': trend_direction
                        })
                    
                    # Small delay to avoid rate limiting
                    time.sleep(random.uniform(0.5, 1.5))
                    
                except Exception as e:
                    print(f"Error getting trends for {keyword}: {e}")
                    continue
            
            # Sort by score
            trending_topics.sort(key=lambda x: x['score'], reverse=True)
            
        except Exception as e:
            print(f"Error in get_trending_topics: {e}")
        
        return trending_topics
    
    def get_related_trends(self, keywords, region='US'):
        """Get related trending queries"""
        related_tags = []
        
        try:
            for keyword in keywords[:3]:  # Limit to prevent rate limiting
                try:
                    # Build payload
                    self.pytrends.build_payload(
                        [keyword],
                        cat=0,
                        timeframe='now 7-d',
                        geo=region
                    )
                    
                    # Get related queries
                    related_queries = self.pytrends.related_queries()
                    
                    if keyword in related_queries:
                        # Get rising queries
                        rising = related_queries[keyword].get('rising')
                        if rising is not None and not rising.empty:
                            for idx, row in rising.head(5).iterrows():
                                query = row['query']
                                value = row['value']
                                
                                related_tags.append({
                                    'tag': query,
                                    'reason': f'Rising trend related to "{keyword}" (+{value}%)',
                                    'score': value if isinstance(value, (int, float)) else 100
                                })
                        
                        # Get top queries if no rising queries
                        if not related_tags:
                            top = related_queries[keyword].get('top')
                            if top is not None and not top.empty:
                                for idx, row in top.head(5).iterrows():
                                    query = row['query']
                                    value = row['value']
                                    
                                    related_tags.append({
                                        'tag': query,
                                        'reason': f'Top search related to "{keyword}"',
                                        'score': value if isinstance(value, (int, float)) else 50
                                    })
                    
                    # Small delay to avoid rate limiting
                    time.sleep(random.uniform(1.0, 2.0))
                    
                except Exception as e:
                    print(f"Error getting related queries for {keyword}: {e}")
                    continue
            
            # Sort by score
            related_tags.sort(key=lambda x: x['score'], reverse=True)
            
            # Remove duplicates
            seen = set()
            unique_tags = []
            for tag in related_tags:
                tag_lower = tag['tag'].lower()
                if tag_lower not in seen:
                    seen.add(tag_lower)
                    unique_tags.append(tag)
            
            related_tags = unique_tags[:15]  # Return top 15
            
        except Exception as e:
            print(f"Error in get_related_trends: {e}")
        
        return related_tags
    
    def calculate_trend_score(self, video_data, trending_topics, related_tags):
        """Calculate how well the video aligns with trends"""
        score = 0
        feedback_points = []
        
        # Check if video uses trending keywords
        video_tags = set(tag.lower() for tag in video_data.get('tags', []))
        video_title = video_data.get('title', '').lower()
        video_desc = video_data.get('description', '').lower()
        
        # Check trending topics in video content
        trending_matches = 0
        for topic in trending_topics:
            topic_name = topic['name'].lower()
            if (topic_name in video_title or 
                topic_name in video_desc or 
                topic_name in video_tags):
                trending_matches += 1
                score += 15
        
        if trending_matches > 0:
            feedback_points.append(f'✓ Video uses {trending_matches} trending keyword(s)')
        else:
            feedback_points.append('⚠ Video does not use current trending keywords')
        
        # Check if video tags match related trends
        related_matches = 0
        for tag_info in related_tags[:10]:
            related_tag = tag_info['tag'].lower()
            # Check for partial matches
            if (any(related_tag in vt for vt in video_tags) or
                related_tag in video_title or
                related_tag in video_desc):
                related_matches += 1
                score += 5
        
        if related_matches > 0:
            feedback_points.append(f'✓ Video aligns with {related_matches} related trend(s)')
        else:
            feedback_points.append('⚠ Consider incorporating trending related topics')
        
        # Check trend momentum
        if trending_topics:
            rising_topics = [t for t in trending_topics if t.get('trend') == 'Rising']
            if rising_topics:
                score += 15
                feedback_points.append(f'✓ {len(rising_topics)} keyword(s) are rising in popularity')
            
            # Check if high-score topics are used
            high_score_topics = [t for t in trending_topics if t.get('score', 0) > 50]
            if high_score_topics:
                score += 10
                feedback_points.append(f'✓ Uses high-interest keywords')
        
        # Timeliness score (how recent is the video)
        upload_date = video_data.get('upload_date', '')
        if 'ago' in upload_date.lower():
            # Recent video
            if 'day' in upload_date or 'hour' in upload_date:
                score += 15
                feedback_points.append('✓ Recent video - good for trending topics')
            elif 'week' in upload_date:
                score += 10
                feedback_points.append('✓ Recent video')
            else:
                score += 5
                feedback_points.append('⚠ Older video - trends may have shifted')
        
        # Cap score at 100
        score = min(100, score)
        
        # If no trending data was found
        if not trending_topics and not related_tags:
            score = 50
            feedback_points = ['⚠ Unable to retrieve trend data - neutral score assigned']
        
        feedback = '\n'.join(feedback_points)
        
        return score, feedback
    
    def get_youtube_trending(self, region='US', category='all'):
        """Get current YouTube trending videos (fallback method)"""
        # This is a simplified version - in production, you would use YouTube Data API
        # For now, return some common trending topics
        
        trending_categories = {
            'all': [
                'viral video', 'trending now', 'popular', 'breaking news',
                'challenge', 'reaction video', 'tutorial', 'review'
            ],
            'gaming': [
                'gameplay', 'gaming news', 'game review', 'lets play',
                'gaming tips', 'speedrun', 'game trailer'
            ],
            'tech': [
                'tech review', 'unboxing', 'tech news', 'how to',
                'tutorial', 'product review', 'comparison'
            ],
            'lifestyle': [
                'vlog', 'daily routine', 'lifestyle tips', 'motivation',
                'productivity', 'self improvement'
            ]
        }
        
        return trending_categories.get(category, trending_categories['all'])
    
    def suggest_seasonal_tags(self):
        """Suggest tags based on current season/time of year"""
        now = datetime.now()
        month = now.month
        
        seasonal_tags = []
        
        # Holiday and seasonal tags
        if month == 12:
            seasonal_tags.extend(['christmas', 'holiday', 'new year', 'winter'])
        elif month in [1, 2]:
            seasonal_tags.extend(['winter', 'new year resolution', 'january'])
        elif month in [3, 4, 5]:
            seasonal_tags.extend(['spring', 'easter', 'spring cleaning'])
        elif month in [6, 7, 8]:
            seasonal_tags.extend(['summer', 'vacation', 'summer fun'])
        elif month in [9, 10, 11]:
            seasonal_tags.extend(['fall', 'autumn', 'back to school', 'halloween', 'thanksgiving'])
        
        # Day of week tags
        day = now.strftime('%A').lower()
        seasonal_tags.append(day)
        
        return seasonal_tags
    
    def get_niche_trends(self, niche_keywords, region='US'):
        """Get trends specific to a niche"""
        try:
            niche_trends = []
            
            for keyword in niche_keywords[:3]:
                self.pytrends.build_payload(
                    [keyword],
                    cat=0,
                    timeframe='today 3-m',
                    geo=region
                )
                
                # Get interest by region
                interest_by_region = self.pytrends.interest_by_region()
                
                # Get related topics
                related_topics = self.pytrends.related_topics()
                
                if keyword in related_topics:
                    rising_topics = related_topics[keyword].get('rising')
                    if rising_topics is not None and not rising_topics.empty:
                        for idx, row in rising_topics.head(5).iterrows():
                            topic = row.get('topic_title', '')
                            if topic:
                                niche_trends.append(topic)
                
                time.sleep(random.uniform(1.0, 2.0))
            
            return niche_trends
            
        except Exception as e:
            print(f"Error getting niche trends: {e}")
            return []

