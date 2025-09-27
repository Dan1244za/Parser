#!/usr/bin/env python3
"""
Flask Web Application for News Parser
Provides a web interface to view and analyze parsed news articles.
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os
from datetime import datetime
from news_parser import NewsParser

app = Flask(__name__)

# Global variable to store parser instance
parser = None

@app.route('/')
def index():
    """Main page showing news dashboard."""
    global parser
    
    if parser is None or not parser.parsed_news:
        return render_template('index.html', 
                             has_data=False, 
                             message="No news data available. Please run the parser first.")
    
    # Get filter parameters
    category = request.args.get('category', '')
    sentiment_filter = request.args.get('sentiment', '')
    source_filter = request.args.get('source', '')
    
    # Filter articles
    articles = parser.parsed_news
    
    if category:
        articles = [a for a in articles if a['category'].lower() == category.lower()]
    
    if sentiment_filter:
        if sentiment_filter == 'positive':
            articles = [a for a in articles if a['sentiment_polarity'] > 0.1]
        elif sentiment_filter == 'negative':
            articles = [a for a in articles if a['sentiment_polarity'] < -0.1]
        elif sentiment_filter == 'neutral':
            articles = [a for a in articles if -0.1 <= a['sentiment_polarity'] <= 0.1]
    
    if source_filter:
        articles = [a for a in articles if source_filter.lower() in a['source'].lower()]
    
    # Get unique categories and sources for filter dropdowns
    categories = list(set([a['category'] for a in parser.parsed_news]))
    sources = list(set([a['source'] for a in parser.parsed_news]))
    
    return render_template('index.html',
                         articles=articles,
                         summary=parser.analysis_results,
                         categories=categories,
                         sources=sources,
                         has_data=True,
                         current_category=category,
                         current_sentiment=sentiment_filter,
                         current_source=source_filter)

@app.route('/parse')
def parse_news():
    """Parse news from all sources."""
    global parser
    
    try:
        parser = NewsParser()
        results = parser.parse_all_news()
        parser.save_results()
        
        return jsonify({
            'success': True,
            'message': f'Successfully parsed {results["total_articles"]} articles',
            'total_articles': results['total_articles']
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error parsing news: {str(e)}'
        }), 500

@app.route('/article/<int:article_id>')
def view_article(article_id):
    """View detailed information about a specific article."""
    global parser
    
    if parser is None or not parser.parsed_news:
        return "No news data available", 404
    
    if 0 <= article_id < len(parser.parsed_news):
        article = parser.parsed_news[article_id]
        return render_template('article_detail.html', article=article, article_id=article_id)
    else:
        return "Article not found", 404

@app.route('/api/articles')
def api_articles():
    """API endpoint to get articles in JSON format."""
    global parser
    
    if parser is None or not parser.parsed_news:
        return jsonify({'error': 'No news data available'}), 404
    
    # Get filter parameters
    category = request.args.get('category', '')
    sentiment = request.args.get('sentiment', '')
    limit = int(request.args.get('limit', 50))
    
    articles = parser.parsed_news[:limit]
    
    if category:
        articles = [a for a in articles if a['category'].lower() == category.lower()]
    
    if sentiment:
        if sentiment == 'positive':
            articles = [a for a in articles if a['sentiment_polarity'] > 0.1]
        elif sentiment == 'negative':
            articles = [a for a in articles if a['sentiment_polarity'] < -0.1]
        elif sentiment == 'neutral':
            articles = [a for a in articles if -0.1 <= a['sentiment_polarity'] <= 0.1]
    
    return jsonify({
        'articles': articles,
        'total': len(articles),
        'summary': parser.analysis_results
    })

@app.route('/api/stats')
def api_stats():
    """API endpoint to get analysis statistics."""
    global parser
    
    if parser is None or not parser.parsed_news:
        return jsonify({'error': 'No news data available'}), 404
    
    return jsonify(parser.analysis_results)

@app.route('/search')
def search():
    """Search articles by keyword."""
    global parser
    
    if parser is None or not parser.parsed_news:
        return jsonify({'error': 'No news data available'}), 404
    
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify({'articles': [], 'total': 0})
    
    # Search in title, summary, and keywords
    results = []
    for article in parser.parsed_news:
        if (query in article['title'].lower() or 
            query in article['summary'].lower() or 
            any(query in kw.lower() for kw in article['keywords'])):
            results.append(article)
    
    return jsonify({
        'articles': results,
        'total': len(results),
        'query': query
    })

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)