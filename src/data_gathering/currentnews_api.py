import requests
import os
from dotenv import load_dotenv
import re
from collections import Counter
from difflib import SequenceMatcher
from itertools import islice

load_dotenv()

GNEWS_API_KEY = os.getenv('CURRENT_NEWS_API_KEY')

def extract_keywords(content, n=1):
    """
    Extract n-grams from the content. n can be 1 (unigrams), 2 (bigrams), 3 (trigrams), etc.
    Stopwords are filtered out, and only meaningful words are kept.
    """
    words = re.findall(r'\b\w+\b', content.lower())
    stopwords = set([
        "the", "and", "to", "of", "in", "a", "on", "for", "with", 
        "at", "by", "from", "it", "is", "was", "as", "that", "this", 
        "have", "be", "which", "are", "or", "an", "but", "not", "you", 
        "i", "we", "he", "she", "they", "us", "our", "their", "his", "her", 
        "about", "over", "under", "more", "than", "if", "while", "however"
    ])
    keywords = [word for word in words if word not in stopwords and len(word) > 2]
    
    # Generate n-grams
    ngrams = zip(*[islice(keywords, i, None) for i in range(n)])
    ngrams_list = [' '.join(ngram) for ngram in ngrams]
    
    return ngrams_list

def fetch_news(city):
    """
    Fetch news articles for a given city using the GNews API.
    """
    url = f"https://gnews.io/api/v4/search?q={city}&lang=en&token={GNEWS_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('articles', [])
    else:
        print(f"Error fetching news for city {city}: {response.status_code}")
        return []

def filter_similar_topics(hot_topics, similarity_threshold=0.7):
    """
    Remove similar topics based on a similarity threshold using sequence matching.
    """
    unique_topics = []
    
    for topic in hot_topics:
        if not any(SequenceMatcher(None, topic, unique_topic).ratio() > similarity_threshold for unique_topic in unique_topics):
            unique_topics.append(topic)
    
    return unique_topics

def extract_hot_topics(articles, n=2, num_topics=5, min_count=2):
    """
    Extract relevant n-grams (hot topics) from the news articles.
    Ensure no two words in one topic are the same and no word is repeated across topics.
    
    n: The number of words to include in the n-grams (default is 2 for bigrams).
    num_topics: The number of hot topics to return.
    min_count: Minimum count of occurrences for a topic to be considered relevant.
    """
    keyword_counter = Counter()
    used_words = set()  # Track words used in all topics

    for article in articles:
        title = article.get('title') or ''
        description = article.get('description') or ''
        content = title + " " + description
        keywords = extract_keywords(content, n=n)  # Extract n-grams
        keyword_counter.update(keywords)

    hot_topics = []
    
    # Iterate over the most common n-grams
    for phrase, count in keyword_counter.most_common():
        if count < min_count:
            continue
        
        words = phrase.split()
        # Check for duplicate words in the same topic or previously used words
        if len(set(words)) == len(words) and not used_words.intersection(words):
            hot_topics.append(phrase)
            used_words.update(words)
        
        if len(hot_topics) >= num_topics:
            break
    
    return hot_topics

def get_currentnews_topics(city, n=2, num_topics=5):
    """
    Get hot topics (n-grams) from news articles for a specific city.
    n: Number of words in the n-grams (default is 2).
    num_topics: Number of hot topics to return (default is 5).
    """
    articles = fetch_news(city)
    if articles:
        hot_topics = extract_hot_topics(articles, n=n, num_topics=num_topics)
    else:
        hot_topics = []
    
    return hot_topics
