"""
Trend Analyzer Module
Analyzes current trends and suggests tags based on trending topics
Enhanced with advanced prediction algorithms, time series analysis, and trend forecasting
"""

from pytrends.request import TrendReq
import time
import random
from datetime import datetime, timedelta
import re
import numpy as np
from scipy import stats
from collections import deque
import warnings
warnings.filterwarnings('ignore')

class TrendAnalyzer:
    def __init__(self):
        # Initialize pytrends
        self.pytrends = TrendReq(hl='en-US', tz=360)
        self.trend_cache = {}
        self.cache_duration = 3600  # Cache for 1 hour
        self.historical_data = {}  # Store historical trend data for better predictions
        self.trend_history = deque(maxlen=100)  # Keep last 100 trend analyses
    
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
        """Get trending topics related to keywords with enhanced analysis"""
        trending_topics = []
        trends_data = {}  # Store for cross-correlation
        
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
                        # Get time series data
                        time_series = interest_df[keyword].values.tolist()
                        trends_data[keyword] = time_series
                        
                        # Calculate average interest
                        avg_interest = interest_df[keyword].mean()
                        
                        # === ENHANCED ANALYSIS ===
                        
                        # 1. Calculate velocity and direction
                        velocity_score, velocity_direction = self.calculate_trend_velocity(time_series)
                        
                        # 2. Calculate acceleration
                        accel_score, accel_state = self.calculate_trend_acceleration(time_series)
                        
                        # 3. Detect lifecycle phase
                        lifecycle, lifecycle_score, lifecycle_desc = self.detect_trend_lifecycle(time_series, keyword)
                        
                        # 4. Calculate momentum
                        momentum_score, momentum_desc = self.calculate_trend_momentum(time_series)
                        
                        # 5. Forecast future trend
                        forecasts, forecast_confidence = self.forecast_trend(time_series, periods_ahead=3)
                        
                        # 6. Detect anomalies (viral spikes)
                        anomalies = self.detect_anomalies(time_series)
                        
                        # 7. Check seasonality
                        has_seasonality, seasonal_score, seasonal_desc = self.analyze_seasonality(time_series)
                        
                        # Calculate comprehensive score
                        comprehensive_score = int(
                            avg_interest * 0.25 +
                            velocity_score * 0.20 +
                            lifecycle_score * 0.25 +
                            momentum_score * 0.20 +
                            accel_score * 0.10
                        )
                        
                        # Determine trend status
                        if velocity_direction == 'rapidly_rising':
                            trend_status = '🚀 Rapidly Rising'
                        elif velocity_direction == 'rising':
                            trend_status = '📈 Rising'
                        elif velocity_direction == 'rapidly_falling':
                            trend_status = '📉 Rapidly Falling'
                        elif velocity_direction == 'falling':
                            trend_status = '⬇️ Declining'
                        else:
                            trend_status = '➡️ Stable'
                        
                        # Build enhanced topic data
                        topic_data = {
                            'name': keyword,
                            'score': comprehensive_score,
                            'avg_interest': int(avg_interest),
                            'trend': trend_status,
                            'velocity': velocity_direction,
                            'acceleration': accel_state,
                            'lifecycle': lifecycle,
                            'lifecycle_desc': lifecycle_desc,
                            'momentum': momentum_desc,
                            'momentum_score': int(momentum_score),
                            'has_anomalies': len(anomalies) > 0,
                            'anomaly_count': len(anomalies),
                            'forecast': forecasts,
                            'forecast_confidence': forecast_confidence,
                            'is_seasonal': has_seasonality,
                            'time_series': time_series
                        }
                        
                        # Add viral indicator if anomalies detected
                        if anomalies:
                            extreme_anomalies = [a for a in anomalies if a['magnitude'] == 'extreme']
                            if extreme_anomalies:
                                topic_data['viral_indicator'] = '⚡ VIRAL POTENTIAL'
                        
                        trending_topics.append(topic_data)
                    
                    # Small delay to avoid rate limiting
                    time.sleep(random.uniform(0.5, 1.5))
                    
                except Exception as e:
                    print(f"Error getting trends for {keyword}: {e}")
                    continue
            
            # Perform cross-correlation analysis
            if len(trends_data) >= 2:
                correlations = self.cross_correlate_trends(trends_data)
                # Add correlation info to topics
                for topic in trending_topics:
                    topic['correlations'] = [
                        c for c in correlations 
                        if c['keyword1'] == topic['name'] or c['keyword2'] == topic['name']
                    ]
            
            # Sort by comprehensive score
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
        """Calculate how well the video aligns with trends using enhanced metrics"""
        score = 0
        feedback_points = []
        
        # Check if video uses trending keywords
        video_tags = set(tag.lower() for tag in video_data.get('tags', []))
        video_title = video_data.get('title', '').lower()
        video_desc = video_data.get('description', '').lower()
        
        # === ENHANCED TREND MATCHING ===
        trending_matches = 0
        high_value_matches = 0
        viral_potential_matches = 0
        emerging_matches = 0
        
        for topic in trending_topics:
            topic_name = topic['name'].lower()
            if (topic_name in video_title or 
                topic_name in video_desc or 
                topic_name in video_tags):
                trending_matches += 1
                
                # Base score from match
                base_score = 10
                
                # Bonus for lifecycle phase
                lifecycle = topic.get('lifecycle', 'unknown')
                if lifecycle == 'emerging':
                    base_score += 15  # High potential
                    emerging_matches += 1
                    feedback_points.append(f'🌱 Using emerging trend "{topic_name}" - excellent timing!')
                elif lifecycle == 'growing':
                    base_score += 12  # Very good
                    feedback_points.append(f'📈 Using growing trend "{topic_name}" - great opportunity!')
                elif lifecycle == 'mature':
                    base_score += 5  # Safe but less exciting
                elif lifecycle == 'declining':
                    base_score -= 5  # Penalize declining trends
                    feedback_points.append(f'⚠ Trend "{topic_name}" is declining - consider fresher topics')
                
                # Bonus for momentum
                momentum_score = topic.get('momentum_score', 50)
                if momentum_score > 75:
                    base_score += 10
                    high_value_matches += 1
                elif momentum_score > 60:
                    base_score += 5
                
                # Bonus for viral potential
                if topic.get('viral_indicator'):
                    base_score += 20
                    viral_potential_matches += 1
                    feedback_points.append(f'⚡ VIRAL POTENTIAL: "{topic_name}" showing explosive growth!')
                
                # Bonus for strong forecasts
                forecast_confidence = topic.get('forecast_confidence', 0)
                if forecast_confidence > 70:
                    forecasts = topic.get('forecast', [])
                    if forecasts and forecasts[-1] > topic.get('avg_interest', 0):
                        base_score += 8
                        feedback_points.append(f'🔮 Trend "{topic_name}" predicted to grow stronger')
                
                score += base_score
        
        # Summary feedback for matches
        if trending_matches > 0:
            feedback_points.insert(0, f'✓ Video uses {trending_matches} trending keyword(s)')
            if high_value_matches > 0:
                feedback_points.insert(1, f'⭐ {high_value_matches} high-momentum trend(s) detected!')
        else:
            feedback_points.append('⚠ Video does not use current trending keywords')
            score -= 10
        
        # Check if video tags match related trends
        related_matches = 0
        for tag_info in related_tags[:10]:
            related_tag = tag_info['tag'].lower()
            if (any(related_tag in vt for vt in video_tags) or
                related_tag in video_title or
                related_tag in video_desc):
                related_matches += 1
                score += 5
        
        if related_matches > 0:
            feedback_points.append(f'✓ Video aligns with {related_matches} related trend(s)')
        else:
            feedback_points.append('⚠ Consider incorporating trending related topics')
        
        # Enhanced momentum analysis
        if trending_topics:
            # Check for rising topics
            rising_topics = [t for t in trending_topics 
                           if 'rising' in t.get('velocity', '').lower()]
            if rising_topics:
                score += 15
                feedback_points.append(f'✓ {len(rising_topics)} keyword(s) have rising momentum')
            
            # Check for accelerating topics
            accelerating = [t for t in trending_topics 
                          if 'accelerating' in t.get('acceleration', '')]
            if accelerating:
                score += 10
                feedback_points.append(f'🚀 {len(accelerating)} keyword(s) are accelerating!')
            
            # Check correlations for synergy
            for topic in trending_topics:
                correlations = topic.get('correlations', [])
                if len(correlations) >= 2:
                    feedback_points.append(f'🔗 Trend "{topic["name"]}" correlates with multiple other trends - strong synergy!')
                    score += 5
                    break  # Only show once
        
        # Timeliness score (how recent is the video)
        upload_date = video_data.get('upload_date', '')
        if 'ago' in upload_date.lower():
            if 'day' in upload_date or 'hour' in upload_date:
                score += 15
                feedback_points.append('✓ Recent video - optimal for trending topics')
            elif 'week' in upload_date:
                score += 10
                feedback_points.append('✓ Recent video')
            else:
                score += 5
                feedback_points.append('⚠ Older video - trends may have shifted')
        
        # Strategic recommendations based on analysis
        if emerging_matches > 0:
            feedback_points.append('💡 Strategy: You\'re ahead of the curve with emerging trends!')
        elif viral_potential_matches > 0:
            feedback_points.append('💡 Strategy: Capitalize on viral potential with immediate promotion!')
        elif trending_matches == 0:
            feedback_points.append('💡 Strategy: Update tags with currently trending keywords for better visibility')
        
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
    
    # ==================== ENHANCED TREND PREDICTION ALGORITHMS ====================
    
    def calculate_trend_velocity(self, time_series_data):
        """
        Calculate the velocity (rate of change) of a trend
        Returns velocity score and direction
        """
        if len(time_series_data) < 2:
            return 0, 'stable'
        
        try:
            # Convert to numpy array
            values = np.array(time_series_data)
            
            # Calculate first derivative (velocity)
            velocity = np.gradient(values)
            
            # Calculate average velocity
            avg_velocity = np.mean(velocity)
            recent_velocity = np.mean(velocity[-3:]) if len(velocity) >= 3 else avg_velocity
            
            # Determine direction and magnitude
            if recent_velocity > 5:
                direction = 'rapidly_rising'
                score = min(100, 50 + abs(recent_velocity) * 2)
            elif recent_velocity > 1:
                direction = 'rising'
                score = 60 + abs(recent_velocity) * 3
            elif recent_velocity < -5:
                direction = 'rapidly_falling'
                score = max(0, 50 - abs(recent_velocity) * 2)
            elif recent_velocity < -1:
                direction = 'falling'
                score = 40 - abs(recent_velocity) * 3
            else:
                direction = 'stable'
                score = 50
            
            return score, direction
            
        except Exception as e:
            print(f"Error calculating velocity: {e}")
            return 50, 'stable'
    
    def calculate_trend_acceleration(self, time_series_data):
        """
        Calculate the acceleration (rate of change of velocity) of a trend
        Indicates if trend is speeding up or slowing down
        """
        if len(time_series_data) < 3:
            return 0, 'steady'
        
        try:
            values = np.array(time_series_data)
            
            # Calculate second derivative (acceleration)
            velocity = np.gradient(values)
            acceleration = np.gradient(velocity)
            
            # Calculate recent acceleration
            recent_accel = np.mean(acceleration[-3:]) if len(acceleration) >= 3 else np.mean(acceleration)
            
            # Determine acceleration state
            if recent_accel > 2:
                state = 'accelerating'
                score = 80
            elif recent_accel > 0.5:
                state = 'slowly_accelerating'
                score = 65
            elif recent_accel < -2:
                state = 'decelerating'
                score = 30
            elif recent_accel < -0.5:
                state = 'slowly_decelerating'
                score = 45
            else:
                state = 'steady'
                score = 50
            
            return score, state
            
        except Exception as e:
            print(f"Error calculating acceleration: {e}")
            return 50, 'steady'
    
    def detect_trend_lifecycle(self, time_series_data, keyword):
        """
        Detect which phase of lifecycle the trend is in:
        - emerging: new trend starting to gain traction
        - growing: trend is actively growing
        - peak: trend has reached maximum interest
        - mature: trend is stable at high interest
        - declining: trend is losing interest
        """
        if len(time_series_data) < 5:
            return 'insufficient_data', 50, 'Not enough data for lifecycle analysis'
        
        try:
            values = np.array(time_series_data)
            
            # Calculate statistics
            mean_value = np.mean(values)
            max_value = np.max(values)
            recent_avg = np.mean(values[-3:])
            early_avg = np.mean(values[:3])
            
            # Calculate growth rate
            if early_avg > 0:
                growth_rate = ((recent_avg - early_avg) / early_avg) * 100
            else:
                growth_rate = 0
            
            # Calculate trend using linear regression
            x = np.arange(len(values))
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, values)
            
            # Determine lifecycle phase
            lifecycle = None
            score = 50
            confidence = abs(r_value) * 100  # R-squared as confidence
            
            if mean_value < 20 and slope > 1:
                lifecycle = 'emerging'
                score = 75  # High potential
                description = f'Emerging trend with {growth_rate:.1f}% growth - Great opportunity!'
            
            elif slope > 2 and recent_avg > early_avg * 1.5:
                lifecycle = 'growing'
                score = 85  # Very hot trend
                description = f'Rapidly growing trend ({growth_rate:.1f}% growth) - Excellent timing!'
            
            elif slope > 0.5 and recent_avg > mean_value * 0.9:
                lifecycle = 'growing'
                score = 70
                description = f'Growing trend ({growth_rate:.1f}% growth) - Good opportunity'
            
            elif abs(slope) < 0.5 and mean_value > 70:
                lifecycle = 'mature'
                score = 60
                description = 'Mature trend with stable high interest - Safe choice'
            
            elif recent_avg >= max_value * 0.95 and slope < 1:
                lifecycle = 'peak'
                score = 55
                description = 'Trend at peak - Consider timing carefully'
            
            elif slope < -1 and recent_avg < mean_value:
                lifecycle = 'declining'
                score = 30
                description = f'Declining trend ({growth_rate:.1f}% change) - Consider alternatives'
            
            elif slope < 0:
                lifecycle = 'declining'
                score = 40
                description = 'Trend losing momentum - May still have value'
            
            else:
                lifecycle = 'stable'
                score = 50
                description = 'Stable trend - Moderate opportunity'
            
            return lifecycle, score, description
            
        except Exception as e:
            print(f"Error detecting lifecycle: {e}")
            return 'unknown', 50, 'Unable to determine lifecycle phase'
    
    def forecast_trend(self, time_series_data, periods_ahead=3):
        """
        Forecast future trend values using exponential smoothing
        Returns predicted values and confidence
        """
        if len(time_series_data) < 4:
            return [], 0
        
        try:
            values = np.array(time_series_data)
            
            # Simple exponential smoothing
            alpha = 0.3  # Smoothing factor
            
            # Calculate smoothed values
            smoothed = [values[0]]
            for i in range(1, len(values)):
                smoothed.append(alpha * values[i] + (1 - alpha) * smoothed[i-1])
            
            # Calculate trend component
            if len(values) >= 2:
                trend = (values[-1] - values[0]) / len(values)
            else:
                trend = 0
            
            # Forecast future values
            forecasts = []
            last_value = smoothed[-1]
            
            for i in range(1, periods_ahead + 1):
                forecast = last_value + (trend * i)
                # Ensure forecast is within reasonable bounds
                forecast = max(0, min(100, forecast))
                forecasts.append(forecast)
            
            # Calculate confidence based on variance
            variance = np.var(values)
            if variance < 100:
                confidence = 80
            elif variance < 300:
                confidence = 60
            else:
                confidence = 40
            
            return forecasts, confidence
            
        except Exception as e:
            print(f"Error forecasting trend: {e}")
            return [], 0
    
    def detect_anomalies(self, time_series_data):
        """
        Detect anomalies (sudden spikes or drops) in trend data
        Useful for identifying viral moments
        """
        if len(time_series_data) < 5:
            return []
        
        try:
            values = np.array(time_series_data)
            
            # Calculate z-scores
            mean = np.mean(values)
            std = np.std(values)
            
            if std == 0:
                return []
            
            z_scores = np.abs((values - mean) / std)
            
            # Identify anomalies (z-score > 2)
            anomalies = []
            for i, z in enumerate(z_scores):
                if z > 2:
                    anomaly_type = 'spike' if values[i] > mean else 'drop'
                    anomalies.append({
                        'index': i,
                        'value': values[i],
                        'z_score': z,
                        'type': anomaly_type,
                        'magnitude': 'extreme' if z > 3 else 'significant'
                    })
            
            return anomalies
            
        except Exception as e:
            print(f"Error detecting anomalies: {e}")
            return []
    
    def analyze_seasonality(self, time_series_data, period=7):
        """
        Detect seasonal patterns in trend data
        period=7 for weekly patterns
        """
        if len(time_series_data) < period * 2:
            return False, 0, 'Insufficient data for seasonality analysis'
        
        try:
            values = np.array(time_series_data)
            
            # Calculate autocorrelation at the seasonal period
            if len(values) > period:
                mean = np.mean(values)
                var = np.var(values)
                
                if var == 0:
                    return False, 0, 'No variance in data'
                
                # Simple autocorrelation calculation
                autocorr = 0
                n = len(values) - period
                
                for i in range(n):
                    autocorr += (values[i] - mean) * (values[i + period] - mean)
                
                autocorr = autocorr / (n * var)
                
                # Check if seasonal pattern exists
                if autocorr > 0.5:
                    return True, autocorr * 100, f'Strong seasonal pattern detected (correlation: {autocorr:.2f})'
                elif autocorr > 0.3:
                    return True, autocorr * 100, f'Moderate seasonal pattern (correlation: {autocorr:.2f})'
                else:
                    return False, autocorr * 100, 'No significant seasonal pattern'
            
            return False, 0, 'Insufficient data length'
            
        except Exception as e:
            print(f"Error analyzing seasonality: {e}")
            return False, 0, 'Error in seasonality analysis'
    
    def calculate_trend_momentum(self, time_series_data):
        """
        Calculate overall trend momentum combining multiple factors
        Returns a momentum score (0-100) and description
        """
        if len(time_series_data) < 3:
            return 50, 'neutral'
        
        try:
            values = np.array(time_series_data)
            
            # Factor 1: Recent growth
            recent_avg = np.mean(values[-3:])
            earlier_avg = np.mean(values[:3])
            if earlier_avg > 0:
                growth = ((recent_avg - earlier_avg) / earlier_avg) * 100
            else:
                growth = 0
            growth_score = min(100, 50 + growth)
            
            # Factor 2: Velocity
            velocity_score, _ = self.calculate_trend_velocity(values)
            
            # Factor 3: Consistency (inverse of volatility)
            volatility = np.std(values) / (np.mean(values) + 1)
            consistency_score = max(0, 100 - volatility * 20)
            
            # Factor 4: Current level
            current_level = values[-1]
            level_score = min(100, current_level)
            
            # Weighted combination
            momentum = (
                growth_score * 0.3 +
                velocity_score * 0.3 +
                consistency_score * 0.2 +
                level_score * 0.2
            )
            
            # Determine description
            if momentum > 75:
                description = 'strong_upward'
            elif momentum > 60:
                description = 'moderate_upward'
            elif momentum > 40:
                description = 'neutral'
            elif momentum > 25:
                description = 'moderate_downward'
            else:
                description = 'strong_downward'
            
            return momentum, description
            
        except Exception as e:
            print(f"Error calculating momentum: {e}")
            return 50, 'neutral'
    
    def cross_correlate_trends(self, trends_dict):
        """
        Analyze correlations between multiple trends
        Identifies related trends that move together
        """
        if len(trends_dict) < 2:
            return []
        
        try:
            correlations = []
            keywords = list(trends_dict.keys())
            
            for i in range(len(keywords)):
                for j in range(i + 1, len(keywords)):
                    kw1, kw2 = keywords[i], keywords[j]
                    data1 = np.array(trends_dict[kw1])
                    data2 = np.array(trends_dict[kw2])
                    
                    # Ensure same length
                    min_len = min(len(data1), len(data2))
                    if min_len < 3:
                        continue
                    
                    data1 = data1[:min_len]
                    data2 = data2[:min_len]
                    
                    # Calculate correlation
                    if np.std(data1) > 0 and np.std(data2) > 0:
                        corr = np.corrcoef(data1, data2)[0, 1]
                        
                        if abs(corr) > 0.5:
                            correlations.append({
                                'keyword1': kw1,
                                'keyword2': kw2,
                                'correlation': corr,
                                'strength': 'strong' if abs(corr) > 0.7 else 'moderate',
                                'type': 'positive' if corr > 0 else 'negative'
                            })
            
            # Sort by absolute correlation
            correlations.sort(key=lambda x: abs(x['correlation']), reverse=True)
            return correlations
            
        except Exception as e:
            print(f"Error in cross-correlation: {e}")
            return []

