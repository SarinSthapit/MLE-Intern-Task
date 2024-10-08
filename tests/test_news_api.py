import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from data_gathering.news_api import extract_hot_topics, extract_keywords, fetch_news, get_news_topics

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

    def test_extract_hot_topics(self):
        articles = [
            {'title': 'Climate Change Effects', 'description': 'Discussing climate change.'},
            {'title': 'Election Reform Needed', 'description': 'People want election reform.'},
            {'title': 'Healthcare Policy Updates', 'description': 'Updates on healthcare policy.'}
        ]
        result = extract_hot_topics(articles)
        expected_topics = ['climate', 'change', 'election', 'reform', 'healthcare']
        self.assertTrue(set(expected_topics).issuperset(set(result)))

    @patch('data_gathering.news_api.fetch_news')
    def test_get_news_topics(self, mock_fetch_news):
        mock_fetch_news.return_value = [
            {'title': 'Climate Change Effects', 'description': 'Discussion on climate.'},
            {'title': 'Healthcare Policies', 'description': 'Healthcare is important.'},
        ]
        city = "Kathmandu"
        hot_topics = get_news_topics(city)

        expected_topics = ['climate', 'change', 'discussion', 'effects', 'healthcare']
        self.assertEqual(sorted(hot_topics), sorted(expected_topics))

if __name__ == '__main__':
    unittest.main()
