const mongoose = require("mongoose");

const licenseSchema = new mongoose.Schema({
    hwid:  {
        type: String,
        required: true
    },
    discord: {
        type: String,
        required: true
    },
    discordId: {
        type: String,
        required: true
    },
    createdAt: {
        type: String,
        required: true
    }
}, {versionKey: false});


module.exports = mongoose.model("License", licenseSchema);