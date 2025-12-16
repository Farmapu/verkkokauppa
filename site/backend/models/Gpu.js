const mongoose = require('mongoose')

const gpuModel = mongoose.model("gpu", 
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
            clock: {
                type:String, 
                required: [true, "Pakollinen kenttä"]
            },
            boostclock: {
                type:String,
                required: [true, "Pakollinen kenttä"]
            },
            cuda: {
                type:String,
                required: [true, "Pakollinen kenttä"]
            },
            cudaCores: {
                type:String,
                required: [true, "Pakollinen kenttä"]
            },
            output: {
                type:String,
                required: [true, "Pakollinen kenttä"]
            },
            x: {
                type:String,
                required: [true, "Pakollinen kenttä"]
            },
            y: {
                type:Boolean,
                required: [true, "Pakollinen kenttä"]
            },
            pciGen: {
                type:String,
                required: [true, "Pakollinen kenttä"]
            },
            memory: {
                type:String,
                required: [true, "Pakollinen kenttä"]
            },
            lane: {
                type:String,
                required: [true, "Pakollinen kenttä"]
            },
            maxDisplays: {
                type:String,
                required: [true, "Pakollinen kenttä"]
            },
            sizeSlots: {
                type:String,
                required: [true, "Pakollinen kenttä"]
            },
            energyDraw: {
                type:String,
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
    }), 'gpus'
)

module.exports = gpuModel