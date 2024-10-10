from .news_api import extract_hot_topics, get_news_topics

def display_hot_topics(city):
    news_data = get_news_topics(city)
    if news_data:
        top_topics = extract_hot_topics(news_data)
        if top_topics:
            for i, topic in enumerate(top_topics, start=1):
                print(f"Topic {i}: {topic}")

        else:
            print(f"No relevant topics available for {city}.")
    else:
        print(f"Failed to find news for {city}.")