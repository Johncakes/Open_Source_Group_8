import os

import requests


class TmdbClient:
    BASE_URL = "https://api.themoviedb.org/3"

    def __init__(self, token: str, language: str = "ko-KR"):
        self.token = token
        self.language = language
        self.headers = {"accept": "application/json", "Authorization": f"Bearer {self.token}"}

    def get(self, path: str, params: dict = None):
        url = f"{self.BASE_URL}{path}"

        if params is None:
            params = {}
        params.update(self.default_params)

        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()

        return response.json()

    def get_popular_movies(self, page: int = 1, region: str = "KR"):
        return self.get("/movie/popular", {"page": page, "region": region})

    def get_movie_details(self, movie_id: int):
        return self.get(f"/movie/{movie_id}")

    def get_movie_credits(self, movie_id: int):
        return self.get(f"/movie/{movie_id}/credits")

    @property
    def default_params(self):
        return {
            "language": self.language,
        }


tmdb_client = TmdbClient(token=os.getenv("TMDB_TOKEN"))
