const express = require("express");
const emotionRoute = require("./routes/emotion.jsx");
const app = express();

app.use(express.json());
app.use("/emotion", emotionRoute);

app.listen(5000, () => {
  console.log("Backend running on http://localhost:5000");
});
