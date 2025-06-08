import express from "express";
const router = express.Router();
import { getSongsForEmotion } from "../services/spotify.js";

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
  

export default router ;
