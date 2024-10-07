import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_news(city):
    api_key = os.getenv('API_KEY')
    url = f"https://newsapi.org/v2/everything?q={city}&apiKey={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error when fetching news for {city}: {e}")
        return {}
    

def extract_hot_topics(news_data):
    articles = news_data.get('articles', [])
    topics = [articles['title'] for articles in articles]
    return topics[:5]
    

