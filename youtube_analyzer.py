"""
YouTube Video Analyzer Module
Extracts video metadata, transcripts, and other relevant information
"""

import re
from urllib.parse import urlparse, parse_qs
import requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi
import json

class YouTubeAnalyzer:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def extract_video_id(self, url):
        """Extract video ID from YouTube URL"""
        # Handle different YouTube URL formats
        patterns = [
            r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([^&]+)',
            r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([^?]+)',
            r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/([^?]+)',
            r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/v\/([^?]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        # Try parsing as query parameter
        parsed = urlparse(url)
        if parsed.hostname in ['www.youtube.com', 'youtube.com', 'm.youtube.com']:
            query = parse_qs(parsed.query)
            if 'v' in query:
                return query['v'][0]
        
        raise ValueError("Invalid YouTube URL")
    
    def get_video_metadata(self, video_id):
        """Scrape video metadata from YouTube page"""
        url = f"https://www.youtube.com/watch?v={video_id}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract JSON data from page
            scripts = soup.find_all('script')
            video_data = {}
            
            for script in scripts:
                if script.string and 'ytInitialData' in script.string:
                    # Extract ytInitialData
                    json_text = script.string
                    start = json_text.find('ytInitialData = ') + len('ytInitialData = ')
                    end = json_text.find('};', start) + 1
                    if start > 0 and end > 0:
                        try:
                            data = json.loads(json_text[start:end])
                            video_data['ytInitialData'] = data
                        except:
                            pass
                
                if script.string and 'ytInitialPlayerResponse' in script.string:
                    # Extract ytInitialPlayerResponse
                    json_text = script.string
                    start = json_text.find('ytInitialPlayerResponse = ') + len('ytInitialPlayerResponse = ')
                    end = json_text.find('};', start) + 1
                    if start > 0 and end > 0:
                        try:
                            data = json.loads(json_text[start:end])
                            video_data['ytInitialPlayerResponse'] = data
                        except:
                            pass
            
            # Parse metadata
            metadata = self._parse_metadata(video_data, soup)
            metadata['video_id'] = video_id
            
            return metadata
            
        except Exception as e:
            # Fallback to basic metadata
            return self._get_basic_metadata(video_id, soup if 'soup' in locals() else None)
    
    def _parse_metadata(self, video_data, soup):
        """Parse metadata from extracted JSON data"""
        metadata = {}
        
        try:
            # Get data from ytInitialPlayerResponse
            if 'ytInitialPlayerResponse' in video_data:
                player_data = video_data['ytInitialPlayerResponse']
                video_details = player_data.get('videoDetails', {})
                
                metadata['title'] = video_details.get('title', 'Unknown')
                metadata['channel'] = video_details.get('author', 'Unknown')
                metadata['views'] = int(video_details.get('viewCount', 0))
                metadata['duration'] = self._format_duration(int(video_details.get('lengthSeconds', 0)))
                metadata['tags'] = video_details.get('keywords', [])
                metadata['description'] = video_details.get('shortDescription', '')
            
            # Get additional data from ytInitialData
            if 'ytInitialData' in video_data:
                initial_data = video_data['ytInitialData']
                
                # Try to extract likes and other engagement metrics
                try:
                    contents = initial_data['contents']['twoColumnWatchNextResults']['results']['results']['contents']
                    video_primary_info = None
                    
                    for content in contents:
                        if 'videoPrimaryInfoRenderer' in content:
                            video_primary_info = content['videoPrimaryInfoRenderer']
                            break
                    
                    if video_primary_info:
                        # Get date
                        date_text = video_primary_info.get('dateText', {}).get('simpleText', 'Unknown')
                        metadata['upload_date'] = date_text
                        
                        # Get likes
                        sentiment_bar = video_primary_info.get('sentimentBar', {})
                        if sentiment_bar:
                            # Likes might be in different places depending on YouTube's layout
                            pass
                        
                        # Try to get likes from video actions
                        menu_renderer = video_primary_info.get('videoActions', {}).get('menuRenderer', {})
                        top_level_buttons = menu_renderer.get('topLevelButtons', [])
                        
                        for button in top_level_buttons:
                            if 'toggleButtonRenderer' in button:
                                toggle = button['toggleButtonRenderer']
                                if 'defaultText' in toggle:
                                    text = toggle['defaultText'].get('accessibility', {}).get('accessibilityData', {}).get('label', '')
                                    if 'like' in text.lower():
                                        # Extract number from text
                                        likes = self._extract_number(text)
                                        if likes:
                                            metadata['likes'] = likes
                
                except Exception as e:
                    print(f"Error extracting engagement metrics: {e}")
            
            # Fallback to meta tags
            if not metadata.get('title'):
                title_tag = soup.find('meta', property='og:title')
                if title_tag:
                    metadata['title'] = title_tag.get('content', 'Unknown')
            
            if not metadata.get('description'):
                desc_tag = soup.find('meta', property='og:description')
                if desc_tag:
                    metadata['description'] = desc_tag.get('content', '')
            
        except Exception as e:
            print(f"Error parsing metadata: {e}")
        
        return metadata
    
    def _get_basic_metadata(self, video_id, soup):
        """Get basic metadata as fallback"""
        metadata = {
            'video_id': video_id,
            'title': 'Unknown',
            'channel': 'Unknown',
            'views': 0,
            'likes': 0,
            'upload_date': 'Unknown',
            'duration': 'Unknown',
            'description': '',
            'tags': []
        }
        
        if soup:
            # Try to get title
            title_tag = soup.find('meta', property='og:title')
            if title_tag:
                metadata['title'] = title_tag.get('content', 'Unknown')
            
            # Try to get description
            desc_tag = soup.find('meta', property='og:description')
            if desc_tag:
                metadata['description'] = desc_tag.get('content', '')
        
        return metadata
    
    def get_transcript(self, video_id):
        """Get video transcript"""
        try:
            # Try to get transcript in English
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            # Try to find English transcript
            try:
                transcript = transcript_list.find_transcript(['en'])
                transcript_data = transcript.fetch()
            except:
                # Get any available transcript
                transcript = transcript_list.find_generated_transcript(['en'])
                transcript_data = transcript.fetch()
            
            # Combine transcript text
            full_text = ' '.join([item['text'] for item in transcript_data])
            
            return {
                'full_text': full_text,
                'segments': transcript_data
            }
        
        except Exception as e:
            print(f"Error getting transcript: {e}")
            return {
                'full_text': '',
                'segments': []
            }
    
    def analyze_video(self, url):
        """Main method to analyze video"""
        # Extract video ID
        video_id = self.extract_video_id(url)
        
        # Get metadata
        metadata = self.get_video_metadata(video_id)
        
        # Get transcript
        transcript = self.get_transcript(video_id)
        
        # Create summary of transcript
        transcript_text = transcript['full_text']
        if transcript_text:
            # Create a summary (first 500 characters)
            metadata['transcript_summary'] = transcript_text[:500] + '...' if len(transcript_text) > 500 else transcript_text
            metadata['transcript_full'] = transcript_text
        else:
            metadata['transcript_summary'] = 'Transcript not available'
            metadata['transcript_full'] = ''
        
        return metadata
    
    def _format_duration(self, seconds):
        """Format duration in seconds to readable format"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        if hours > 0:
            return f"{hours}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes}:{secs:02d}"
    
    def _extract_number(self, text):
        """Extract number from text like '1.2K likes'"""
        # Remove commas
        text = text.replace(',', '')
        
        # Look for patterns like 1.2K, 1.2M, etc.
        match = re.search(r'([\d.]+)\s*([KMB])?', text, re.IGNORECASE)
        if match:
            number = float(match.group(1))
            unit = match.group(2)
            
            if unit:
                unit = unit.upper()
                if unit == 'K':
                    number *= 1000
                elif unit == 'M':
                    number *= 1000000
                elif unit == 'B':
                    number *= 1000000000
            
            return int(number)
        
        return 0

