import os
import streamlit as st
import requests, base64
from PIL import Image
import numpy as np
import random

# ========================
# Spotify API Setup
# ========================
CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")

def get_spotify_token():
    """Get Spotify API token"""
    auth_url = "https://accounts.spotify.com/api/token"
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode("ascii")

    response = requests.post(
        auth_url,
        headers={"Authorization": f"Basic {auth_header}"},
        data={"grant_type": "client_credentials"}
    )
    return response.json().get("access_token")

def get_songs_from_spotify(query):
    """Search Spotify songs by emotion keyword"""
    token = get_spotify_token()
    url = f"https://api.spotify.com/v1/search?q={query}&type=track&limit=5"
    response = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    results = response.json()
    
    songs = []
    if "tracks" in results:
        for item in results["tracks"]["items"]:
            songs.append({
                "name": item["name"],
                "artist": item["artists"][0]["name"],
                "url": item["external_urls"]["spotify"],
                "id": item["id"]
            })
    return songs

# ========================
# Placeholder Emotion Detector
# ========================
def detect_emotion(image):
    """Temporary emotion detector (random for now)"""
    emotions = ["Happy", "Sad", "Angry", "Surprise", "Neutral"]
    return random.choice(emotions)

# ========================
# Streamlit UI
# ========================
st.title("🎭 Emotion Driven Music 🎵")
st.write("Upload a photo → Detect emotion → Get Spotify music suggestions")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
camera_image = st.camera_input("Or take a photo with your camera")

final_image = None
if uploaded_file is not None:
    final_image = Image.open(uploaded_file).convert("RGB")
elif camera_image is not None:
    final_image = Image.open(camera_image).convert("RGB")

if final_image is not None:
    st.image(final_image, caption="Your Image", use_column_width=True)

    # Detect emotion
    emotion = detect_emotion(final_image)
    st.subheader(f"😊 Detected Emotion: {emotion}")

    # Get Spotify songs
    st.write("🎶 Suggested Songs:")
    songs = get_songs_from_spotify(emotion)
    if songs:
        for s in songs:
            st.markdown(f"- 🎵 [{s['name']} - {s['artist']}]({s['url']})")
            # Embed Spotify player
            st.markdown(f'<iframe src="https://open.spotify.com/embed/track/{s["id"]}" '
                        f'width="100%" height="80" frameborder="0" '
                        f'allowtransparency="true" allow="encrypted-media"></iframe>',
                        unsafe_allow_html=True)
    else:
        st.warning("No songs found. Try again!")
