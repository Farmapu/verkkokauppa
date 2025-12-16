const mongoose = require('mongoose')

const ordersModel = mongoose.model("order", 
    new mongoose.Schema({
        _id: {
            type:Object,
            required: false
        },
        itemID: {
            type:String,
            required: [true, "Pakollinen kenttä"]
        },
        customerID: {
            type:String,
            required: [true, "Pakollinen kenttä"]
        },orderFullPrice: {
            type:String,
            required: [true, "Pakollinen kenttä"]
        }
    }), 'orders'
)

module.exports = customerInfoModel