from fastapi import FastAPI, Query
from spotify_lyrics_scraper import getToken, getLyrics, spotifyDict

app = FastAPI()

# 🎟️ Your Spotify sp_dc cookie — required for lyrics access
SP_DC = (
    "AQAAkbYKb2gSiNk8Rb70_bpUnjpzPMDDZriDa48pZr0-aJ0GGBfeMEXkZl_QvKVSd7s62tvXBlOFtQV4ox_-RvH4qdgO3A98aOqiFRQFd9feTsLFOm7sLVxNVu1XFCUEJE50YZIwzi64WhFInlUx_aLLYdPhbTGiIBvlzZRRZKWwNocxaIkmsUheO8k2cnr3ia60XwxcXxeXM6ynQErjvVjD7bWrSO-UQ0yHqtAjZsLqVifHCIVOrd-zNwrqtW6OBGlktB1ZeNi9dg"
)

@app.get("/")
def home():
    return {
        "message": "🎶 Welcome to Broken Vzn's Lyrics API",
        "usage": "/lyrics?query=song+name+by+artist",
        "creator": "Broken Vzn"
    }

@app.get("/lyrics")
def get_lyrics(query: str = Query(..., description="Song name and artist")):
    try:
        token = getToken(SP_DC)
        lyrics_data = getLyrics(token, songName=query)

        if isinstance(lyrics_data, spotifyDict):
            full_lyrics = lyrics_data.formatLyrics(mode=0)  # plain text
            thumbnail = lyrics_data.get("image") or None

            return {
                "title": lyrics_data.songName,
                "lyrics": full_lyrics,
                "thumbnail": thumbnail,
                "creator": "Broken Vzn"
            }

        return {
            "title": query,
            "lyrics": None,
            "thumbnail": None,
            "creator": "Broken Vzn",
            "error": str(lyrics_data)
        }

    except Exception as e:
        return {
            "title": query,
            "lyrics": None,
            "thumbnail": None,
            "creator": "Broken Vzn",
            "error": str(e)
        }