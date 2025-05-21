import json
import os

import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

from movie.models import Genre


INPUT_FILE = "genres.json"


def main():
    print("📦 Bulk importing genres from genres.json...")

    try:
        with open(INPUT_FILE, encoding="utf-8") as f:
            genre_data = json.load(f)

        genres = [Genre(id=genre["id"], name=genre["name"]) for genre in genre_data]

        Genre.objects.bulk_create(genres, ignore_conflicts=True)

        print(f"✅ Done. {len(genres)} genres attempted to insert.")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
