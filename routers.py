from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.responses import Response
from reviews import get_movies_data
from sentiment_analysis import analyze_sentiment, text_cleaning
from celery import chain
from celery.result import AsyncResult
from models import engine
from sqlalchemy import text
import json

app = FastAPI()


@app.post('/movies')
def movies():
    get_movies_data.apply_async()
    return {'message': 'Fetching Movie Data'}


def fetch_reviews(movie_id):
    # query = text("SELECT * FROM Reviews WHERE some_column = :value")

    query = text(
        "SELECT review FROM review_table "
        "INNER JOIN movie_table ON review_table.movie_id = movie_table.id "
        "WHERE review_table.movie_id = :movie_id"
    )
    params = {'movie_id': movie_id}

    with engine.connect() as connection:
        result = connection.execute(query, **params)
        rows = result.fetchall()

    for row in rows:
        review_text = row[0]
        review_text = review_text.replace('\r\n', '\n')
        yield review_text


@app.post('/analyze')
def analyze_sentiments(movie_id: int):
    all_movie_reviews = list(fetch_reviews(movie_id))

    chain(text_cleaning.s(json.dumps(all_movie_reviews)), analyze_sentiment.s()).apply_async()

    return {'message': 'calculating sentiments'}


@app.get('/get_sentiments')
def sentiments(celery_task_id: str):
    celery_task_id = AsyncResult(celery_task_id)
    if celery_task_id.status == 'SUCCESS':
        pass
    else:
        return {"message": "Calculating Sentiments"}
