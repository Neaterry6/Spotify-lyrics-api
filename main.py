from fastapi import FastAPI, Query
from spotify_lyrics_scraper import getToken, getLyrics, spotifyDict

app = FastAPI()

# Paste your actual sp_dc cookie value here
SP_DC = "AQANYSRZpndtOAAr007tzf1CW2FGA40WYp96t1UHChgGCWVxfdmcz9Q7Vmkb4JZvu8GzbAWdk5W6J-0SKE4_40nXo5XHprBNVaoSsdROJYsFRyuTeazmVKGL7TMK4TKed8N1A7NiGTi1kwHeb1yXH9YxTyQGtEdz71147KxIGBdyc0-o9HaiRholSHzlEWVW2Aai4oKrnLK0ruYfu4YvlucJ1h_oGw-Jn3KDbCXNvkmOqIahdrU76BCNHN2msYeaS8pKVE-LvMTtkfg"

@app.get("/")
def home():
    return {
        "message": "Welcome to Broken Vzn's Lyrics API",
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
            return {
                "title": lyrics_data.songName,
                "lyrics": full_lyrics,
                "creator": "Broken Vzn"
            }
        else:
            return {
                "title": query,
                "lyrics": None,
                "creator": "Broken Vzn",
                "error": str(lyrics_data)
            }
    except Exception as e:
        return {
            "title": query,
            "lyrics": None,
            "creator": "Broken Vzn",
            "error": str(e)
      }
