import json
import time

from movie.clients.tmdb import tmdb_client


OUTPUT_FILE = "popular_movies.json"
MAX_PAGES = 5


def main():
    movies = []

    for page in range(1, MAX_PAGES + 1):
        print(f"📥 Fetching popular movies - page {page}")
        try:
            data = tmdb_client.get_popular_movies(page=page)
            movies.extend(data.get("results", []))
        except Exception as e:
            print(f"❌ Error on page {page}: {e}")
            break
        time.sleep(0.2)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(movies, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Done. {len(movies)} movies saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
