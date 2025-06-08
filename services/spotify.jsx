const axios = require("axios");

const CLIENT_ID = "c01090b6625c4ccbb8a9d25d40fee4c2";
const CLIENT_SECRET = "1abbdc8239464f3e9372c98d587f28b8";

let accessToken = "";

async function getAccessToken() {
  const response = await axios.post(
    "https://accounts.spotify.com/api/token",
    new URLSearchParams({ grant_type: "client_credentials" }),
    {
      headers: {
        Authorization:
          "Basic " + Buffer.from(CLIENT_ID + ":" + CLIENT_SECRET).toString("base64"),
        "Content-Type": "application/x-www-form-urlencoded",
      },
    }
  );
  accessToken = response.data.access_token;
}

async function getSongsForEmotion(emotion) {
  if (!accessToken) await getAccessToken();

  const emotionToGenre = {
    happy: "happy",
    sad: "sad",
    angry: "rock",
    neutral: "chill",
    surprise: "party",
    fear: "ambient",
    disgust: "metal",
  };

  const genre = emotionToGenre[emotion.toLowerCase()] || "pop";

  const res = await axios.get(
    `https://api.spotify.com/v1/search?q=${genre}&type=track&limit=5`,
    {
      headers: { Authorization: `Bearer ${accessToken}` },
    }
  );

  return res.data.tracks.items.map((track) => ({
    name: track.name,
    artist: track.artists[0].name,
    url: track.external_urls.spotify,
  }));
}

module.exports = { getSongsForEmotion };
