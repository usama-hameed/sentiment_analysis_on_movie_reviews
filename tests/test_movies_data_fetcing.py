from reviews import get_movie_reviews, get_all_movies, headers
import requests
import json


def test_get_all_movies():
    url = "https://api.themoviedb.org/3/movie/popular"
    response = requests.get(url, headers=headers)

    assert response.status_code == 200

    movies = get_all_movies()

    for movie in movies:
        if 'results' in movie:
            assert type(movie['results']) == list


def test_get_movies_reviews():
    count = 0
    url = "https://api.themoviedb.org/3/movie/{movie_id}/reviews".format(movie_id=298618)
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    if json.loads(response.text)['results']:
        for data in json.loads(response.text)['results']:
            if 'author' and 'content' in data:
                count += 1
    assert count == 7


