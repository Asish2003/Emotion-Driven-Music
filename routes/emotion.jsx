const express = require("express");
const router = express.Router();
const { getSongsForEmotion } = require("../services/spotify.jsx");

router.post("/", async (req, res) => {
    const { emotion } = req.body;
    try {
      const songs = await getSongsForEmotion(emotion);
      res.json(songs);
    } catch (err) {
      console.error("Backend Error:", err);
      res.status(500).json({ error: "Failed to fetch songs" });
    }
  });
  

module.exports = router;
