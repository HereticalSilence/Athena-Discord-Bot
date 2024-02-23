#-- Import Discord Application Tokens --#
import secret

#-- Import Discord Related Packages --#
import discord
from discord.ext import tasks, commands
import asyncio

#-- Import SQLITE3 for database access --#
import sqlite3

#-- Additional Imports --#
import datetime
import random
import os

#-- Discord Intents --#
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.members = True
intents.message_content = True

#-- Bot Launcher --#
ValidSelection = False
while not ValidSelection:

    botSelection = int(input("Please select a bot to launch\n0. Athena\n1. Athena Dev\n-> "))

    if botSelection == 0:
        TOKEN = secret.Athena_Token
        prefix = "$"

        bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix), owner_id=secret.OwnerID, case_insensitive=True, intents=intents)
        
        ValidSelection = True

    elif botSelection == 1:
        TOKEN = secret.AthenaDev_Token
        prefix = "$$"

        bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix), owner_id=secret.OwnerID, case_insensitive=True, intents=intents)

        ValidSelection = True
        
    else:
        print ("ERROR: Invalid Bot Selection\n")

#-- Universal Variables --#
bot.prefix = prefix
bot.startTime = datetime.datetime.now()

#-- Initial Cogs --#
#This will eventually be replaced with a better way to do this
#by loading the cogs from a database but that is for later
initialCogs = []

#-- Load Cog Function --#
async def loadCog(cog):
    try:
        await bot.load_extension(cog)
    except Exception:
        print(Exception)
    else:
        print(f"{cog} was loaded successfully")

#-- Ready Function --#
@bot.event
async def on_ready():
    for cog in initialCogs:
        loadCog(cog)
    print(f"Logged in as {bot.user} (ID: {bot.user.id})\nStart Time: {bot.startTime}")

bot.run(TOKEN)