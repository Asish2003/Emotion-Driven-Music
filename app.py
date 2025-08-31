import streamlit as st
import numpy as np
from PIL import Image
import os

# ----------------------------
# Dummy emotion classifier (replace with real ML model)
# ----------------------------
def predict_emotion(image):
    # TODO: Replace with actual model prediction
    emotions = ["Happy", "Sad", "Angry", "Surprised", "Neutral"]
    return np.random.choice(emotions)

# ----------------------------
# Emotion → Music mapping
# ----------------------------
emotion_music = {
    "Happy": "songs/happy_song.mp3",
    "Sad": "songs/sad_song.mp3",
    "Angry": "songs/angry_song.mp3",
    "Surprised": "songs/surprised_song.mp3",
    "Neutral": "songs/neutral_song.mp3",
}

# ----------------------------
# Streamlit UI
# ----------------------------
st.set_page_config(page_title="Emotion Driven Music", page_icon="🎶")

st.title("🎶 Emotion-Driven Music Player")
st.write("Upload an image or take a photo to detect your emotion and play music!")

# Upload option
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# Webcam option
camera_image = st.camera_input("Or take a photo")

# Process image
img = None
if uploaded_file is not None:
    img = Image.open(uploaded_file)
elif camera_image is not None:
    img = Image.open(camera_image)

if img is not None:
    st.image(img, caption="Uploaded Image", use_column_width=True)

    # Predict emotion
    emotion = predict_emotion(img)
    st.subheader(f"Detected Emotion: {emotion}")

    # Play music
    if emotion in emotion_music:
        music_path = emotion_music[emotion]
        if os.path.exists(music_path):
            st.audio(music_path, format="audio/mp3")
        else:
            st.warning(f"No song found for {emotion}. Please add an MP3 in 'songs/' folder.")
