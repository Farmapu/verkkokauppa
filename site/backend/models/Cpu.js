const mongoose = require('mongoose')

const cpuModel = mongoose.model("cpu", 
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
            core: {
                type:Number, 
                required: [true, "Pakollinen kenttä"]
            },
            socket: {
                type:String,
                required: [true, "Pakollinen kenttä"]
            },
            baseclock: {
                type:String,
                required: [true, "Pakollinen kenttä"]
            },
            turboclock: {
                type:String,
                required: [true, "Pakollinen kenttä"]
            },
            threads: {
                type:Number,
                required: [true, "Pakollinen kenttä"]
            },
            ramSupport: {
                type:String,
                required: [true, "Pakollinen kenttä"]
            },
            integratedGraphics: {
                type:Boolean,
                required: [true, "Pakollinen kenttä"]
            }
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
    }), 'cpus'
)

module.exports = cpuModel