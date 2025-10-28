# YouTube SEO Analyzer

An advanced SEO analysis tool designed to scan and analyze YouTube videos, providing comprehensive tag suggestions and optimization recommendations based on current trends and customizable performance metrics.

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Features

### 🎯 Comprehensive Video Analysis
- **Metadata Extraction**: Automatically extracts title, description, tags, views, likes, and channel information
- **Transcript Analysis**: Retrieves and analyzes video transcripts for content-based tag suggestions
- **Engagement Metrics**: Analyzes view counts, likes, and engagement rates

### 🏷️ Intelligent Tag Suggestions
- **🤖 ML-Based Tag Prediction**: Uses AI models to intelligently predict tags (NEW!)
  - Zero-shot classification for content categorization
  - Semantic similarity analysis for contextual tags
  - Clustering-based tag discovery
  - Quality metrics and tag explanations
  - All models run locally - no API keys required
- **TF-IDF Analysis**: Uses advanced natural language processing to identify key terms
- **Keyword Extraction**: Identifies the most relevant keywords from video content
- **Phrase Detection**: Suggests multi-word tags for better specificity
- **Smart Filtering**: Removes generic and overused tags

### 📈 Advanced Trend Prediction & Analysis
- **Google Trends Integration**: Analyzes current search trends related to your video content
- **Trend Lifecycle Detection**: Identifies if trends are emerging, growing, peaking, or declining
- **Velocity & Acceleration Analysis**: Measures how fast trends are rising or falling
- **Momentum Scoring**: Multi-factor analysis combining growth, velocity, consistency, and level
- **Trend Forecasting**: Predicts future trend values using exponential smoothing
- **Viral Detection**: Identifies anomalous spikes indicating viral potential
- **Seasonality Analysis**: Detects recurring patterns in trend data
- **Cross-Correlation**: Analyzes relationships between multiple trending keywords
- **Rising Topics**: Identifies trending topics in your niche
- **Related Queries**: Suggests tags based on what people are actively searching for
- **Regional Customization**: Analyze trends for specific geographic regions
- **Timeframe Flexibility**: Choose from daily, weekly, monthly, or quarterly trend data

### 📊 Performance Metrics & Scoring
- **Overall SEO Score**: Get a comprehensive score (0-100) for your video's SEO optimization
- **Detailed Breakdown**: Individual scores for:
  - Title Optimization
  - Description Quality
  - Tag Relevance
  - Content Quality
  - Trend Alignment
- **Customizable Weights**: Adjust the importance of each metric based on your goals
- **Actionable Feedback**: Receive specific recommendations for improvement

### ⚙️ Customizable Settings
- **Metric Weights**: Adjust how different factors contribute to your overall SEO score
- **Tag Count**: Choose how many tags to generate (10-50)
- **Regional Trends**: Select your target region (US, GB, CA, AU, IN, or Worldwide)
- **Timeframes**: Analyze trends from the past day, week, month, or quarter
- **Persistent Settings**: Your preferences are saved automatically

### 🎨 User-Friendly GUI
- **Modern Interface**: Clean, intuitive design with organized tabs
- **Real-Time Analysis**: Progress updates during analysis
- **Easy Copy**: One-click copy of suggested tags
- **Multiple Views**: Separate tabs for different aspects of analysis

## Installation

### Prerequisites
- Python 3.9 or higher
- pip (Python package installer)

### Setup

1. Clone or download this repository:
```bash
git clone https://github.com/yourusername/youtube-seo-analyzer.git
cd youtube-seo-analyzer
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Download required NLTK data (automatic on first run):
The application will automatically download necessary NLTK data files on first launch.

## Usage

### Starting the Application

Run the main application:
```bash
python main.py
```

### Analyzing a Video

1. **Enter YouTube URL**: Paste any YouTube video URL in the input field
   - Supports various formats: `youtube.com/watch?v=...`, `youtu.be/...`, etc.

2. **Click "Analyze Video"**: The application will:
   - Extract video metadata
   - Retrieve and analyze the transcript
   - Generate SEO tag suggestions
   - Analyze current trends
   - Calculate performance metrics

3. **Review Results** across five tabs:

#### 📹 Video Analysis Tab
- Complete video information
- Current metadata and description
- Existing tags
- Transcript summary

#### 🏷️ SEO Suggestions Tab
- Comprehensive list of suggested tags
- One-click copy functionality
- Specific optimization recommendations
- Actionable improvement tips

#### 📈 Trend Analysis Tab
- Current trending topics with comprehensive metrics:
  - Trend lifecycle phase (emerging, growing, peak, mature, declining)
  - Velocity and acceleration indicators
  - Momentum scores and direction
  - Viral potential alerts
  - Future trend forecasts with confidence levels
  - Cross-correlation with related trends
- Rising search queries
- Trend-based tag suggestions with detailed explanations
- Strategic recommendations based on trend analysis

#### 📊 Performance Metrics Tab
- Overall SEO score with color coding:
  - 🟢 Green (80-100): Excellent
  - 🟡 Yellow (60-79): Good
  - 🔴 Red (0-59): Needs Improvement
- Detailed breakdown of individual metrics
- Specific feedback for each category
- Prioritized recommendations

#### ⚙️ Settings Tab
- Adjust metric weights to match your goals
- Configure number of suggested tags
- Select target region for trend analysis
- Choose trend analysis timeframe
- Save preferences for future sessions

### Tips for Best Results

1. **Use Complete Information**: Videos with detailed descriptions and transcripts yield better suggestions
2. **Leverage ML Tags**: Combine ML-predicted tags with traditional tags for maximum discoverability
3. **Regular Analysis**: Re-analyze videos periodically as trends change
4. **Test Different Regions**: Try different regional settings if you have an international audience
5. **Adjust Weights**: Customize metric weights based on your specific goals (e.g., prioritize trend alignment for viral content)
6. **Monitor Trends**: Use shorter timeframes (1-7 days) for rapidly changing niches
7. **Trust the AI**: ML-predicted tags often discover relevant categories you might not have considered
8. **Combine Methods**: Use both ML and traditional tags for the best coverage

## Understanding the Metrics

### Title Optimization (Default: 20%)
Evaluates:
- Length (optimal: 50-70 characters)
- Keyword placement
- Use of power words
- Numbers and formatting

### Description Quality (Default: 15%)
Evaluates:
- Length and detail
- Presence of links and timestamps
- Call-to-action inclusion
- Hashtag usage

### Tag Relevance (Default: 25%)
Evaluates:
- Number of tags (optimal: 15-30)
- Mix of short and long-tail tags
- Tag variety and specificity
- Avoidance of generic tags

### Content Quality (Default: 20%)
Evaluates:
- Transcript availability and length
- Engagement metrics
- Keyword consistency across title, description, and content

### Trend Alignment (Default: 20%)
Evaluates:
- Use of trending keywords
- Alignment with related trends
- Topic momentum
- Content timeliness

## Technical Details

### Architecture

The application consists of four main modules:

1. **main.py**: GUI application and orchestration
2. **youtube_analyzer.py**: Video data extraction and metadata parsing
3. **seo_engine.py**: SEO analysis and tag generation using NLP
4. **trend_analyzer.py**: Real-time trend analysis using Google Trends

### Data Sources

- **YouTube**: Video metadata, transcripts, and engagement metrics
- **Google Trends**: Search trend data, related queries, and rising topics
- **NLP Analysis**: TF-IDF vectorization, keyword frequency, and phrase extraction

### Privacy & Data

- All analysis is performed locally on your machine
- No video data is stored or transmitted to third parties
- Trend data comes from public Google Trends API
- Settings are saved locally in `settings.json`

## Troubleshooting

### "Invalid YouTube URL"
- Ensure the URL is complete and properly formatted
- Try copying the URL directly from the browser address bar

### "Transcript not available"
- Some videos don't have transcripts (disabled by creator or auto-captions unavailable)
- Analysis will still work but may have fewer tag suggestions

### "Trend analysis unavailable"
- May occur due to rate limiting from Google Trends
- Wait a few minutes and try again
- Try analyzing with fewer/different keywords

### Import Errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Update pip: `python -m pip install --upgrade pip`
- Try installing packages individually if bulk install fails

### NLTK Data Errors
- The application downloads required data automatically
- If issues persist, manually download:
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

## Limitations

- **Rate Limiting**: Google Trends API has rate limits; avoid analyzing too many videos in quick succession
- **Transcript Availability**: Not all videos have transcripts
- **Metadata Access**: Some video metadata may be restricted or unavailable
- **Trend Data**: Trend analysis requires active internet connection

## Machine Learning Tag Prediction

The tool now includes **ML-based tag prediction** using local AI models:

### Features:
- **Zero-Shot Classification**: Automatically categorizes content using Facebook's BART model
- **Semantic Analysis**: Finds contextually relevant tags using sentence transformers
- **Clustering**: Discovers hidden patterns and tag groups
- **Quality Metrics**: Provides diversity and quality scores for generated tags
- **Tag Explanations**: Shows why each tag was predicted

### Requirements:
```bash
pip install transformers sentence-transformers torch
```

### Key Benefits:
- ✅ **100% Free** - No API keys or subscriptions required
- ✅ **Privacy-Friendly** - All processing happens locally on your computer
- ✅ **No Rate Limits** - Unlimited analyses
- ✅ **Offline Ready** - Works without internet (after initial model download)

For detailed information, see [ML_TAG_PREDICTION.md](ML_TAG_PREDICTION.md)

## Future Enhancements

Potential features for future versions:
- YouTube Data API integration for official metrics
- Historical performance tracking
- A/B testing suggestions
- Competitor analysis
- Batch video analysis
- Export reports to PDF/CSV
- Video upload preview analysis
- Multi-language ML support
- Fine-tuned YouTube-specific models

## Enhanced Trend Prediction Algorithms

The tool now includes sophisticated trend analysis algorithms:

### Key Features:
1. **Time Series Analysis**: Calculate trend velocity (rate of change) and acceleration
2. **Lifecycle Detection**: Identify if trends are emerging, growing, at peak, mature, or declining
3. **Forecasting**: Predict future trend values with confidence levels
4. **Anomaly Detection**: Spot viral spikes and unusual trend patterns
5. **Momentum Analysis**: Multi-factor scoring combining multiple trend indicators
6. **Seasonality Detection**: Identify recurring patterns in trend data
7. **Cross-Correlation**: Find related trends that move together

### How It Helps:
- **Emerging Trends**: Get in early before competition increases
- **Viral Potential**: Identify trends showing explosive growth patterns
- **Declining Trends**: Avoid keywords losing relevance
- **Strategic Timing**: Match content releases to trend momentum
- **Synergy Discovery**: Find related keywords that work well together

For detailed information, see [ENHANCED_TREND_ALGORITHMS.md](ENHANCED_TREND_ALGORITHMS.md)

## Contributing

Contributions are welcome! Areas for improvement:
- Additional metric calculations
- UI/UX improvements
- Performance optimizations
- Additional language support
- ~~Machine learning integrations~~ ✅ Added in v1.1.0!
- Fine-tuning ML models for YouTube-specific content
- Multi-language ML support

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for educational and analytical purposes. Always follow YouTube's Terms of Service and Community Guidelines. The SEO suggestions are recommendations based on analysis algorithms and should be used as guidance alongside your own judgment and YouTube's best practices.

## Acknowledgments

- **YouTube Transcript API**: For transcript extraction
- **Google Trends (pytrends)**: For trend analysis
- **NLTK & scikit-learn**: For natural language processing
- **Beautiful Soup**: For web scraping capabilities

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review the Troubleshooting section

---

**Made with ❤️ for content creators looking to optimize their YouTube presence**
