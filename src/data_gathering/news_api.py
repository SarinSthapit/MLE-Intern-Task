import requests
import os
from dotenv import load_dotenv
import requests
import json
from collections import Counter
import re

load_dotenv()

API_KEY = os.getenv('API_KEY')


def extract_keywords(content):
    words = re.findall(r'\b\w+\b', content.lower())
    stopwords = set(["the", "and", "to", "of", "in", "a", "on", "for", "with", "at", "by", "from", "it", "is", "was", "as", "that", "this"])
    keywords = [word for word in words if word not in stopwords and len(word) > 2]
    return keywords


def fetch_news(city):
    url = f"https://newsapi.org/v2/everything?q={city}&apiKey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('articles', [])
    else:
        print(f"Error fetching news for city {city}: {response.status_code}")
        return []


def extract_hot_topics(articles):
    keyword_counter = Counter()
    
    for article in articles:
        title = article.get('title') or ''  
        description = article.get('description') or ''  
        content = title + " " + description
        keywords = extract_keywords(content)
        keyword_counter.update(keywords)
    
    hot_topics = [word for word, count in keyword_counter.most_common(5)]
    return hot_topics


def get_news_topics(city):
    articles = fetch_news(city)
    hot_topics = extract_hot_topics(articles)
    return hot_topics


city = "Kathmandu" 
hot_topics = get_news_topics(city)
print(f"Top 5 hot topics in {city}: {hot_topics}")
