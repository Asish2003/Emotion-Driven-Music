import os
import cv2
import numpy as np
import streamlit as st
import requests, base64
from PIL import Image
from tensorflow.keras.models import load_model

# ========================
# Spotify API Setup
# ========================
CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")

@st.cache_resource
def get_spotify_token():
    """Get Spotify API token"""
    auth_url = "https://accounts.spotify.com/api/token"
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode("ascii")

    response = requests.post(auth_url,
                             headers={"Authorization": f"Basic {auth_header}"},
                             data={"grant_type": "client_credentials"})
    return response.json().get("access_token")

def get_songs_from_spotify(query):
    """Search Spotify songs by emotion"""
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
                "url": item["external_urls"]["spotify"]
            })
    return songs

# ========================
# Load Emotion Model
# ========================
@st.cache_resource
def load_emotion_model():
    return load_model("emotion_model.h5")  # make sure this file is in repo

emotion_model = load_emotion_model()
emotion_labels = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]

# ========================
# Streamlit UI
# ========================
st.title("🎭 Emotion Driven Music 🎵")
st.write("Upload a photo → Detect emotion → Get Spotify music suggestions")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Convert to OpenCV format
    img_array = np.array(image)
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    resized = cv2.resize(gray, (48, 48))
    normalized = resized / 255.0
    reshaped = np.reshape(normalized, (1, 48, 48, 1))

    # Predict emotion
    prediction = emotion_model.predict(reshaped)
    emotion = emotion_labels[np.argmax(prediction)]
    
    st.subheader(f"😊 Detected Emotion: {emotion}")

    # Get Spotify songs
    st.write("🎶 Suggested Songs:")
    songs = get_songs_from_spotify(emotion)
    if songs:
        for s in songs:
            st.markdown(f"- 🎵 [{s['name']} - {s['artist']}]({s['url']})")
    else:
        st.warning("No songs found. Try again!")
