from fastapi import FastAPI, Query
from lyrics_fetcher import fetch_lyrics

app = FastAPI()

@app.get("/search")
def get_lyrics(query: str = Query(..., description="e.g. 'lyrics of baby girl by joeboy'")):
    if "lyrics of" in query.lower():
        parts = query.lower().replace("lyrics of", "").strip().split("by")
        if len(parts) == 2:
            title = parts[0].strip()
            artist = parts[1].strip()
            lyrics = fetch_lyrics(title, artist)
            return {
                "title": title,
                "artist": artist,
                "lyrics": lyrics,
                "creator": "broken vzn"
            }
    return {"error": "Invalid query format. Use 'lyrics of <song> by <artist>'"}
