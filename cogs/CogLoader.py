#-- Discord Imports --#
import discord
from discord.ext import commands

#-- Import Datetime for Cog Start Time --#
import datetime

class CogLoader(commands.Cog, name = "CogLoader", description = "Commands related to the loading and unloading of cogs."):
    def __init__(self, bot):
        self.bot = bot
        self.StartTime = datetime.datetime.now() #Cog Start Time (when loaded)
        self.unloadable = False #Determines if the cog can be unloaded - False means it cannot be unloaded

    #-- Embeds Function --#
    #-- Takes 3 parameters though colour is preset where necessary --#    
    def createEmbed(self, title, description, colour=0x7DF9FF):
        return discord.Embed(title = title, description = description, colour = colour)
    
    #-- Load Cog Command --#
    @commands.command(name = "Load", aliases = ["l"], description = "Loads a given cog", usage = "<Cog Name>")
    @commands.is_owner()
    async def load(self, ctx, cog):
        try:
            await self.bot.load_extension("cogs."+cog)
        except Exception as ExceptionMessage:
            return await ctx.send(embed=self.createEmbed("ERROR", f"Could not load {cog}\n{ExceptionMessage}"))
        else:
            return await ctx.send(embed=self.createEmbed("SUCCESS", f"Successfully loaded {cog}"))
    
    #-- Unload Cog Command --#
    @commands.command(name = "Unload", aliases = ["u"], description = "Unloads a given cog", usage = "<Cog Name>")
    @commands.is_owner()
    async def unload(self, ctx, cog):
        if not self.bot.cogs[cog].unloadable:
            return await ctx.send(embed=self.createEmbed("ERROR", f"Could not unload {cog} as it is unloadable."))
        try:
            await self.bot.unload_extension("cogs."+cog)
        except Exception as ExceptionMessage:
            return await ctx.send(embed=self.createEmbed("ERROR", f"Could not unload {cog}\n{ExceptionMessage}"))
        else:
            return await ctx.send(embed=self.createEmbed("SUCCESS", f"Successfully unloaded {cog}"))
    
    #-- Reload Cog Commands --#
    @commands.command(name = "Reload", aliases = ["r", "Refresh"], description = "Reloads a given cog", usage = "<Cog Name or all>")
    @commands.is_owner()
    async def reload(self, ctx, cog):
        if cog.lower() == "all":
            embed = self.createEmbed("", None)
            for cog in dict(sorted(self.bot.cogs.items())):
                if not self.bot.cogs[cog].unloadable:
                    embed.add_field(name=" ", value=f':warning: {cog} was not reloaded as it is unloadable', inline=False)
                else:
                    try:
                        await self.bot.unload_extension("cogs."+cog)
                        await self.bot.load_extension("cogs."+cog)
                    except Exception as ExceptionMessage:
                        embed.add_field(name=" ", value=f':warning: {cog} was not reloaded\n\t{ExceptionMessage}', inline=False)
                    else:
                        embed.add_field(name=" ", value=f':white_check_mark: {cog} was reloaded', inline=False)
            return await ctx.send(embed=embed)
        else:
            if not self.bot.cogs[cog].unloadable:
                return await ctx.send(embed=self.createEmbed("ERROR", f"Could not unload {cog} as it is unloadable."))
            try:
                await self.bot.unload_extension("cogs."+cog)
                await self.bot.load_extension("cogs."+cog)
            except Exception as ExceptionMessage:
                return await ctx.send(embed=self.createEmbed("ERROR", f"{cog} could not be reloaded\n{ExceptionMessage}"))
            else:
                return await ctx.send(embed=self.createEmbed("Success", f"{cog} was reloaded"))

            
#--Cog Setup Function --#
async def setup(bot):
    await bot.add_cog(CogLoader(bot))