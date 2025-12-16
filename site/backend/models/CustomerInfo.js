const mongoose = require('mongoose')

const customerInfoModel = mongoose.model("customerInfo", 
    new mongoose.Schema({
        _id: {
            type:Object,
            required: false
        },
        name: {
            type:String,
            required: [true, "Pakollinen kenttä"]
        },
        password: {
            type:String,
            required: [true, "Pakollinen kenttä"]
        },
        address:{
            street: {
                type:String, 
                required: [true, "Pakollinen kenttä"]
            },
            postalCode: {
                type:String,
                required: [true, "Pakollinen kenttä"]
            },
            city: {
                type:String,
                required: [true, "Pakollinen kenttä"]
            },
            country: {
                type:String,
                required: [true, "Pakollinen kenttä"]
            }
        },
        email: {
            type:String,
            required: [true, "Pakollinen kenttä"]
        },
        phonenNumber: {
            type:String,
            required: [true, "Pakollinen kenttä"]
        },
        paymentDetails:{
            cardNumber: {
                type:Number,
                required: [true, "Pakollinen kenttä"]
            },
            cvc: {
                type:Number,
                required: [true, "Pakollinen kenttä"]
            },
            expirationDate: {
                type:String,
                required: [true, "Pakollinen kenttä"]
            },
            name: {
                type:String,
                required: [true, "Pakollinen kenttä"]
            }
        },
        Warranty:Number
    }), 'customerInfos'
)

module.exports = customerInfoModel