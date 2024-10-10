import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from data_gathering.gnews_api import extract_keywords, fetch_news

class TestNewsApiFunctions(unittest.TestCase):

    def test_extract_keywords(self):
        content = "This is a test to extract keywords from this content."
        expected_keywords = ['extract', 'keywords', 'content', 'test']
        result = extract_keywords(content)
        self.assertEqual(sorted(result), sorted(expected_keywords))


    @patch('data_gathering.news_api.requests.get')
    def test_fetch_news_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'articles': [
                {'title': 'Article 1', 'description': 'Description 1'},
                {'title': 'Article 2', 'description': 'Description 2'},
            ]
        }
        mock_get.return_value = mock_response

        city = "Kathmandu"
        articles = fetch_news(city)

        self.assertEqual(len(articles), 2)
        self.assertEqual(articles[0]['title'], 'Article 1')


    @patch('data_gathering.news_api.requests.get')
    def test_fetch_news_failure(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        city = "Kathmandu"
        articles = fetch_news(city)

        self.assertEqual(articles, [])


if __name__ == '__main__':
    unittest.main()
