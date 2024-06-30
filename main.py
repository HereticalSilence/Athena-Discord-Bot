#-- Import Discord Application Tokens --#
import secret

#-- Import Discord Related Packages --#
import discord
from discord.ext import tasks, commands

#-- Import psycopg2 for database access --#
import psycopg2

#-- Additional Imports --#
import datetime

#-- Connect to Database Function --#
#-- This function is used to connect to the database --#
#-- It takes the database name as a parameter and returns the cursor and connection --#
def connectToDatabase(Database):
    print (f"Attempting to connect to {Database} database")
    try:
        connection = psycopg2.connect(user = secret.DatabaseUser, password = secret.DatabasePassword, host = secret.DatabaseHost, port = secret.DatabasePort, database = Database)
        cursor = connection.cursor()
        print (f"Connected to {Database} database successfully")
        return cursor, connection
    except (Exception, psycopg2.Error) as error:
        print(f"Error while connecting to {Database}", error)


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
        bot.dbCursor, bot.dbConnection = connectToDatabase("Athena")

        ValidSelection = True

    elif botSelection == 1:
        TOKEN = secret.AthenaDev_Token
        prefix = "$$"

        bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix), owner_id=secret.OwnerID, case_insensitive=True, intents=intents)
        bot.dbCursor, bot.dbConnection = connectToDatabase("Athena-Dev")

        ValidSelection = True
        
    else:
        print ("ERROR: Invalid Bot Selection\n")

#-- Bot Start Time --#
bot.startTime = datetime.datetime.now()

#-- Remove Standard Help Command --#
bot.remove_command('help')

#-- Universal Variables --#
bot.prefix = prefix
bot.startTime = datetime.datetime.now()

#-- Initial Cogs --#
bot.dbCursor.execute("SELECT modulename FROM modules WHERE enabled = True;")
initialCogs = bot.dbCursor.fetchall()
bot.dbConnection.close()

#-- Load Cog Function --#
async def loadCog(cog):
    try:
        await bot.load_extension("cogs." + cog[0])
    except Exception:
        print(Exception)
    else:
        print(f"{cog[0]} was loaded successfully")

#-- Ready Function --#
@bot.event
async def on_ready():
    print ("\n---------------------------------")
    for cog in initialCogs:
        await loadCog(cog)
    print ("---------------------------------\n")
    print(f"Logged in as {bot.user} (ID: {bot.user.id})\nStart Time: {bot.startTime}")
    

bot.run(TOKEN)