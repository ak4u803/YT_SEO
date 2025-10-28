"""
SEO Engine Module
Analyzes video content and suggests SEO tags and optimizations
"""

import re
from collections import Counter
import string
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import numpy as np
from ml_tag_predictor import MLTagPredictor

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except (LookupError, OSError):
    nltk.download('punkt', quiet=True)

# Some newer NLTK versions separate punkt tables. Ensure it's present too.
try:
    nltk.data.find('tokenizers/punkt_tab')
except (LookupError, OSError):
    try:
        nltk.download('punkt_tab', quiet=True)
    except Exception:
        pass

try:
    nltk.data.find('corpora/stopwords')
except (LookupError, OSError):
    nltk.download('stopwords', quiet=True)

class SEOEngine:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        # Common YouTube stop words to exclude from tags
        self.youtube_stop_words = {
            'video', 'videos', 'youtube', 'channel', 'subscribe', 
            'like', 'comment', 'share', 'watch', 'click', 'link',
            'description', 'today', 'new', 'check'
        }
        self.stop_words.update(self.youtube_stop_words)
        
        # Initialize ML Tag Predictor
        try:
            self.ml_predictor = MLTagPredictor()
            self.ml_enabled = True
        except Exception as e:
            print(f"ML Tag Predictor not available: {e}")
            self.ml_predictor = None
            self.ml_enabled = False
        
    def analyze_seo(self, video_data):
        """Main SEO analysis method"""
        results = {
            'suggested_tags': [],
            'ml_tags': [],
            'ml_tag_explanations': {},
            'ml_quality_metrics': {},
            'suggestions': [],
            'title_score': 0,
            'title_feedback': '',
            'description_score': 0,
            'description_feedback': '',
            'tag_score': 0,
            'tag_feedback': '',
            'content_score': 0,
            'content_feedback': '',
            'recommendations': []
        }
        
        # Analyze title
        title_analysis = self.analyze_title(video_data.get('title', ''))
        results['title_score'] = title_analysis['score']
        results['title_feedback'] = title_analysis['feedback']
        results['suggestions'].extend(title_analysis['suggestions'])
        
        # Analyze description
        desc_analysis = self.analyze_description(video_data.get('description', ''))
        results['description_score'] = desc_analysis['score']
        results['description_feedback'] = desc_analysis['feedback']
        results['suggestions'].extend(desc_analysis['suggestions'])
        
        # Analyze existing tags
        tag_analysis = self.analyze_tags(video_data.get('tags', []))
        results['tag_score'] = tag_analysis['score']
        results['tag_feedback'] = tag_analysis['feedback']
        results['suggestions'].extend(tag_analysis['suggestions'])
        
        # Analyze content quality
        content_analysis = self.analyze_content(video_data)
        results['content_score'] = content_analysis['score']
        results['content_feedback'] = content_analysis['feedback']
        
        # Generate suggested tags (traditional method)
        suggested_tags = self.generate_tags(video_data)
        results['suggested_tags'] = suggested_tags
        
        # Generate ML-based tags
        if self.ml_enabled and self.ml_predictor:
            try:
                ml_results = self.ml_predictor.predict_tags(video_data, num_tags=30)
                results['ml_tags'] = ml_results.get('ml_tags', [])
                results['ml_category_scores'] = ml_results.get('category_scores', {})
                results['ml_method'] = ml_results.get('method_used', 'N/A')
                
                # Get explanations for ML tags
                if results['ml_tags']:
                    results['ml_tag_explanations'] = self.ml_predictor.get_tag_explanations(
                        results['ml_tags'][:10], 
                        video_data
                    )
                    
                    # Analyze tag quality
                    results['ml_quality_metrics'] = self.ml_predictor.analyze_tag_quality(
                        results['ml_tags']
                    )
            except Exception as e:
                print(f"Error in ML tag generation: {e}")
                results['ml_tags'] = []
        
        # Generate recommendations
        results['recommendations'] = self.generate_recommendations(results)
        
        return results
    
    def analyze_title(self, title):
        """Analyze video title for SEO"""
        analysis = {
            'score': 0,
            'feedback': '',
            'suggestions': []
        }
        
        if not title:
            analysis['feedback'] = 'No title found.'
            return analysis
        
        score = 0
        feedback_points = []
        
        # Length check (optimal: 50-70 characters)
        title_length = len(title)
        if 50 <= title_length <= 70:
            score += 30
            feedback_points.append('✓ Title length is optimal')
        elif 40 <= title_length < 50 or 70 < title_length <= 80:
            score += 20
            feedback_points.append('⚠ Title length is acceptable but not optimal')
            analysis['suggestions'].append('Consider adjusting title length to 50-70 characters for optimal visibility')
        else:
            score += 10
            feedback_points.append('✗ Title length is not optimal')
            analysis['suggestions'].append(f'Title is {title_length} characters. Aim for 50-70 characters')
        
        # Keyword placement (keywords should be early)
        words = title.lower().split()
        if len(words) > 0:
            score += 20
            feedback_points.append('✓ Title contains searchable keywords')
        
        # Capitalization check
        if title[0].isupper():
            score += 10
            feedback_points.append('✓ Title is properly capitalized')
        
        # Check for numbers (numbers improve CTR)
        if re.search(r'\d+', title):
            score += 10
            feedback_points.append('✓ Title contains numbers (good for CTR)')
        else:
            analysis['suggestions'].append('Consider adding numbers to your title (e.g., "5 Ways", "Top 10") to improve click-through rate')
        
        # Check for power words
        power_words = ['best', 'ultimate', 'guide', 'how to', 'tips', 'tricks', 
                       'secrets', 'proven', 'amazing', 'perfect', 'essential']
        if any(word in title.lower() for word in power_words):
            score += 15
            feedback_points.append('✓ Title contains power words')
        else:
            analysis['suggestions'].append('Consider using power words like "Ultimate", "Best", "Essential" to make title more compelling')
        
        # Check for clickbait-y all caps
        if title.isupper():
            score -= 10
            feedback_points.append('✗ Avoid all caps titles')
            analysis['suggestions'].append('Avoid using all caps in your title')
        else:
            score += 15
        
        analysis['score'] = min(100, score)
        analysis['feedback'] = '\n'.join(feedback_points)
        
        return analysis
    
    def analyze_description(self, description):
        """Analyze video description for SEO"""
        analysis = {
            'score': 0,
            'feedback': '',
            'suggestions': []
        }
        
        if not description:
            analysis['feedback'] = '✗ No description found'
            analysis['suggestions'].append('Add a detailed description (at least 200 characters)')
            return analysis
        
        score = 0
        feedback_points = []
        
        # Length check (optimal: 200+ characters)
        desc_length = len(description)
        if desc_length >= 200:
            score += 30
            feedback_points.append(f'✓ Description length is good ({desc_length} characters)')
        elif desc_length >= 100:
            score += 20
            feedback_points.append(f'⚠ Description could be longer ({desc_length} characters)')
            analysis['suggestions'].append('Expand your description to at least 200 characters for better SEO')
        else:
            score += 10
            feedback_points.append(f'✗ Description is too short ({desc_length} characters)')
            analysis['suggestions'].append('Add a more detailed description (aim for 200+ characters)')
        
        # Check for links
        if 'http' in description or 'www.' in description:
            score += 15
            feedback_points.append('✓ Description contains links')
        else:
            analysis['suggestions'].append('Add relevant links in your description (social media, website, related videos)')
        
        # Check for timestamps
        if re.search(r'\d+:\d+', description):
            score += 15
            feedback_points.append('✓ Description contains timestamps')
        else:
            if desc_length > 200:
                analysis['suggestions'].append('Consider adding timestamps for longer videos to improve user experience')
        
        # Check for keywords in first 200 characters
        first_200 = description[:200].lower()
        if len(first_200) > 50:
            score += 20
            feedback_points.append('✓ Description starts with content')
        
        # Check for call to action
        cta_words = ['subscribe', 'like', 'comment', 'share', 'follow', 'join']
        if any(word in description.lower() for word in cta_words):
            score += 10
            feedback_points.append('✓ Description contains call-to-action')
        else:
            analysis['suggestions'].append('Add a call-to-action (e.g., "Subscribe for more content")')
        
        # Check for hashtags
        if '#' in description:
            score += 10
            feedback_points.append('✓ Description includes hashtags')
        
        analysis['score'] = min(100, score)
        analysis['feedback'] = '\n'.join(feedback_points)
        
        return analysis
    
    def analyze_tags(self, tags):
        """Analyze existing video tags"""
        analysis = {
            'score': 0,
            'feedback': '',
            'suggestions': []
        }
        
        if not tags:
            analysis['feedback'] = '✗ No tags found'
            analysis['suggestions'].append('Add tags to improve discoverability')
            return analysis
        
        score = 0
        feedback_points = []
        
        # Number of tags (optimal: 15-30)
        num_tags = len(tags)
        if 15 <= num_tags <= 30:
            score += 30
            feedback_points.append(f'✓ Good number of tags ({num_tags})')
        elif 10 <= num_tags < 15 or 30 < num_tags <= 40:
            score += 20
            feedback_points.append(f'⚠ Tag count is acceptable ({num_tags})')
            analysis['suggestions'].append(f'Aim for 15-30 tags (currently {num_tags})')
        else:
            score += 10
            feedback_points.append(f'✗ Tag count needs improvement ({num_tags})')
            if num_tags < 10:
                analysis['suggestions'].append(f'Add more tags (currently {num_tags}, aim for 15-30)')
            else:
                analysis['suggestions'].append(f'Too many tags may dilute focus (currently {num_tags}, aim for 15-30)')
        
        # Tag variety (mix of short and long tags)
        tag_lengths = [len(tag.split()) for tag in tags]
        has_short = any(l == 1 for l in tag_lengths)
        has_medium = any(2 <= l <= 3 for l in tag_lengths)
        has_long = any(l > 3 for l in tag_lengths)
        
        variety_count = sum([has_short, has_medium, has_long])
        if variety_count >= 2:
            score += 25
            feedback_points.append('✓ Good mix of short and long-tail tags')
        else:
            score += 10
            analysis['suggestions'].append('Include a mix of short tags and long-tail phrases')
        
        # Check for brand/channel tags
        unique_tags = set(tag.lower() for tag in tags)
        if len(unique_tags) < num_tags * 0.9:
            score += 15
            feedback_points.append('✓ Some branded/consistent tags found')
        
        # Average tag length (characters)
        avg_length = sum(len(tag) for tag in tags) / num_tags if num_tags > 0 else 0
        if 10 <= avg_length <= 30:
            score += 20
            feedback_points.append('✓ Tag length is appropriate')
        else:
            score += 10
        
        # Check for overly generic tags
        generic_tags = {'video', 'youtube', 'vlog', 'new', 'viral'}
        if not any(tag.lower() in generic_tags for tag in tags):
            score += 10
            feedback_points.append('✓ No overly generic tags')
        else:
            analysis['suggestions'].append('Remove very generic tags like "video" or "youtube"')
        
        analysis['score'] = min(100, score)
        analysis['feedback'] = '\n'.join(feedback_points)
        
        return analysis
    
    def analyze_content(self, video_data):
        """Analyze overall content quality"""
        analysis = {
            'score': 0,
            'feedback': '',
        }
        
        score = 0
        feedback_points = []
        
        # Check if transcript is available
        transcript = video_data.get('transcript_full', '')
        if transcript:
            score += 30
            feedback_points.append('✓ Transcript available')
            
            # Analyze transcript length
            word_count = len(transcript.split())
            if word_count > 500:
                score += 20
                feedback_points.append(f'✓ Substantial content ({word_count} words)')
            elif word_count > 200:
                score += 15
                feedback_points.append(f'⚠ Moderate content length ({word_count} words)')
            else:
                score += 10
                feedback_points.append(f'⚠ Short content ({word_count} words)')
        else:
            score += 10
            feedback_points.append('⚠ No transcript available')
        
        # Check engagement metrics
        views = video_data.get('views', 0)
        likes = video_data.get('likes', 0)
        
        if views > 0 and likes > 0:
            engagement_rate = (likes / views) * 100
            if engagement_rate > 5:
                score += 25
                feedback_points.append(f'✓ Strong engagement rate ({engagement_rate:.2f}%)')
            elif engagement_rate > 2:
                score += 15
                feedback_points.append(f'⚠ Moderate engagement rate ({engagement_rate:.2f}%)')
            else:
                score += 10
                feedback_points.append(f'⚠ Low engagement rate ({engagement_rate:.2f}%)')
        
        # Content consistency check
        title = video_data.get('title', '').lower()
        description = video_data.get('description', '').lower()
        
        if title and description:
            # Check if key title words appear in description
            title_words = set(self.extract_keywords(title, max_keywords=5))
            desc_words = set(self.extract_keywords(description, max_keywords=20))
            
            overlap = len(title_words & desc_words)
            if overlap >= 3:
                score += 25
                feedback_points.append('✓ Good keyword consistency between title and description')
            elif overlap >= 1:
                score += 15
                feedback_points.append('⚠ Some keyword consistency')
            else:
                score += 5
                feedback_points.append('✗ Low keyword consistency between title and description')
        
        analysis['score'] = min(100, score)
        analysis['feedback'] = '\n'.join(feedback_points)
        
        return analysis
    
    def generate_tags(self, video_data):
        """Generate suggested tags based on video content"""
        tags = []
        
        # Extract text from various sources
        title = video_data.get('title', '')
        description = video_data.get('description', '')
        transcript = video_data.get('transcript_full', '')
        
        # Combine all text
        all_text = f"{title} {title} {title} {description} {transcript}"  # Title weighted more
        
        # Extract keywords using TF-IDF
        tfidf_keywords = self.extract_keywords_tfidf(all_text, max_keywords=30)
        tags.extend(tfidf_keywords)
        
        # Extract keywords using frequency analysis
        freq_keywords = self.extract_keywords(all_text, max_keywords=20)
        tags.extend(freq_keywords)
        
        # Extract phrases
        phrases = self.extract_phrases(all_text, max_phrases=15)
        tags.extend(phrases)
        
        # Add tags from title
        title_tags = self.extract_title_tags(title)
        tags.extend(title_tags)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_tags = []
        for tag in tags:
            tag_lower = tag.lower()
            if tag_lower not in seen and len(tag) > 2:
                seen.add(tag_lower)
                unique_tags.append(tag)
        
        # Clean and format tags
        cleaned_tags = [self.clean_tag(tag) for tag in unique_tags]
        cleaned_tags = [tag for tag in cleaned_tags if tag and len(tag) > 2]
        
        return cleaned_tags[:50]  # Return top 50 tags
    
    def extract_keywords(self, text, max_keywords=20):
        """Extract keywords using frequency analysis"""
        if not text:
            return []
        
        # Tokenize and clean
        text = text.lower()
        words = word_tokenize(text)
        
        # Remove stop words and punctuation
        words = [word for word in words 
                if word not in self.stop_words 
                and word not in string.punctuation
                and len(word) > 2
                and word.isalpha()]
        
        # Get most common words
        counter = Counter(words)
        keywords = [word for word, count in counter.most_common(max_keywords)]
        
        return keywords
    
    def extract_keywords_tfidf(self, text, max_keywords=20):
        """Extract keywords using TF-IDF"""
        if not text:
            return []
        
        try:
            # Create TF-IDF vectorizer
            vectorizer = TfidfVectorizer(
                max_features=max_keywords,
                stop_words='english',
                ngram_range=(1, 1),
                min_df=1
            )
            
            # Fit and transform
            tfidf_matrix = vectorizer.fit_transform([text])
            feature_names = vectorizer.get_feature_names_out()
            
            # Get scores
            scores = tfidf_matrix.toarray()[0]
            
            # Sort by score
            keyword_scores = list(zip(feature_names, scores))
            keyword_scores.sort(key=lambda x: x[1], reverse=True)
            
            # Return keywords
            keywords = [kw for kw, score in keyword_scores if len(kw) > 2]
            
            return keywords
        
        except Exception as e:
            print(f"Error in TF-IDF extraction: {e}")
            return []
    
    def extract_phrases(self, text, max_phrases=15):
        """Extract common phrases (2-3 word combinations)"""
        if not text:
            return []
        
        text = text.lower()
        words = word_tokenize(text)
        
        # Remove stop words at boundaries
        words = [w for w in words if w.isalpha()]
        
        # Extract bigrams and trigrams
        phrases = []
        
        # Bigrams
        for i in range(len(words) - 1):
            if (words[i] not in self.stop_words and 
                words[i+1] not in self.stop_words and
                len(words[i]) > 2 and len(words[i+1]) > 2):
                phrase = f"{words[i]} {words[i+1]}"
                phrases.append(phrase)
        
        # Trigrams
        for i in range(len(words) - 2):
            if (words[i] not in self.stop_words and 
                words[i+2] not in self.stop_words and
                len(words[i]) > 2 and len(words[i+2]) > 2):
                phrase = f"{words[i]} {words[i+1]} {words[i+2]}"
                phrases.append(phrase)
        
        # Count phrases
        phrase_counter = Counter(phrases)
        common_phrases = [phrase for phrase, count in phrase_counter.most_common(max_phrases) if count > 1]
        
        return common_phrases
    
    def extract_title_tags(self, title):
        """Extract specific tags from title"""
        if not title:
            return []
        
        tags = []
        
        # Extract the main topic (usually early in title)
        words = title.split()
        if len(words) >= 2:
            # Add first few words as a tag
            tags.append(' '.join(words[:2]))
            if len(words) >= 3:
                tags.append(' '.join(words[:3]))
        
        # Extract individual meaningful words
        meaningful_words = [w for w in words if w.lower() not in self.stop_words and len(w) > 3]
        tags.extend(meaningful_words[:5])
        
        return tags
    
    def clean_tag(self, tag):
        """Clean and format a tag"""
        # Remove extra whitespace
        tag = ' '.join(tag.split())
        
        # Remove punctuation from ends
        tag = tag.strip(string.punctuation)
        
        # Convert to title case for multi-word tags
        if ' ' in tag:
            tag = tag.title()
        
        return tag
    
    def generate_recommendations(self, seo_results):
        """Generate actionable recommendations"""
        recommendations = []
        
        # Based on scores, provide recommendations
        if seo_results['title_score'] < 70:
            recommendations.append('Improve your title: Make it more compelling and include key search terms early')
        
        if seo_results['description_score'] < 70:
            recommendations.append('Enhance your description: Add more detail, include relevant links and timestamps')
        
        if seo_results['tag_score'] < 70:
            recommendations.append('Optimize your tags: Use 15-30 relevant tags with a mix of specific and broad terms')
        
        if seo_results['content_score'] < 70:
            recommendations.append('Improve content alignment: Ensure your title, description, and content are closely related')
        
        # General recommendations
        recommendations.append('Update tags regularly based on trending topics in your niche')
        recommendations.append('Monitor performance metrics and adjust strategy accordingly')
        recommendations.append('Use the suggested tags to improve discoverability')
        
        return recommendations

