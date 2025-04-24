const express = require('express')
const mongoose = require('mongoose')
const cors = require('cors')
const ramModel = require('./models/Ram')
require("dotenv").config({path: "./.env"})

const app = express();
const mongoURL = process.env.MONGO_URI;
const port = 8080;

app.use(cors());

mongoose.connect(mongoURL, {
        dbName: 'Verkkokauppa'
    }
    ).then(() =>{
        console.log("Connection successful.")
        app.listen(port, () =>{
            console.log("Server is running on port", port);
    });
}).catch((error) => console.log(error));

app.get("/ram", async(req, res) => {
    const ramData = await ramModel.find({});
    res.json(ramData);
})

app.get("/api", (req, res) =>{
    res.json({ trees:["oak", "spruce", "birch"] });
});