from flask import Flask, render_template, request
import os
from src.data_gathering.actions_needed import analyze_gathered_action_info
from src.data_gathering.gnews_api import get_gnews_topics
from src.data_gathering.news_api import get_news_topics
from src.data_gathering.reddit_api import gather_all_discussions
from src.data_gathering.analysis import analyze_gathered_info, plot_sentiments
import warnings 

warnings.filterwarnings("ignore", category=FutureWarning, message="resume_download is deprecated")
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", message="Special tokens have been added in the vocabulary.*")

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    analysis_results = None
    hot_topics = None
    summaries = None
    sentiments = None
    overall = None
    actions = None

    if request.method == 'POST':
        city = request.form['city']
        selected_api = request.form['api']

        if selected_api == 'newsapi':
            hot_topics = get_news_topics(city, n=2, num_topics=5) 
        elif selected_api == 'gnewsapi':
            hot_topics = get_gnews_topics(city, n=2, num_topics=5) 

        gather_all_discussions(hot_topics, limit=5)

        summaries, sentiments = analyze_gathered_info() 
        actions, actionsentiments = analyze_gathered_action_info()
        
        print("Actions Needed:")
        for topic, action in actions.items():
            print(f"{topic}: {action}")
        
        
        overall = {
            'positive': sum(1 for sentiment_list in sentiments.values() for sentiment in sentiment_list if sentiment['label'] == 'POSITIVE'),
            'negative': sum(1 for sentiment_list in sentiments.values() for sentiment in sentiment_list if sentiment['label'] == 'NEGATIVE')
        }

        analysis_results = {
            'summaries': summaries,
            'sentiments': sentiments,
            'overall': overall,
            'actions': actions
        }

        static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
        plot_path = os.path.join(static_folder, 'sentiment_analysis.png')
        plot_sentiments(sentiments, plot_path)

    return render_template("index.html", analysis_results=analysis_results, hot_topics=hot_topics)


if __name__ == "__main__":
    app.run(debug=True)
