import json
from interactions import Client, listen, Status, Activity
from interactions import slash_command, SlashContext, slash_option
from interactions import Permissions, slash_default_member_permission
from interactions import OptionType
from interactions import Embed
import interactions
from time import sleep
from datetime import datetime
from interactions import Embed
from colored import fg as color
import requests

# Configuration
config = json.load(open("config.json"))
guild = config["guild"]
version = config["version"]
apiKey = config["apiKey"]
bot = Client(status=Status.DND, activity=Activity(name="over cheating plebs", type=interactions.ActivityType.WATCHING), intents=interactions.Intents.ALL, token=config["token"])

@listen
async def on_ready():
    print(f'Cipher Client bot is up and running.')

@slash_command(
        name="addclient",
        description="Add Client to User",
        scopes=[guild])
@slash_option(name="user", description="User reciving license", required=True, opt_type=OptionType.USER)
@slash_option(name="hwid", description="Hardware ID of user", required=True, opt_type=OptionType.STRING)
@slash_default_member_permission(Permissions.ADMINISTRATOR)
async def addClientCommand(ctx: SlashContext, user, hwid: str):
    await ctx.defer()
    discordId = user.id
    userExists = userExist(discordId)

    if(userExists):
        return await ctx.send("User already has a license")

    headers = {
        "apikey": apiKey
    }

    data = {
        "hwid": hwid,
        "discord": user.tag,
        "discordId": discordId
    }

    req = requests.post("http://api.gyazo.cam/api/add", headers=headers, json=data)
    
    hwid = req.json()['hwid']
    createdAt = req.json()['createdAt']

    embed = Embed(
    title="**User Added ✅**",
    color=40191,
    fields=[interactions.EmbedField(name="**HWID**", value=hwid, inline=False),
                interactions.EmbedField(name="**Created At**", value=createdAt, inline=False)],
    footer=interactions.EmbedFooter(text=f"Cipher Client @ {datetime.now().strftime('%m/%d/%y')}", icon_url="https://i.imgur.com/uBjHq0U.png"))
    
    embed.set_thumbnail(url=user.avatar_url)

    return await ctx.send(embeds=embed)

@slash_command(
        name="removeclient",
        description="Remove Client to User",
        scopes=[guild])
@slash_option(name="user", description="User that is getting license removed", required=True, opt_type=OptionType.USER)
@slash_default_member_permission(Permissions.ADMINISTRATOR)
async def removeClientCommand(ctx: SlashContext, user):
    await ctx.defer()
    discordId = user.id
    userExists = userExist(discordId)

    if userExists == False:
        return await ctx.send("User does not have a license")
    hwid = getHwid(discordId)
    req = requests.post("http://api.gyazo.cam/api/remove", headers={"apikey": apiKey}, json={"hwid": hwid})

    embed = Embed(
    title="**User Removed 🗙**",
    color=40191,
    fields=[interactions.EmbedField(name="**User**", value=user.tag, inline=False)],
    footer=interactions.EmbedFooter(text=f"Cipher Client @ {datetime.now().strftime('%m/%d/%y')}", icon_url="https://i.imgur.com/uBjHq0U.png"))
    
    embed.set_thumbnail(url=user.avatar_url)

    return await ctx.send(embeds=embed)

@slash_command(
        name="info",
        description="Returns info about user",
        scopes=[guild])
@slash_option(name="user", description="User info", required=True, opt_type=OptionType.USER)
@slash_default_member_permission(Permissions.ADMINISTRATOR)
async def infoCommand(ctx: SlashContext, user):
    await ctx.defer()
    discordId = user.id
    userExists = userExist(discordId)

    if userExists == False:
        return await ctx.send("User does not have a license")

    req = requests.get("http://api.gyazo.cam/api/info", headers={"apikey": apiKey}, json={"discordId": discordId})

    hwid = req.json()['hwid']
    createdAt = req.json()['createdAt']
    embed = Embed(
    title="**Cipher Client**",
    description="Client Info :video_game: ",
    color=40191,
    fields=[interactions.EmbedField(name="**HWID**", value=hwid, inline=False),
                interactions.EmbedField(name="**Created At**", value=createdAt, inline=False)],
    footer=interactions.EmbedFooter(text=f"Cipher Client @ {datetime.now().strftime('%m/%d/%y')}", icon_url="https://i.imgur.com/uBjHq0U.png"))
    
    embed.set_thumbnail(url=user.avatar_url)

    return await ctx.send(embeds=embed)

def userExist(discordId: str):
    req = requests.get("http://api.gyazo.cam/api/info", headers={"apikey": apiKey}, json={"discordId": discordId})
    if req.status_code == 403: return KeyError
    elif req.status_code == 404: return False
    elif req.status_code == 200: return True

def getHwid(discordId: str):
    req = requests.get("http://api.gyazo.cam/api/info", headers={"apikey": apiKey}, json={"discordId": discordId})
    if req.status_code == 403: return KeyError
    elif req.status_code == 404: return False
    elif req.status_code == 200:
        return req.json()['hwid']

# Start Discord Bot
bot.start()