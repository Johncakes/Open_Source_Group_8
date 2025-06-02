import json
import os
import time

from movie.clients.tmdb import tmdb_client

POPULAR_FILE = "popular_movies.json"
DETAIL_FILE = "movie_details.json"


def load_existing_movie_ids():
    if os.path.exists(DETAIL_FILE):
        with open(DETAIL_FILE, encoding="utf-8") as f:
            details = json.load(f)
            movie_ids = {detail["movie"]["id"] for detail in details}
            return details, movie_ids

    return [], set()


def extract_movie_data(movie_json):
    production_companies = movie_json.get("production_companies", [])
    production_company_name = (
        production_companies[0].get("name", "") if production_companies else ""
    )

    origin_country = movie_json.get("origin_country")
    origin_country_code = origin_country[0] if origin_country else ""

    return {
        "id": movie_json["id"],
        "title": movie_json.get("title", ""),
        "original_title": movie_json.get("original_title", ""),
        "overview": movie_json.get("overview", ""),
        "poster_path": movie_json.get("poster_path"),
        "backdrop_path": movie_json.get("backdrop_path"),
        "release_date": movie_json.get("release_date"),
        "runtime": movie_json.get("runtime"),
        "popularity": movie_json.get("popularity", 0),
        "origin_country": origin_country_code,
        "production_company": production_company_name,
        "genres": [genre["id"] for genre in movie_json.get("genres", [])],
    }


def extract_casts(credits_json):
    return [
        {
            "name": cast.get("name", ""),
            "character": cast.get("character", ""),
            "profile_path": cast.get("profile_path"),
        }
        for cast in credits_json.get("cast", [])[:5]
    ]


def extract_crews(credits_json):
    return [
        {
            "name": crew.get("name", ""),
            "job": crew.get("job", ""),
            "profile_path": crew.get("profile_path"),
        }
        for crew in credits_json.get("crew", [])[:3]
    ]


def main():
    existing_data, existing_ids = load_existing_movie_ids()

    with open(POPULAR_FILE, encoding="utf-8") as f:
        popular_movies = json.load(f)

    items = []

    for movie in popular_movies:
        movie_id = movie.get("id")
        if movie_id in existing_ids:
            continue

        print(f"🔍 Fetching details for ID {movie_id}")
        try:
            movie_json = tmdb_client.get_movie_details(movie_id)
            credits_json = tmdb_client.get_movie_credits(movie_id)

            item = {
                "movie": extract_movie_data(movie_json),
                "credits": {
                    "movie_id": movie_id,
                    "casts": extract_casts(credits_json),
                    "crews": extract_crews(credits_json),
                },
            }

            items.append(item)
            time.sleep(0.25)

        except Exception as e:
            print(f"❌ Failed to fetch {movie_id}: {e}")

    # append + save
    full_data = existing_data + items

    with open(DETAIL_FILE, "w", encoding="utf-8") as f:
        json.dump(full_data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Done. {len(items)} new movies added.")


if __name__ == "__main__":
    main()
