from .news_api import get_news, extract_hot_topics

def display_hot_topics(city):
    news_data = get_news(city)
    if news_data:
        top_topics = extract_hot_topics(news_data)
        if top_topics:
            for i, topic in enumerate(top_topics, start=1):
                print(f"Topic {i}: {topic}")

        else:
            print(f"No relevant topics available for {city}.")
    else:
        print(f"Failed to find news for {city}.")