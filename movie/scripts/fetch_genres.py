import json

from movie.clients.tmdb import tmdb_client

OUTPUT_FILE = "genres.json"


def main():
    print("📥 Fetching genres from TMDb...")
    try:
        data = tmdb_client.get("/genre/movie/list")
        genres = data.get("genres", [])

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(genres, f, ensure_ascii=False, indent=2)

        print(f"✅ Saved {len(genres)} genres to {OUTPUT_FILE}")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
