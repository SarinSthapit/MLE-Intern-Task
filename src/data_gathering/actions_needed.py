import warnings 
import json
import os
from dotenv import load_dotenv
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer, pipeline
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore", category=FutureWarning, message="resume_download is deprecated")

from .news_api import get_news_topics
from .reddit_api import gather_all_discussions

load_dotenv()

t5_model = T5ForConditionalGeneration.from_pretrained('t5-small', force_download=False)
t5_tokenizer = T5Tokenizer.from_pretrained('t5-small', legacy=False)

sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def summarize_text_t5(text):
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
    
    refined_summary = refine_summary(summary)
    
    return refined_summary.replace(":", "").strip()

def refine_summary(summary):

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

    with open(json_path, 'r') as f:
        return json.load(f)

def summarize_discussions(discussions):

    summaries = {}
    max_input_length = 512

    for topic, discussion_list in discussions.items():
        full_text = " ".join([comment['body'] for discussion in discussion_list for comment in discussion['comments']])
        chunks = [full_text[i:i + max_input_length] for i in range(0, len(full_text), max_input_length)]
        combined_summary = summarize_text_t5(" ".join(chunks))
        summaries[topic] = combined_summary.strip()

    return summaries






def analyze_gathered_action_info():
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../data/discussions.json')
    discussions = load_discussions(json_path)

    summaries = summarize_discussions(discussions)

    return summaries
