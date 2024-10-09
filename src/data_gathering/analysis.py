import warnings 
import json
import os
from dotenv import load_dotenv
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer, pipeline
import matplotlib.pyplot as plt

# Suppress the resume_download FutureWarning
warnings.filterwarnings("ignore", category=FutureWarning, message="resume_download is deprecated")

from .news_api import get_news_topics
from .reddit_api import gather_all_discussions

# Load environment variables from .env file
load_dotenv()

# Initialize the T5 model and tokenizer
t5_model = T5ForConditionalGeneration.from_pretrained('t5-small', force_download=False)
t5_tokenizer = T5Tokenizer.from_pretrained('t5-small', legacy=False)

# Initialize a sentiment analysis pipeline
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def summarize_text_t5(text):
    """
    Summarize the given text using the T5 model and refine the summary for grammatical accuracy.
    """
    input_text = "summarize: " + text
    inputs = t5_tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)

    summary_ids = t5_model.generate(
        inputs, 
        max_length=550,
        min_length=10,
        length_penalty=1.0,
        num_beams=4, 
        early_stopping=True
    )

    summary = t5_tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    
    # Refine the summary for grammatical accuracy
    refined_summary = refine_summary(summary)
    
    return refined_summary.replace(":", "").strip()

def refine_summary(summary):
    """
    Refine the summary to improve its grammatical accuracy.
    """
    input_text = "refine: " + summary
    inputs = t5_tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)

    refined_ids = t5_model.generate(
        inputs,
        max_length=550,
        min_length=10,
        length_penalty=1.0,
        num_beams=4,
        early_stopping=True
    )

    refined_summary = t5_tokenizer.decode(refined_ids[0], skip_special_tokens=True)
    return refined_summary

def load_discussions(json_path):
    """
    Load discussions from a JSON file.
    """
    with open(json_path, 'r') as f:
        return json.load(f)

def summarize_discussions(discussions):
    """
    Summarize the combined text of all discussions for each topic.
    """
    summaries = {}
    max_input_length = 512

    for topic, discussion_list in discussions.items():
        full_text = " ".join([comment['body'] for discussion in discussion_list for comment in discussion['comments']])
        chunks = [full_text[i:i + max_input_length] for i in range(0, len(full_text), max_input_length)]
        combined_summary = summarize_text_t5(" ".join(chunks))
        summaries[topic] = combined_summary.strip()

    return summaries

def analyze_sentiment(discussions):
    """
    Analyze sentiment of the combined text of all discussions for each topic.
    """
    sentiments = {}
    max_input_length = 512

    for topic, discussion_list in discussions.items():
        full_text = " ".join([comment['body'] for discussion in discussion_list for comment in discussion['comments']])
        chunks = [full_text[i:i + max_input_length] for i in range(0, len(full_text), max_input_length)]
        
        combined_sentiment = []
        for chunk in chunks:
            sentiment = sentiment_analyzer(chunk)
            combined_sentiment.extend(sentiment)

        sentiments[topic] = combined_sentiment

    return sentiments




def overall_sentiment(sentiments):
    """
    Calculate overall sentiment based on the sentiment of discussions.
    Returns a dictionary with counts of positive and negative sentiments.
    """
    overall = {'positive': 0, 'negative': 0}
    
    for topic, sentiment_list in sentiments.items():
        for sentiment in sentiment_list:
            if sentiment['label'] == 'POSITIVE':
                overall['positive'] += 1
            elif sentiment['label'] == 'NEGATIVE':
                overall['negative'] += 1
                
    return overall

def plot_sentiments(sentiments, save_path):
    """
    Plot the sentiment counts for each topic and save the plot.
    """
    topics = []
    positive_counts = []
    negative_counts = []

    for topic, sentiment_list in sentiments.items():
        topics.append(topic)
        positive_count = sum(1 for sentiment in sentiment_list if sentiment['label'] == 'POSITIVE')
        negative_count = sum(1 for sentiment in sentiment_list if sentiment['label'] == 'NEGATIVE')
        positive_counts.append(positive_count)
        negative_counts.append(negative_count)

    x = range(len(topics))
    plt.bar(x, positive_counts, width=0.4, label='Positive', align='center', color='green')
    plt.bar(x, negative_counts, width=0.4, label='Negative', align='edge', color='red')
    plt.xlabel('Topics')
    plt.ylabel('Sentiment Count')
    plt.xticks(x, topics, rotation='vertical')
    plt.title('Sentiment Analysis by Topic')
    plt.legend()
    plt.tight_layout()

    plt.savefig(save_path)
    plt.close()

def analyze_gathered_info():
    """
    Load the discussions from a JSON file, summarize them, analyze their sentiment,
    and extract actionable needs.
    """
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../data/discussions.json')
    discussions = load_discussions(json_path)

    summaries = summarize_discussions(discussions)
    sentiments = analyze_sentiment(discussions)

    return summaries, sentiments

""" 
if __name__ == "__main__":
    # Fetch hot topics from the news for a specific city
    city = "California" 
    hot_topics = get_news_topics(city, n=2, num_topics=5)
    
    # Gather discussions from Reddit based on the hot topics
    gather_all_discussions(hot_topics, limit=5)
    
    # Summarize and analyze sentiment of the gathered discussions
    summaries, sentiments = analyze_gathered_info()
    
    # Print the summaries
    print("Summaries of Discussions:")
    for topic, summary in summaries.items():
        print(f"{topic}: {summary}")
    
    # Print the sentiments
    print("\nSentiments of Discussions:")
    for topic, sentiment in sentiments.items():
        print(f"{topic}: {sentiment}")
    
    
    # Plot the sentiments
    static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../static')
    plot_path = os.path.join(static_folder, 'sentiment_analysis.png')
    plot_sentiments(sentiments, plot_path)
    
    # Calculate overall sentiment
    overall = overall_sentiment(sentiments)
    print("\nOverall Sentiment:")
    print(f"Positive: {overall['positive']}, Negative: {overall['negative']}")
  """