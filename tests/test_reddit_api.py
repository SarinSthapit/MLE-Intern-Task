import unittest
import sys
import os
from unittest.mock import patch, MagicMock
import json

from unittest.mock import patch

from src.data_gathering.reddit_api import gather_all_discussions, gather_discussions_for_topic

class TestRedditApiFunctions(unittest.TestCase):

    @patch('praw.Reddit')
    def test_gather_discussions_for_topic(self, mock_reddit):
        mock_submission_1 = MagicMock()
        mock_submission_1.title = "Test Submission 1"
        mock_submission_1.score = 100
        mock_submission_1.num_comments = 5

        mock_submission_2 = MagicMock()
        mock_submission_2.title = "Test Submission 2"
        mock_submission_2.score = 200
        mock_submission_2.num_comments = 10

        mock_comment_1 = MagicMock()
        mock_comment_1.body = "First comment"
        mock_comment_1.score = 10

        mock_reddit_instance = mock_reddit.return_value
        mock_reddit_instance.subreddit.return_value.search.return_value = [mock_submission_1, mock_submission_2]

        mock_submission_1.comments.replace_more.return_value = None
        mock_submission_1.comments.list.return_value = [mock_comment_1]

        mock_submission_2.comments.replace_more.return_value = None
        mock_submission_2.comments.list.return_value = [mock_comment_1]

        topic = "test topic"
        discussions = gather_discussions_for_topic(topic)

        self.assertEqual(len(discussions), 5) 


        @patch('src.data_gathering.reddit_api.gather_discussions_for_topic')
        @patch('builtins.open', new_callable=unittest.mock.mock_open)
        @patch('json.dump')
        def test_gather_all_discussions(self, mock_json_dump, mock_open, mock_gather_discussions):
            mock_gather_discussions.side_effect = lambda topic, limit: [
                {
                    "title": f"Test Submission {topic}",
                    "score": 100,
                    "num_comments": 5,
                    "comments": [
                        {"body": "First comment", "score": 10},
                        {"body": "Second comment", "score": 5}
                    ]
                }
            ]

            topics = ["topic1", "topic2"]
            gather_all_discussions(topics, limit=5)

            mock_gather_discussions.assert_any_call("topic1", limit=5)
            mock_gather_discussions.assert_any_call("topic2", limit=5)

            mock_open.assert_called_once_with(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../data/discussions.json'), 'w')
            mock_json_dump.assert_called_once()  

if __name__ == '__main__':
    unittest.main()
