from flask import Flask, render_template, request
import os
from src.data_gathering.actions_needed import analyze_gathered_action_info
from src.data_gathering.currentnews_api import get_currentnews_topics
from src.data_gathering.gnews_api import get_gnews_topics
from src.data_gathering.news_api import get_news_topics
from src.data_gathering.reddit_api import gather_all_discussions
from src.data_gathering.analysis import analyze_gathered_info, plot_sentiments

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    analysis_results = None
    hot_topics = None
    summaries = None
    sentiments = None
    overall = None

    if request.method == 'POST':
        city = request.form['city']
        
        selected_api = request.form['api']

        if selected_api == 'newsapi':
            hot_topics = get_news_topics(city, n=2, num_topics=5)  # Use your existing NewsAPI function
        elif selected_api == 'gnewsapi':
            hot_topics = get_gnews_topics(city, n=2, num_topics=5) 
        elif selected_api == 'currentnewsapi':
            hot_topics = get_currentnews_topics(city, n=2, num_topics=5) 
        # Task 2: Gather Reddit discussions based on the hot topics
        gather_all_discussions(hot_topics, limit=5)

        # Task 3: Perform analysis (summarization and sentiment analysis) on gathered discussions
        summaries, sentiments= analyze_gathered_info()  # Update this line
        actions = analyze_gathered_action_info()
        
        # Calculate overall sentiment
        overall = {
            'positive': sum(1 for sentiment_list in sentiments.values() for sentiment in sentiment_list if sentiment['label'] == 'POSITIVE'),
            'negative': sum(1 for sentiment_list in sentiments.values() for sentiment in sentiment_list if sentiment['label'] == 'NEGATIVE')
        }

        # Prepare analysis results for display
        analysis_results = {
            'summaries': summaries,
            'sentiments': sentiments,
            'overall': overall,
          # Add actionable needs to results
        }

        # Save the sentiment analysis plot to the static folder
        static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
        plot_path = os.path.join(static_folder, 'sentiment_analysis.png')
        plot_sentiments(sentiments, plot_path)

    return render_template("index.html", analysis_results=analysis_results, hot_topics=hot_topics)

if __name__ == "__main__":
    app.run(debug=True)
