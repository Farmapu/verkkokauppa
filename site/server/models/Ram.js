const mongoose = require('mongoose')

const ramModel = mongoose.model("rams", 
    new mongoose.Schema({
        _id: Object,
        name: String,
        Technical:{
            ddr: String,
            memorySize: String,
            memorySpeed: String,
            cl: String
        },
        Price:{
            withoutTax: String,
            taxAmount: String,
            totalPrice: String
        },
        Warranty: String
    }), 'rams'
)

module.exports = ramModel