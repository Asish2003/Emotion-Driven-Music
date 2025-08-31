import streamlit as st
import numpy as np
from PIL import Image
import os
import requests
import base64

# ----------------------------
# Dummy emotion classifier (replace with ML model)
# ----------------------------
def predict_emotion(image):
    emotions = ["Happy", "Sad", "Angry", "Surprised", "Neutral"]
    return np.random.choice(emotions)

# ----------------------------
# Spotify Authentication (Client Credentials Flow)
# ----------------------------
def get_spotify_token():
    client_id = os.environ.get("SPOTIFY_CLIENT_ID")
    client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")
    
    auth_url = "https://accounts.spotify.com/api/token"
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode("ascii")
    
    response = requests.post(auth_url, 
                             headers={"Authorization": f"Basic {auth_header}"},
                             data={"grant_type": "client_credentials"})
    
    return response.json().get("access_token")

def search_spotify(track_query, token):
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": track_query, "type": "track", "limit": 1}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    if "tracks" in data and len(data["tracks"]["items"]) > 0:
        return data["tracks"]["items"][0]["external_urls"]["spotify"]
    return None

# ----------------------------
# Map emotions to keywords
# ----------------------------
emotion_keywords = {
    "Happy": "feel good upbeat",
    "Sad": "sad emotional",
    "Angry": "rock metal angry",
    "Surprised": "party dance surprise",
    "Neutral": "chill lofi relax"
}

# ----------------------------
# Streamlit UI
# ----------------------------
st.set_page_config(page_title="Emotion Driven Music", page_icon="🎶")

st.title("🎶 Emotion-Driven Music Player with Spotify")
st.write("Upload an image or take a photo to detect your emotion and suggest Spotify tracks!")

# Upload or take photo
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
camera_image = st.camera_input("Or take a photo")

img = None
if uploaded_file:
    img = Image.open(uploaded_file)
elif camera_image:
    img = Image.open(camera_image)

if img is not None:
    st.image(img, caption="Uploaded Image", use_column_width=True)

    # Predict emotion
    emotion = predict_emotion(img)
    st.subheader(f"Detected Emotion: {emotion}")

    # Get Spotify track
    token = get_spotify_token()
    query = emotion_keywords.get(emotion, "chill")
    track_url = search_spotify(query, token)

    if track_url:
        st.markdown(f"🎧 Here's a Spotify suggestion for your mood: [Open in Spotify]({track_url})")
    else:
        st.warning("No tracks found. Try again.")
