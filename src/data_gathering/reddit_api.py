import json
import praw
import os
import sys
from dotenv import load_dotenv

from .news_api import get_news_topics

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)


def gather_discussions_for_topic(topic, limit=5):
    discussions = []
    for submission in reddit.subreddit("all").search(topic, limit=limit):
        discussion = {
            "title": submission.title,
            "score": submission.score,
            "num_comments": submission.num_comments,
            "comments": []
        }

        submission.comments.replace_more(limit=0)
        for idx, comment in enumerate(submission.comments.list()):
            if idx >= 25:
                break
            if len(comment.body.split()) >= 15:
                discussion["comments"].append({
                    "body": comment.body,
                    "score": comment.score
                })

        discussions.append(discussion)

    return discussions


def gather_all_discussions(topics, limit=5):
    all_discussions = {}
    for topic in topics:
        print(f"Gathering discussions for topic: {topic}")
        all_discussions[topic] = gather_discussions_for_topic(topic, limit)

    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../data/discussions.json')
    
    with open(json_path, 'w') as f:
        json.dump(all_discussions, f, indent=4)
    print(f"Discussions gathered for {len(topics)} topics.")
