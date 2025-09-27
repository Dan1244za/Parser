#!/usr/bin/env python3
"""
Demo script for News Parser Application
Shows how to use the parser programmatically and demonstrates key features.
"""

from news_parser import NewsParser
import json
from datetime import datetime

def demo_basic_parsing():
    """Demonstrate basic news parsing functionality."""
    print("=" * 60)
    print("NEWS PARSER DEMO - Basic Functionality")
    print("=" * 60)
    
    # Initialize parser
    parser = NewsParser()
    
    # Parse news from all sources
    print("\n1. Parsing news from all sources...")
    results = parser.parse_all_news()
    
    print(f"\n✅ Successfully parsed {results['total_articles']} articles")
    
    # Display summary statistics
    print("\n2. Analysis Summary:")
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
    
    return parser

def demo_filtering(parser):
    """Demonstrate filtering capabilities."""
    print("\n" + "=" * 60)
    print("DEMO - Filtering and Analysis")
    print("=" * 60)
    
    # Get technology news
    tech_news = parser.get_news_by_category('Technology')
    print(f"\n🔧 Technology articles: {len(tech_news)}")
    if tech_news:
        print("Sample technology article:")
        article = tech_news[0]
        print(f"  Title: {article['title'][:80]}...")
        print(f"  Source: {article['source']}")
        print(f"  Sentiment: {article['sentiment_polarity']:.3f}")
        print(f"  Keywords: {', '.join(article['keywords'][:5])}")
    
    # Get positive sentiment news
    positive_news = parser.get_news_by_sentiment(min_polarity=0.1)
    print(f"\n😊 Positive sentiment articles: {len(positive_news)}")
    
    # Get negative sentiment news
    negative_news = parser.get_news_by_sentiment(max_polarity=-0.1)
    print(f"😞 Negative sentiment articles: {len(negative_news)}")
    
    # Get neutral sentiment news
    neutral_news = parser.get_news_by_sentiment(min_polarity=-0.1, max_polarity=0.1)
    print(f"😐 Neutral sentiment articles: {len(neutral_news)}")

def demo_article_analysis(parser):
    """Demonstrate detailed article analysis."""
    print("\n" + "=" * 60)
    print("DEMO - Detailed Article Analysis")
    print("=" * 60)
    
    if not parser.parsed_news:
        print("No articles available for analysis.")
        return
    
    # Analyze the first few articles in detail
    print("\nDetailed analysis of first 3 articles:")
    print("-" * 50)
    
    for i, article in enumerate(parser.parsed_news[:3]):
        print(f"\n📰 Article {i+1}: {article['title'][:60]}...")
        print(f"   Source: {article['source']}")
        print(f"   Category: {article['category']}")
        print(f"   Sentiment Polarity: {article['sentiment_polarity']:.3f}")
        print(f"   Sentiment Subjectivity: {article['sentiment_subjectivity']:.3f}")
        print(f"   Top Keywords: {', '.join(article['keywords'][:5])}")
        print(f"   Link: {article['link']}")

def demo_export_functionality(parser):
    """Demonstrate export functionality."""
    print("\n" + "=" * 60)
    print("DEMO - Export Functionality")
    print("=" * 60)
    
    # Save results to JSON
    filename = f"demo_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    parser.save_results(filename)
    print(f"✅ Results saved to {filename}")
    
    # Show file size
    import os
    if os.path.exists(filename):
        size = os.path.getsize(filename)
        print(f"📁 File size: {size:,} bytes ({size/1024:.1f} KB)")

def main():
    """Main demo function."""
    print("🚀 NEWS PARSER APPLICATION DEMO")
    print("This demo showcases the key features of the News Parser application.")
    print("The demo will parse news, analyze content, and demonstrate filtering capabilities.")
    
    try:
        # Run all demo functions
        parser = demo_basic_parsing()
        demo_filtering(parser)
        demo_article_analysis(parser)
        demo_export_functionality(parser)
        
        print("\n" + "=" * 60)
        print("🎉 DEMO COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Run 'python app.py' to start the web interface")
        print("2. Open http://localhost:5000 in your browser")
        print("3. Explore the interactive dashboard")
        print("4. Check the generated JSON files for detailed results")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {str(e)}")
        print("Please check your internet connection and dependencies.")
        print("Make sure all required packages are installed: pip install -r requirements.txt")

if __name__ == "__main__":
    main()