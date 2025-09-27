# News Parser Application

A comprehensive news parsing and analysis tool that fetches news from multiple sources, analyzes content using natural language processing, and provides insights through a modern web interface.

## Features

### 🔍 Multi-Source News Fetching
- **RSS Feeds**: BBC, CNN, Reuters, NPR, O'Reilly Radar
- **API Integration**: NewsAPI support (with API key)
- **Extensible**: Easy to add new sources

### 📊 Advanced Analysis
- **Sentiment Analysis**: Polarity and subjectivity scoring
- **Content Categorization**: Automatic categorization (Technology, Politics, Business, Health, Sports, Science, Entertainment)
- **Keyword Extraction**: Automatic keyword identification and scoring
- **Source Analysis**: Track news distribution across sources

### 🌐 Modern Web Interface
- **Responsive Dashboard**: Clean, modern interface built with Bootstrap
- **Interactive Filtering**: Filter by category, sentiment, and source
- **Detailed Views**: Individual article analysis pages
- **Real-time Statistics**: Live charts and metrics
- **Search Functionality**: Find articles by keywords

### 📈 Analytics & Insights
- Category distribution charts
- Source analysis
- Sentiment trends
- Keyword frequency analysis
- Export capabilities (JSON format)

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd news-parser
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download NLTK data** (if not automatically downloaded)
   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('stopwords')
   ```

4. **Optional: Configure NewsAPI**
   - Get a free API key from [NewsAPI](https://newsapi.org/)
   - Replace `YOUR_API_KEY_HERE` in `news_parser.py` with your actual API key

## Usage

### Command Line Interface

Run the news parser directly:

```bash
python news_parser.py
```

This will:
- Fetch news from all configured sources
- Perform sentiment analysis and categorization
- Generate summary statistics
- Save results to `news_analysis.json`

### Web Interface

Start the Flask web application:

```bash
python app.py
```

Then open your browser and navigate to:
```
http://localhost:5000
```

### Web Interface Features

1. **Dashboard**: Overview of all parsed news with statistics
2. **Filtering**: Filter articles by category, sentiment, or source
3. **Search**: Search articles by keywords
4. **Article Details**: View detailed analysis for individual articles
5. **API Endpoints**: RESTful API for programmatic access

## API Endpoints

### GET `/api/articles`
Returns articles in JSON format with optional filtering.

**Parameters:**
- `category`: Filter by category
- `sentiment`: Filter by sentiment (positive, negative, neutral)
- `limit`: Maximum number of articles to return

**Example:**
```
GET /api/articles?category=Technology&sentiment=positive&limit=10
```

### GET `/api/stats`
Returns analysis statistics.

### GET `/search?q=keyword`
Search articles by keyword.

## Configuration

### Adding News Sources

#### RSS Feeds
Add new RSS feeds to the `rss_feeds` list in `news_parser.py`:

```python
self.news_sources = {
    'rss_feeds': [
        'https://feeds.bbci.co.uk/news/rss.xml',
        'https://your-new-feed-url.com/rss.xml',  # Add here
        # ... other feeds
    ]
}
```

#### API Sources
Add new API sources to the `api_sources` dictionary:

```python
'api_sources': {
    'your_api': {
        'url': 'https://api.example.com/news',
        'params': {
            'api_key': 'your_api_key',
            'format': 'json'
        }
    }
}
```

### Customizing Analysis

#### Adding Categories
Modify the `categorize_news` method to add new categories:

```python
categories = {
    'Your Category': ['keyword1', 'keyword2', 'keyword3'],
    # ... existing categories
}
```

#### Sentiment Analysis
The application uses TextBlob for sentiment analysis. You can enhance it by:
- Training custom models
- Using more sophisticated NLP libraries
- Adding domain-specific sentiment dictionaries

## File Structure

```
news-parser/
├── news_parser.py          # Main parser class and logic
├── app.py                  # Flask web application
├── requirements.txt        # Python dependencies
├── templates/              # HTML templates
│   ├── base.html          # Base template
│   ├── index.html        # Dashboard template
│   └── article_detail.html # Article detail template
├── static/                 # Static assets (CSS, JS)
├── news_analysis.json     # Generated analysis results
└── README.md              # This file
```

## Dependencies

- **requests**: HTTP library for API calls
- **beautifulsoup4**: HTML/XML parsing
- **feedparser**: RSS/Atom feed parsing
- **flask**: Web framework
- **pandas**: Data manipulation and analysis
- **nltk**: Natural language processing
- **textblob**: Sentiment analysis
- **newspaper3k**: Article extraction
- **lxml**: XML/HTML processing

## Performance Considerations

- **Rate Limiting**: Be respectful of news source rate limits
- **Caching**: Consider implementing caching for frequently accessed data
- **Async Processing**: For large-scale parsing, consider async/await patterns
- **Database Storage**: For production use, consider using a database instead of JSON files

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Future Enhancements

- [ ] Database integration (SQLite/PostgreSQL)
- [ ] Real-time news updates
- [ ] Advanced NLP models
- [ ] Machine learning for better categorization
- [ ] Email notifications for specific topics
- [ ] Mobile app interface
- [ ] Docker containerization
- [ ] Cloud deployment guides

## Troubleshooting

### Common Issues

1. **ImportError: No module named 'nltk'**
   ```bash
   pip install nltk
   ```

2. **SSL Certificate Errors**
   ```bash
   pip install --upgrade certifi
   ```

3. **NewsAPI Rate Limiting**
   - Check your API key
   - Ensure you're not exceeding rate limits
   - Consider upgrading to a paid plan

4. **RSS Feed Parsing Errors**
   - Some feeds may be temporarily unavailable
   - Check feed URLs manually
   - Consider adding error handling for specific feeds

### Getting Help

- Check the [Issues](https://github.com/your-username/news-parser/issues) page
- Create a new issue with detailed error information
- Include your Python version and operating system

---

**Built with ❤️ for the developer community**