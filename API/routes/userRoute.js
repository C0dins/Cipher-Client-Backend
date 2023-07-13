const router = require("express").Router();
const config = require("../config.json");
const User = require("../models/User");
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
	windowMs: 60 * 1000,
	max: 3,
    message:'Too many requests created from this IP, please try again after an bit',
	standardHeaders: true,
	legacyHeaders: false,
})


router.post("/add", async (req, res) => {
    const {apikey} = req.headers;
    if (apikey != config.apiKey) {
        return res.status(401).send("You must send a Valid Authorization header")
    }
    if (req.body.hwid == null || req.body.discord == null || req.body.discordId == null){
        return res.status(403).send("Invalid body not enough info found!")
    }
    
    const hwid = req.body.hwid
    const discord = req.body.discord
    const discordId = req.body.discordId
    const createdAt = new Date().toLocaleDateString("en-US")
    let user = new User({hwid, discord, discordId, createdAt})

    try{
        const userSave = await user.save();
        const data = {
            hwid: hwid,
            createdAt: userSave.createdAt
        }
        return res.send(data)
    } catch (err){
        console.log(err)
    }

})

router.post("/remove", async (req, res) => {
    const {apikey} = req.headers;
    if (apikey != config.apiKey) {
        return res.status(401).send("You must send a Valid Authorization header")
    }

    const hwid = req.body.hwid
    if (hwid == null) {
        return res.status(403).send("Invalid body not enough info found!")

    }
    const doc = await User.deleteOne({hwid: hwid})
    if(!doc.acknowledged){
        return res.status(400).send("Error while deleting User")
    } else if(doc.deletedCount == 0){
        return res.status(404).send("No user found with that Hardware ID")
    } else if(doc.deletedCount > 0){
        return  res.send("Successfully deleted " + hwid)
    }
    
})

router.get("/info", async (req, res) => {
    const {apikey} = req.headers;
    if (apikey !== config.apiKey) {
        return res.status(401).send("You must send a Valid Authorization header");
    }

    const discordID = req.body.discordId
    if (discordID == null) {
        return res.status(403).send("Please provide a valid discord user")
    }

    const doc = await User.findOne({discordId: discordID})

    if(doc == null){
        return res.status(404).send("Not found")
    }

    const data = {
        hwid: doc.hwid,
        discord: doc.discord,
        discordId: doc.discordId,
        createdAt: doc.createdAt
    }

    res.send(data)
})

router.post("/auth", limiter, async (req, res) => {
    const hwid = req.body.hwid
    const ip = req.ip.substring(7)

    console.log("[" + new Date().toLocaleDateString("en-US") + "] Auth Request by " + ip + " on " + hwid)

    if (hwid == null) {
        return  res.status(403).send("Invalid body not enough info found!")
    }

    const doc = await User.findOne({hwid: hwid})

    if(doc == null){
        return  res.status(404).send("Not found")
    }


    res.send("License is valid") 

})


module.exports = router;