import requests
import os
from dotenv import load_dotenv
import re
from collections import Counter
from difflib import SequenceMatcher
from itertools import islice

load_dotenv()

GNEWS_API_KEY = os.getenv('GNEWS_API_KEY')

def extract_keywords(content, n=1):
    words = re.findall(r'\b\w+\b', content.lower())
    stopwords = set([
        "the", "and", "to", "of", "in", "a", "on", "for", "with", 
        "at", "by", "from", "it", "is", "was", "as", "that", "this", 
        "have", "be", "which", "are", "or", "an", "but", "not", "you", 
        "i", "we", "he", "she", "they", "us", "our", "their", "his", "her", 
        "about", "over", "under", "more", "than", "if", "while", "however"
    ])
    keywords = [word for word in words if word not in stopwords and len(word) > 2]
    
    ngrams = zip(*[islice(keywords, i, None) for i in range(n)])
    ngrams_list = [' '.join(ngram) for ngram in ngrams]
    
    return ngrams_list


def fetch_news(city):
    url = f"https://gnews.io/api/v4/search?q={city}&lang=en&token={GNEWS_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('articles', [])
    else:
        print(f"Error fetching news for city {city}: {response.status_code}")
        return []


def filter_similar_topics(hot_topics, similarity_threshold=0.7):
    unique_topics = []
    
    for topic in hot_topics:
        if not any(SequenceMatcher(None, topic, unique_topic).ratio() > similarity_threshold for unique_topic in unique_topics):
            unique_topics.append(topic)
    
    return unique_topics


def extract_hot_topics(articles, n=2, num_topics=5, min_count=2):
    keyword_counter = Counter()
    used_words = set()  

    for article in articles:
        title = article.get('title') or ''
        description = article.get('description') or ''
        content = title + " " + description
        keywords = extract_keywords(content, n=n) 
        keyword_counter.update(keywords)

    hot_topics = []
    
    for phrase, count in keyword_counter.most_common():
        if count < min_count:
            continue
        
        words = phrase.split()
        if len(set(words)) == len(words) and not used_words.intersection(words):
            hot_topics.append(phrase)
            used_words.update(words)
        
        if len(hot_topics) >= num_topics:
            break
    
    return hot_topics


def get_gnews_topics(city, n=2, num_topics=5):
    articles = fetch_news(city)
    if articles:
        hot_topics = extract_hot_topics(articles, n=n, num_topics=num_topics)
    else:
        hot_topics = []
    
    return hot_topics
