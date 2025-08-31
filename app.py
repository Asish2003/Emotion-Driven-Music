import os
import requests, base64
import streamlit as st

# Load keys safely
CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")

# Function to fetch token
@st.cache_resource
def get_spotify_token():
    auth_url = "https://accounts.spotify.com/api/token"
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode("ascii")

    response = requests.post(auth_url,
                             headers={"Authorization": f"Basic {auth_header}"},
                             data={"grant_type": "client_credentials"})
    return response.json().get("access_token")
