const express = require('express')
const mongoose = require('mongoose')
require("dotenv").config({path: "./.env"})
const ramModel = require('./models/Ram')
const { spawn } = require('child_process')
const cors = require("cors")

const app = express()
app.use(cors())
const mongoURL = process.env.MONGO_URI;
const port = 8080;

const runBot = async (script, args) => {
    const arguments = args.map(arg => args.toString());
    const py = spawn("python", [script, ...arguments]);
    const result = await new Promise((resolved, reject) =>{
        let output;

        py.stdout.on('data', (data) => {
            let buf = Buffer.from(data);
            output = buf.toString('latin1');
        });
        py.stderr.on("data", (data) => {
            console.error('[Python] Error: ' + data)
            reject('Error ${chat}')
        });
        py.on("exit", (code) => {
            //console.log($(code))
            resolved(output);
        });
    });
    return result;
}

app.use(express.json());

//Database connection
mongoose.connect(mongoURL, {
        dbName: 'Verkkokauppa'
    }
    ).then(() =>{
        console.log("Connection successful.")
        //Initialize API server
        app.listen(port, () =>{
            console.log("Server is running on port", port);
    });
}).catch((error) => console.log(error));

//Receive data
app.get("/products/ram", async(req, res) => {
    const ramData = await ramModel.find();
    res.json(ramData);
});

//Send data
app.post('/products/ram/add', async(req, res) => {
    try{
        const item = await ramModel.create(req.body);
        res.status(200).json(ramModel);
    } catch (error){
        res.status(500).json({message: error.message});
    }
});

//Run chatbot
app.get('/chatbot', async (req, res) => {
    try {
        const result = await runBot('Python/chat.py', [req.query.message]);
        res.json({result: result});
    } catch (error) {
        res.status(500).json({Error_message: error.message});
    }
})

// app.get('/test', (req, res) =>{
//     res.send("Hello")
// });