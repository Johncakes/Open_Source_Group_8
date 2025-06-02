import json
import os
from datetime import datetime

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

from movie.models import Genre, Movie, MovieCast, MovieCrew  # noqa

INPUT_FILE = "movie_details.json"


def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except Exception:
        return None


def import_casts(movie, casts):
    MovieCast.objects.filter(movie=movie).delete()
    for cast in casts:
        MovieCast.objects.create(
            movie=movie,
            name=cast.get("name", ""),
            character=cast.get("character", ""),
            profile_path=cast.get("profile_path"),
        )


def import_crews(movie, crews):
    MovieCrew.objects.filter(movie=movie).delete()
    for crew in crews:
        MovieCrew.objects.create(
            movie=movie,
            name=crew.get("name", ""),
            job=crew.get("job", ""),
            profile_path=crew.get("profile_path"),
        )


def import_movie_record(record):
    movie_data = record["movie"]
    credits = record["credits"]

    defaults = {
        "title": movie_data.get("title", ""),
        "original_title": movie_data.get("original_title", ""),
        "overview": movie_data.get("overview", ""),
        "poster_path": movie_data.get("poster_path"),
        "backdrop_path": movie_data.get("backdrop_path"),
        "release_date": parse_date(movie_data.get("release_date")),
        "runtime": movie_data.get("runtime"),
        "popularity": movie_data.get("popularity", 0),
        "origin_country": movie_data.get("origin_country", ""),
        "production_company": movie_data.get("production_company", ""),
    }

    movie, created = Movie.objects.update_or_create(
        id=movie_data["id"],
        defaults=defaults,
    )

    genre_ids = movie_data.get("genres", [])
    movie.genres.set(Genre.objects.filter(id__in=genre_ids))

    import_casts(movie, credits.get("casts", []))
    import_crews(movie, credits.get("crews", []))

    print(f"{'🆕 Created' if created else '🔁 Updated'}: {movie.title}")


def main():
    print("🎬 Importing from movie_details.json...")

    with open(INPUT_FILE, encoding="utf-8") as f:
        records = json.load(f)

    for record in records:
        import_movie_record(record)

    print(f"\n✅ Done. Imported {len(records)} movies.")


if __name__ == "__main__":
    main()
