import requests
import json
from sqlalchemy.orm import Session, sessionmaker
from models import Review, Movie, engine
from celery_config import celery_app

access_token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0MDM4ODMxZTE1ODM1YjlkMDY1ZDgwZDg2NTAwN2ZkYiIsInN1YiI6IjY0YzRlZDY4OWI2ZTQ3MDBmZjM2MzY1MCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.QwEnsOxBKelt3Dd6OhyQok7G5zR9DG_Iwxr3e-YY0WE"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer {token}".format(token=access_token)}


def get_all_movies():
    url = "https://api.themoviedb.org/3/movie/popular"
    response = requests.get(url, headers=headers)
    response = json.loads(response.text)
    # print(response)
    if 'results' in response:
        for movies in response['results']:
            yield movies


def get_movie_reviews(id: int):
    reviews = {}
    all_reviews = []
    url = "https://api.themoviedb.org/3/movie/{movie_id}/reviews".format(movie_id=id)
    response = requests.get(url, headers=headers)
    response = json.loads(response.text)
    reviews['movie_id'] = id
    if response['results']:
        for res in response['results']:
            if 'author' and 'content' in res:
                reviews['author'] = res['author']
                reviews['review'] = res['content']
                reviews = {}
                reviews['movie_id'] = id
            all_reviews.append(reviews)

    save_data(all_reviews, 'reviews')


def save_data(data, table):
    Session = sessionmaker(bind=engine)
    session = Session()

    if table == 'movies':
        movie = Movie(
            id=data['movie_id'],
            title=data['title'],
            release_date=data['release_date'],
            original_language=data['original_language']
        )
        session.add(movie)

    elif table == 'reviews':
        for review_data in data:
            if 'author' and 'review' in review_data:
                review = Review(
                    author=review_data['author'],
                    review=review_data['review'],
                    movie_id=review_data['movie_id']
                )
                session.add(review)

    session.commit()
    session.close()


@celery_app.task
def get_movies_data():
    movies_data = {}
    movies = get_all_movies()
    for movie in movies:
        movies_data['movie_id'] = movie['id']
        movies_data['title'] = movie['title']
        movies_data['release_date'] = movie['release_date']
        movies_data['original_language'] = movie['original_language']
        save_data(movies_data, 'movies')
        get_movie_reviews(movie['id'])
