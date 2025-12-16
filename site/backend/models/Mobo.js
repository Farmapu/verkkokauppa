const mongoose = require('mongoose')

const moboModel = mongoose.model("mobo", 
    new mongoose.Schema({
        _id: {
            type:Object,
            required: false
        },
        name: {
            type:String,
            required: [true, "Pakollinen kenttä"]
        },
        Technical:{
            piiriSarja: {
                type:String, 
                required: [true, "Pakollinen kenttä"]
            },
            socket: {
                type:String,
                required: [true, "Pakollinen kenttä"]
            },
            compitableProcessors: {
                type:String,
                required: [true, "Pakollinen kenttä"]
            },
            internalIO: {
                moboPower: {
                    type:String,
                    required: [true, "Pakollinen kenttä"]
                },
                cpuPower: {
                    type:String,
                    required: [true, "Pakollinen kenttä"]
                },
                cpuFan: {
                    type:String,
                    required: [true, "Pakollinen kenttä"]
                },
                pumpFan: {
                    type:String,
                    required: [true, "Pakollinen kenttä"]
                },
                systemFan: {
                    type:String,
                    required: [true, "Pakollinen kenttä"]
                },
                frontAudio: {
                    type:String,
                    required: [true, "Pakollinen kenttä"]
                }
            },
            externalIO: {
                hdmi: {
                    type:Number,
                    required: [true, "Pakollinen kenttä"]
                },
                displayport: {
                    type:Number,
                    required: [true, "Pakollinen kenttä"]
                },
            },
        },
        Price:{
            withoutTax: {
                type:Number,
                required: [true, "Pakollinen kenttä"]
            },
            taxAmount: {
                type:Number,
                required: [true, "Pakollinen kenttä"]
            },
            totalPrice: {
                type:Number,
                required: [true, "Pakollinen kenttä"]
            }
        },
        Warranty:Number
    }), 'mobos'
)

module.exports = moboModel