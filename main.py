
from flask import Flask, jsonify
import requests
import urllib.parse
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

# 🔐 Genius API Access Token
GENIUS_ACCESS_TOKEN = "2yHuhzVQAmuuHKKcJekeM3wXiBLQzt8GDqWVodgzq7slXnwZSZqLqXnhwVcjIwn9"

# 🔍 Search Genius for lyrics page
def search_genius_lyrics(query):
    url = "https://api.genius.com/search"
    headers = {"Authorization": f"Bearer {GENIUS_ACCESS_TOKEN}"}
    params = {"q": query}
    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        data = response.json()
        hits = data.get("response", {}).get("hits", [])
        if hits:
            top = hits[0]["result"]
            return {
                "title": top.get("title"),
                "artist": top.get("primary_artist", {}).get("name"),
                "lyrics_url": top.get("url"),
                "thumbnail": top.get("song_art_image_thumbnail_url")
            }
    except Exception as e:
        print(f"[Genius API Error] {e}")
    return None

# 🧠 Scrape lyrics from Genius page
def scrape_lyrics_from_url(lyrics_url):
    try:
        page = requests.get(lyrics_url, timeout=5)
        soup = BeautifulSoup(page.text, "html.parser")
        lyrics_divs = soup.find_all("div", class_="Lyrics__Container")
        if not lyrics_divs:
            lyrics_divs = soup.find_all("div", class_="lyrics")
        lyrics = "\n".join([div.get_text(separator="\n").strip() for div in lyrics_divs])
        return lyrics if lyrics else None
    except Exception as e:
        print(f"[Scrape Error] {e}")
        return None

# 🎤 Lyrics route
@app.route('/lyrics/<path:query>')
def lyrics(query):
    decoded_query = urllib.parse.unquote(query)
    result = search_genius_lyrics(decoded_query)
    if not result:
        return jsonify({
            "title": decoded_query,
            "error": "Lyrics not found",
            "creator": "Broken Vzn"
        }), 404

    lyrics_text = scrape_lyrics_from_url(result["lyrics_url"])
    if not lyrics_text:
        return jsonify({
            "title": result["title"],
            "artist": result["artist"],
            "lyrics_url": result["lyrics_url"],
            "thumbnail": result["thumbnail"],
            "error": "Lyrics could not be scraped",
            "creator": "Broken Vzn"
        }), 500

    return jsonify({
        "title": result["title"],
        "artist": result["artist"],
        "lyrics_url": result["lyrics_url"],
        "thumbnail": result["thumbnail"],
        "lyrics": lyrics_text,
        "creator": "Broken Vzn"
    })

# 🏠 Optional root route
@app.route('/')
def home():
    return jsonify({"message": "Genius Lyrics API is running", "creator": "Broken Vzn"})

# 🚀 Render-compatible port binding
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True, threaded=True)