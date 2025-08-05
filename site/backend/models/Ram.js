const mongoose = require('mongoose')

const ramModel = mongoose.model("ram", 
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
            ddr: {
                type:Number, 
                required: [true, "Pakollinen kenttä"]
            },
            memorySize: {
                type:Number,
                required: [true, "Pakollinen kenttä"]
            },
            memorySpeed: {
                type:Number,
                required: [true, "Pakollinen kenttä"]
            },
            cl: {
                type:Number,
                required: [true, "Pakollinen kenttä"]
            },
            energyDraw: {
                type:Number,
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
    }), 'rams'
)

module.exports = ramModel