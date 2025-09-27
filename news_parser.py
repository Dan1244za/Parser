#!/usr/bin/env python3
"""
News Parser Application
A comprehensive news parsing and analysis tool that fetches news from multiple sources,
analyzes content, and provides insights through a web interface.
"""

import requests
import feedparser
import json
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any
from bs4 import BeautifulSoup
from textblob import TextBlob
import pandas as pd
from newspaper import Article
import nltk
from urllib.parse import urljoin, urlparse

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class NewsParser:
    """Main news parser class that handles fetching and analyzing news from multiple sources."""
    
    def __init__(self):
        self.news_sources = {
            'rss_feeds': [
                'https://feeds.bbci.co.uk/news/rss.xml',
                'https://rss.cnn.com/rss/edition.rss',
                'https://feeds.reuters.com/reuters/topNews',
                'https://feeds.npr.org/1001/rss.xml',
                'https://feeds.feedburner.com/oreilly/radar'
            ],
            'api_sources': {
                'newsapi': {
                    'url': 'https://newsapi.org/v2/top-headlines',
                    'params': {
                        'apiKey': 'YOUR_API_KEY_HERE',  # Replace with actual API key
                        'country': 'us',
                        'pageSize': 20
                    }
                }
            }
        }
        self.parsed_news = []
        self.analysis_results = {}
    
    def fetch_rss_news(self) -> List[Dict[str, Any]]:
        """Fetch news from RSS feeds."""
        print("Fetching news from RSS feeds...")
        rss_news = []
        
        for feed_url in self.news_sources['rss_feeds']:
            try:
                feed = feedparser.parse(feed_url)
                print(f"Processing {feed_url}: {len(feed.entries)} articles")
                
                for entry in feed.entries[:10]:  # Limit to 10 articles per feed
                    article_data = {
                        'title': entry.get('title', ''),
                        'link': entry.get('link', ''),
                        'summary': entry.get('summary', ''),
                        'published': entry.get('published', ''),
                        'source': feed.feed.get('title', 'Unknown'),
                        'source_type': 'RSS',
                        'feed_url': feed_url
                    }
                    rss_news.append(article_data)
                    
            except Exception as e:
                print(f"Error fetching from {feed_url}: {str(e)}")
                continue
        
        return rss_news
    
    def fetch_api_news(self) -> List[Dict[str, Any]]:
        """Fetch news from API sources."""
        print("Fetching news from API sources...")
        api_news = []
        
        for source_name, source_config in self.news_sources['api_sources'].items():
            try:
                if source_name == 'newsapi':
                    # Skip if no API key provided
                    if 'YOUR_API_KEY_HERE' in source_config['params']['apiKey']:
                        print("Skipping NewsAPI - no API key provided")
                        continue
                    
                    response = requests.get(source_config['url'], params=source_config['params'])
                    if response.status_code == 200:
                        data = response.json()
                        for article in data.get('articles', []):
                            article_data = {
                                'title': article.get('title', ''),
                                'link': article.get('url', ''),
                                'summary': article.get('description', ''),
                                'published': article.get('publishedAt', ''),
                                'source': article.get('source', {}).get('name', 'Unknown'),
                                'source_type': 'API',
                                'api_source': source_name
                            }
                            api_news.append(article_data)
                            
            except Exception as e:
                print(f"Error fetching from {source_name}: {str(e)}")
                continue
        
        return api_news
    
    def extract_full_article(self, url: str) -> Dict[str, str]:
        """Extract full article content from URL."""
        try:
            article = Article(url)
            article.download()
            article.parse()
            
            return {
                'full_text': article.text,
                'authors': article.authors,
                'publish_date': str(article.publish_date) if article.publish_date else '',
                'top_image': article.top_image,
                'keywords': article.keywords
            }
        except Exception as e:
            print(f"Error extracting article from {url}: {str(e)}")
            return {}
    
    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Analyze sentiment of text using TextBlob."""
        if not text:
            return {'polarity': 0.0, 'subjectivity': 0.0}
        
        blob = TextBlob(text)
        return {
            'polarity': blob.sentiment.polarity,
            'subjectivity': blob.sentiment.subjectivity
        }
    
    def categorize_news(self, title: str, summary: str) -> str:
        """Categorize news based on keywords in title and summary."""
        text = f"{title} {summary}".lower()
        
        categories = {
            'Technology': ['tech', 'ai', 'artificial intelligence', 'software', 'computer', 'digital', 'cyber', 'data', 'internet', 'app', 'startup'],
            'Politics': ['president', 'congress', 'senate', 'election', 'vote', 'government', 'policy', 'law', 'political'],
            'Business': ['business', 'economy', 'market', 'stock', 'company', 'corporate', 'finance', 'financial', 'trading'],
            'Health': ['health', 'medical', 'doctor', 'hospital', 'disease', 'covid', 'pandemic', 'medicine', 'healthcare'],
            'Sports': ['sport', 'football', 'basketball', 'baseball', 'soccer', 'olympics', 'game', 'player', 'team'],
            'Science': ['science', 'research', 'study', 'discovery', 'space', 'climate', 'environment', 'energy'],
            'Entertainment': ['movie', 'film', 'music', 'celebrity', 'entertainment', 'show', 'actor', 'singer']
        }
        
        for category, keywords in categories.items():
            if any(keyword in text for keyword in keywords):
                return category
        
        return 'General'
    
    def extract_keywords(self, text: str, num_keywords: int = 10) -> List[str]:
        """Extract key terms from text."""
        if not text:
            return []
        
        # Simple keyword extraction (can be enhanced with more sophisticated methods)
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        
        # Remove common stopwords
        stopwords = set(['the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'its', 'may', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'man', 'oil', 'sit', 'yes', 'yet'])
        words = [word for word in words if word not in stopwords]
        
        # Count word frequency
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Return top keywords
        return sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:num_keywords]
    
    def parse_all_news(self) -> Dict[str, Any]:
        """Parse news from all sources and perform analysis."""
        print("Starting news parsing and analysis...")
        
        # Fetch news from all sources
        all_news = []
        all_news.extend(self.fetch_rss_news())
        all_news.extend(self.fetch_api_news())
        
        print(f"Total articles fetched: {len(all_news)}")
        
        # Analyze each article
        analyzed_news = []
        for i, article in enumerate(all_news):
            print(f"Analyzing article {i+1}/{len(all_news)}: {article['title'][:50]}...")
            
            # Combine title and summary for analysis
            full_text = f"{article['title']} {article['summary']}"
            
            # Perform analysis
            sentiment = self.analyze_sentiment(full_text)
            category = self.categorize_news(article['title'], article['summary'])
            keywords = self.extract_keywords(full_text)
            
            # Add analysis results to article
            article.update({
                'sentiment_polarity': sentiment['polarity'],
                'sentiment_subjectivity': sentiment['subjectivity'],
                'category': category,
                'keywords': [kw[0] for kw in keywords],
                'keyword_scores': dict(keywords),
                'analysis_timestamp': datetime.now().isoformat()
            })
            
            analyzed_news.append(article)
        
        self.parsed_news = analyzed_news
        
        # Generate summary statistics
        self.analysis_results = self.generate_summary_statistics()
        
        return {
            'articles': analyzed_news,
            'summary': self.analysis_results,
            'total_articles': len(analyzed_news),
            'parse_timestamp': datetime.now().isoformat()
        }
    
    def generate_summary_statistics(self) -> Dict[str, Any]:
        """Generate summary statistics from parsed news."""
        if not self.parsed_news:
            return {}
        
        df = pd.DataFrame(self.parsed_news)
        
        # Category distribution
        category_counts = df['category'].value_counts().to_dict()
        
        # Sentiment analysis
        avg_polarity = df['sentiment_polarity'].mean()
        avg_subjectivity = df['sentiment_subjectivity'].mean()
        
        # Source distribution
        source_counts = df['source'].value_counts().to_dict()
        
        # Time analysis (if dates are available)
        recent_articles = len(df)  # Simplified - could parse dates for more accurate analysis
        
        return {
            'category_distribution': category_counts,
            'average_sentiment_polarity': round(avg_polarity, 3),
            'average_sentiment_subjectivity': round(avg_subjectivity, 3),
            'source_distribution': source_counts,
            'total_articles': len(df),
            'recent_articles': recent_articles
        }
    
    def save_results(self, filename: str = 'news_analysis.json'):
        """Save analysis results to JSON file."""
        results = {
            'articles': self.parsed_news,
            'summary': self.analysis_results,
            'parse_timestamp': datetime.now().isoformat()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"Results saved to {filename}")
    
    def get_news_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get news articles filtered by category."""
        return [article for article in self.parsed_news if article['category'].lower() == category.lower()]
    
    def get_news_by_sentiment(self, min_polarity: float = None, max_polarity: float = None) -> List[Dict[str, Any]]:
        """Get news articles filtered by sentiment polarity."""
        filtered = self.parsed_news
        
        if min_polarity is not None:
            filtered = [article for article in filtered if article['sentiment_polarity'] >= min_polarity]
        
        if max_polarity is not None:
            filtered = [article for article in filtered if article['sentiment_polarity'] <= max_polarity]
        
        return filtered


def main():
    """Main function to run the news parser."""
    print("News Parser Application")
    print("=" * 50)
    
    # Initialize parser
    parser = NewsParser()
    
    # Parse all news
    results = parser.parse_all_news()
    
    # Print summary
    print("\nAnalysis Summary:")
    print("-" * 30)
    summary = results['summary']
    print(f"Total articles: {summary['total_articles']}")
    print(f"Average sentiment polarity: {summary['average_sentiment_polarity']}")
    print(f"Average sentiment subjectivity: {summary['average_sentiment_subjectivity']}")
    
    print("\nCategory Distribution:")
    for category, count in summary['category_distribution'].items():
        print(f"  {category}: {count}")
    
    print("\nSource Distribution:")
    for source, count in summary['source_distribution'].items():
        print(f"  {source}: {count}")
    
    # Save results
    parser.save_results()
    
    # Example: Get technology news
    tech_news = parser.get_news_by_category('Technology')
    print(f"\nTechnology articles found: {len(tech_news)}")
    
    # Example: Get positive news
    positive_news = parser.get_news_by_sentiment(min_polarity=0.1)
    print(f"Positive sentiment articles: {len(positive_news)}")


if __name__ == "__main__":
    main()