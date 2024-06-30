#-- Import Discord --#
import discord

#-- Import Commands and Tasks --#
from discord.ext import commands, tasks

#-- Import Datetime for Cog Start Time and Uptime --#
import datetime 

class Info(commands.Cog, name = "Info", description = "Information about Athena and Members"):
    def __init__(self, bot):
        self.bot = bot
        self.unloadable = True
        self.bot.version = "0.1"
        self.version = self.bot.version
        self.start_time = self.bot.startTime
        self.StartTime = datetime.datetime.now()
        self.statusChange.start()
        self.last_status = ""
    
    def cog_unload(self):
        print ("Cancelling Status Change Task")
        self.statusChange.cancel()
    
    #-- Version Command --#
    @commands.command(name="Version", aliases=["v"], description="Displays Athena's current version")
    async def version(self, ctx):
        embed = discord.Embed(description="I'm on **V" + self.version + "** of Athena.py", color=0x7DF9FF)
        return await ctx.send(embed=embed)
    
        #-- Uptime Formatting Function --#
    def uptimeCalc(self):
        now = datetime.datetime.now()
        delta = now - self.start_time
        days, remainder = divmod(int(delta.total_seconds()), 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        if days < 10:
             days = "0" + str(days)
        if hours < 10:
            hours = "0" + str(hours)
        if minutes < 10:
            minutes = "0" + str(minutes)
        return days, hours, minutes



    #-- Uptime Command --#
    @commands.command(name="Uptime", description="Shows how long Athena has been awake for!")
    async def uptime(self, ctx):
        days, hours, minutes = self.uptimeCalc()
        return await ctx.send(embed=discord.Embed(description=f"I've been awake for **{days}d** **{hours}h** **{minutes}m**\nWhew, where's the coffee? :coffee:", color=0x7DF9FF))
    
    @tasks.loop(seconds=15.0)
    async def statusChange(self):
        days, hours, minutes = self.uptimeCalc()
        #statusMessage = random.choice(["Athena | V"+self.bot.version, f"Athena | {self.bot.prefix}help", f"Athena | {uptimeData}"])
        return await self.bot.change_presence(activity=discord.Activity(type=0, name=f"Athena | {self.bot.prefix}help", state=f"{days}d {hours}h {minutes}m | V{self.bot.version}", details=f'V{self.bot.version}'))

async def setup(bot):
	await bot.add_cog(Info(bot))