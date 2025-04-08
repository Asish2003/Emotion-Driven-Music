import express from "express";
import { getSongsForEmotion } from "../services/spotify.js";
const router = express.Router();

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
  

export { router as emotionRoute };
