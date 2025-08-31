import os, base64, requests
import streamlit as st

CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")

@st.cache_resource
def get_spotify_token():
    """Fetch client-credentials token (cached so it is reused)."""
    if not CLIENT_ID or not CLIENT_SECRET:
        raise RuntimeError("Spotify credentials not found in environment variables.")
    auth_url = "https://accounts.spotify.com/api/token"
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode("ascii")
    resp = requests.post(auth_url,
                         headers={"Authorization": f"Basic {auth_header}"},
                         data={"grant_type": "client_credentials"})
    resp.raise_for_status()
    return resp.json()["access_token"]

def get_songs_from_spotify(query, limit=5):
    token = get_spotify_token()
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": query, "type": "track", "limit": limit}
    r = requests.get(url, headers=headers, params=params)
    r.raise_for_status()
    data = r.json()
    items = data.get("tracks", {}).get("items", [])
    songs = [{"name": i["name"], "artist": i["artists"][0]["name"], "url": i["external_urls"]["spotify"]} for i in items]
    return songs
