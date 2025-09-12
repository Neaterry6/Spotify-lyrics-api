import subprocess

def fetch_lyrics(title: str, artist: str) -> str:
    try:
        result = subprocess.run(
            ["node", "lyrics.js", title, artist],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error fetching lyrics: {str(e)}"
