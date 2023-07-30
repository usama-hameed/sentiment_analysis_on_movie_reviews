from fastapi.testclient import TestClient
from routers import app
from unittest.mock import patch
from celery_config import celery_app


def test_movies_route():
    client = TestClient(app)

    with patch('reviews.get_movies_data.apply_async') as mock_get_movies_data:
        response = client.post('/movies')

        assert response.status_code == 200
        assert response.json() == {'message': 'Fetching Movie Data'}
        mock_get_movies_data.assert_called_once()


def test_analyze_route():
    client = TestClient(app)

    with patch('sentiment_analysis.text_cleaning.apply_async') as mock_text_cleaning:
        with patch('sentiment_analysis.analyze_sentiment.apply_async') as mock_analyze_sentiment:
            response = client.post(f'/analyze?movie_id={298618}')

        assert response.status_code == 200
        assert response.json() == {'message': 'calculating sentiments'}
        mock_text_cleaning.assert_called_once()
        mock_analyze_sentiment.assert_called_once()
