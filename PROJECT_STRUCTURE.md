# Project Structure

Overview of the YouTube SEO Analyzer project structure and file organization.

```
youtube-seo-analyzer/
│
├── main.py                     # Main application entry point & GUI
├── youtube_analyzer.py         # YouTube video data extraction module
├── seo_engine.py              # SEO analysis and tag generation engine
├── trend_analyzer.py          # Google Trends analysis module
│
├── requirements.txt           # Python package dependencies
├── settings.json              # User settings (created on first save)
│
├── README.md                  # Comprehensive documentation
├── QUICKSTART.md             # Quick start guide
├── CHANGELOG.md              # Version history and changes
├── PROJECT_STRUCTURE.md      # This file
├── LICENSE                   # MIT License
│
├── setup.bat                 # Windows setup script
├── setup.sh                  # Unix/Linux/Mac setup script
├── example_usage.py          # Programmatic usage examples
│
└── .gitignore                # Git ignore patterns

```

## File Descriptions

### Core Application Files

#### `main.py` (Primary GUI Application)
The main entry point for the application. Contains:
- `YouTubeSEOAnalyzer` class - Main application controller
- GUI setup and layout using tkinter
- 5 tabbed interfaces:
  - Video Analysis tab
  - SEO Suggestions tab
  - Trend Analysis tab
  - Performance Metrics tab
  - Settings tab
- Threading for non-blocking analysis
- Settings persistence
- Status updates and error handling

**Key Methods:**
- `setup_ui()` - Initialize GUI components
- `analyze_video()` - Orchestrate full video analysis
- `_perform_analysis()` - Execute analysis in separate thread
- `display_*()` - Update UI with results
- `calculate_metrics()` - Compute weighted scores

#### `youtube_analyzer.py` (Video Data Extraction)
Handles all YouTube video data extraction. Contains:
- `YouTubeAnalyzer` class - Video metadata extractor
- Web scraping using requests + BeautifulSoup
- Transcript retrieval using youtube-transcript-api
- Multiple URL format support

**Key Methods:**
- `analyze_video(url)` - Main analysis method
- `extract_video_id(url)` - Parse video ID from various URL formats
- `get_video_metadata(video_id)` - Scrape video page for metadata
- `get_transcript(video_id)` - Retrieve video transcript
- `_parse_metadata()` - Extract data from YouTube's JSON

**Extracted Data:**
- Title, description, channel name
- View count, like count
- Upload date, duration
- Current tags
- Full transcript

#### `seo_engine.py` (SEO Analysis & Tag Generation)
Performs SEO analysis and generates tag suggestions. Contains:
- `SEOEngine` class - SEO analyzer
- NLP processing using NLTK and scikit-learn
- TF-IDF analysis for keyword extraction
- Multiple scoring algorithms

**Key Methods:**
- `analyze_seo(video_data)` - Main SEO analysis
- `analyze_title()` - Title optimization scoring
- `analyze_description()` - Description quality assessment
- `analyze_tags()` - Current tag evaluation
- `analyze_content()` - Overall content quality
- `generate_tags()` - Create tag suggestions
- `extract_keywords_tfidf()` - TF-IDF keyword extraction
- `extract_phrases()` - Multi-word phrase detection

**Analysis Criteria:**
- Title: length (50-70 chars), keywords, power words, numbers
- Description: length (200+ chars), links, timestamps, CTAs
- Tags: count (15-30), variety, specificity
- Content: transcript quality, engagement, consistency

#### `trend_analyzer.py` (Trend Analysis)
Analyzes current trends using Google Trends. Contains:
- `TrendAnalyzer` class - Trend analyzer
- pytrends integration for Google Trends data
- Rate limiting awareness
- Trend scoring algorithms

**Key Methods:**
- `analyze_trends()` - Main trend analysis
- `extract_video_keywords()` - Extract searchable keywords
- `get_trending_topics()` - Query Google Trends for topics
- `get_related_trends()` - Find related trending queries
- `calculate_trend_score()` - Score trend alignment

**Trend Data:**
- Interest over time for keywords
- Rising related queries
- Top related searches
- Regional trend variations
- Trend momentum (rising/falling)

### Configuration Files

#### `requirements.txt`
Python package dependencies with version specifications:
- Web scraping: requests, beautifulsoup4
- YouTube: youtube-transcript-api
- NLP: nltk, scikit-learn
- Trends: pytrends
- Data: pandas, numpy

#### `settings.json` (Auto-generated)
User preferences saved in JSON format:
```json
{
  "weights": {
    "title_weight": 20,
    "description_weight": 15,
    "tag_weight": 25,
    "content_weight": 20,
    "trend_weight": 20
  },
  "num_tags": 30,
  "region": "US",
  "timeframe": "7d"
}
```

### Documentation Files

#### `README.md`
Comprehensive documentation including:
- Feature overview
- Installation instructions
- Usage guide
- Metric explanations
- Troubleshooting
- Technical details
- Future enhancements

#### `QUICKSTART.md`
Quick start guide with:
- 5-minute setup
- First analysis walkthrough
- Example workflow
- Tips and best practices
- Common issues

#### `CHANGELOG.md`
Version history tracking:
- Release dates
- New features
- Bug fixes
- Breaking changes
- Future plans

### Setup Files

#### `setup.bat` (Windows)
Automated setup script for Windows:
- Checks Python installation
- Upgrades pip
- Installs all dependencies
- Provides status feedback

#### `setup.sh` (Unix/Linux/Mac)
Automated setup script for Unix-like systems:
- Checks Python3 installation
- Upgrades pip
- Installs all dependencies
- Provides status feedback

### Example Files

#### `example_usage.py`
Demonstrates programmatic usage:
- Single video analysis
- Batch analysis
- Video comparison
- No GUI required

## Module Dependencies

```
main.py
├── youtube_analyzer.py
│   ├── requests
│   ├── beautifulsoup4
│   └── youtube_transcript_api
├── seo_engine.py
│   ├── nltk
│   └── scikit-learn
└── trend_analyzer.py
    └── pytrends
```

## Data Flow

```
User Input (URL)
    ↓
youtube_analyzer.py
    ↓
Video Data (metadata, transcript)
    ↓
    ├→ seo_engine.py → SEO Results (tags, scores, suggestions)
    └→ trend_analyzer.py → Trend Results (trending topics, trend tags)
    ↓
main.py (calculate_metrics)
    ↓
Display Results (GUI)
```

## Extension Points

To extend the application:

1. **Add New Metrics**
   - Modify `seo_engine.py` - add new `analyze_*()` method
   - Update `main.py` - add to metrics calculation
   - Add to Settings tab for weight customization

2. **New Data Sources**
   - Create new module (e.g., `competitor_analyzer.py`)
   - Import in `main.py`
   - Add new tab in GUI for results

3. **Export Functionality**
   - Add export methods to respective analyzer classes
   - Create export button in GUI
   - Support CSV, JSON, PDF formats

4. **API Integration**
   - Add YouTube Data API support in `youtube_analyzer.py`
   - Requires API key configuration
   - More reliable metrics

## Best Practices

When modifying the code:

1. **Maintain Modularity**
   - Keep analyzers independent
   - Use clear interfaces between modules
   - Avoid circular dependencies

2. **Error Handling**
   - Gracefully handle API failures
   - Provide fallback mechanisms
   - Show user-friendly error messages

3. **Performance**
   - Use threading for long operations
   - Cache trend data when appropriate
   - Respect API rate limits

4. **UI Updates**
   - Always use `root.after()` for GUI updates from threads
   - Provide progress feedback
   - Disable buttons during analysis

## Testing

To test individual components:

```python
# Test YouTube analyzer
from youtube_analyzer import YouTubeAnalyzer
analyzer = YouTubeAnalyzer()
data = analyzer.analyze_video("VIDEO_URL")

# Test SEO engine
from seo_engine import SEOEngine
seo = SEOEngine()
results = seo.analyze_seo(data)

# Test trend analyzer
from trend_analyzer import TrendAnalyzer
trends = TrendAnalyzer()
trend_results = trends.analyze_trends(data)
```

---

For questions or contributions, see the main [README.md](README.md).

