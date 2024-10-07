import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.data_gathering.display import display_hot_topics
from unittest.mock import patch


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.data_gathering.display import display_hot_topics

class TestDisplay(unittest.TestCase):
    
    @patch('src.data_gathering.display.get_news')
    @patch('src.data_gathering.display.extract_hot_topics')
    def test_display_hot_topics(self, mock_extract_hot_topics, mock_get_news):
        
        mock_get_news.return_value = {'articles': [{"title": "Test Topic"}]}
        mock_extract_hot_topics.return_value = ["Test Topic"]

        display_hot_topics("Kathmandu")

        mock_get_news.assert_called_once_with("Kathmandu")
        print(f"Test passed: 'get_news' was called once with 'Kathmandu'.")

        mock_extract_hot_topics.assert_called_once()
        print("Test passed: 'extract_hot_topics' was called once.")

if __name__ == '__main__':
    unittest.main()

