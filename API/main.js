const express = require("express");
const mongoose = require("mongoose");
const bodyParser = require('body-parser');
const config = require("./config.json")
const app = express();

//Connect to db
mongoose.connect(config.mongoUri, {useNewUrlParser: true}, () => console.log("Connected to mongodb"))

//Import routes
const userRoute = require("./routes/userRoute");

app.use(bodyParser.json())
app.use("/api/", userRoute);
app.listen(2345, () => console.log("Cipher Backend is up"))