#-- Discord Imports --#
import discord
from discord.ext import commands

#-- Import Datetime for Cog Start Time --#
import datetime

class CogLoader(commands.Cog, name = "CogLoader", description = "Commands related to the loading and unloading of cogs."):
    def __init__(self, bot):
        self.bot = bot
        self.StartTime = datetime.datetime.now() #Cog Start Time (when loaded)
        self.unloadable = True #Determines if the cog can be unloaded

    #-- Embeds Function --#
    #-- Takes 4 parameters though colour is preset where necessary --#    
    async def createEmbed(self, ctx, title, description, colour=0x7DF9FF):
        return await ctx.send(embed = discord.Embed(title = title, description = description, colour = colour))
    
    #-- Load Cog Command --#
    @commands.command(name = "load", aliases = ["l"], description = "Loads a given cog", usage = "[Cog Name]")
    @commands.is_owner()
    async def load(self, ctx, *cogName : str):
        cog = "cogs."+cogName
        try:
            await self.bot.load_extension(cog)
        except Exception:
            await self.createEmbed(ctx, "ERROR", f"Could not load {cog}\n{Exception}")
        else:
            await self.createEmbed(ctx, "SUCCESS", f"Successfully loaded {cog}")
    
    #-- Unload Cog Command --#
    @commands.command(name = "unload", aliases = ["u"], description = "Unloads a given cog", usage = "[Cog Name]")
    @commands.is_owner()
    async def unload(self, ctx, *cogName : str):
        cog = "cogs."+cogName
        try:
            await self.bot.unload_extension(cog)
        except Exception:
            await self.createEmbed(ctx, "ERROR", f"Could not unload {cog}\n{Exception}")
        else:
            await self.createEmbed(ctx, "SUCCESS", f"Successfully unloaded {cog}")
            
#--Cog Setup Function --#
async def setup(bot):
    await bot.add_cog(CogLoader(bot))