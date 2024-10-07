import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.data_gathering.news_api import get_news, extract_hot_topics

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.data_gathering.news_api import get_news, extract_hot_topics

class TestNewsAPI(unittest.TestCase):

    def test_get_news_valid_city(self):
        city = "Kathmandu"
        result = get_news(city)
        self.assertIn("articles", result)
        print(f"Test passed: News for city '{city}' contains 'articles'.")

    def test_extract_hot_topics(self):
        mock_news_data = {
            "articles": [
                {"title": "Topic 1"},
                {"title": "Topic 2"},
                {"title": "Topic 3"},
                {"title": "Topic 4"},
                {"title": "Topic 5"},
                {"title": "Topic 6"}
            ]
        }
        result = extract_hot_topics(mock_news_data)
        self.assertEqual(len(result), 5)
        print(f"Test passed: Extracted exactly 5 hot topics.")

if __name__ == '__main__':
    unittest.main()
