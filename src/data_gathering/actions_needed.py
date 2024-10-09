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
        max_length=200,
        min_length=10,
        length_penalty=2.0,
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
        max_length=200,
        min_length=10,
        length_penalty=2.0,
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






def analyze_gathered_action_info():
    """
    Load the discussions from a JSON file, summarize them, analyze their sentiment,
    and extract actionable needs.
    """
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../data/discussions.json')
    discussions = load_discussions(json_path)

    summaries = summarize_discussions(discussions)

    return summaries

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