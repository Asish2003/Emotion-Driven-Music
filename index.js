import express from "express";
import router from "./routes/emotion.js";

const app = express();

app.use(express.json());
app.use("/emotion", router);

app.listen(5000, () => {
  console.log("Backend running on http://localhost:5000");
});
