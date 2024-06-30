import discord
from discord.ext import commands

#-- Import Datetime for Cog Start Time --#
import datetime

class Help(commands.Cog, name = "Help", description = "Help command for Athena"):
    def __init__(self, bot):
        self.bot = bot
        self.StartTime = datetime.datetime.now()
        self.prefix = self.bot.prefix
        self.unloadable = True

    @commands.command(name="Help", description="Hang on a minute you're on this command right now!", usage='<all/module name/command>')
    async def help(self, ctx, *command):

        if not command:
            embed = discord.Embed(title="Help Command", description=f'Use `{self.prefix}help <module>` to gain more information about that module', colour=0x7DF9FF)
            cogs_desc = ''
            for cog in dict(sorted(self.bot.cogs.items())):
                cogs_desc += f'`{cog}` {self.bot.cogs[cog].description}\n'
            embed.add_field(name="Modules", value=cogs_desc, inline=False)

            embed.add_field(name="About", value=f"Athena is developed by HereticalSilence, using discord.py.\n")
            embed.set_footer(text=f"Bot is running V{self.bot.version}")

            return await ctx.send(embed=embed)

        elif command[0].lower() == "all":
            embed = discord.Embed(title=f'All commands', description=f'Use `{self.prefix}help <command>` to gain more information about that command', colour=0x7DF9FF)
            for cog in sorted(self.bot.cogs):
                commands = self.bot.get_cog(cog).get_commands()
                cogDesc = ""
                commandList = []
                for item in commands:
                    if item.hidden:
                        continue
                    if item.usage != None:
                        commandList.append([item.name, item.usage, item.description])
                    else:
                        commandList.append([item.name, item.description])
                    
                for command in sorted(commandList):
                    if len(command) == 2:
                        cogDesc+= f'`{self.prefix}{command[0]}` - {command[1]}\n'
                    elif len(command) == 3:
                        cogDesc+= f'`{self.prefix}{command[0]}` `{command[1]}` - {command[2]}\n'                
                embed.add_field(name=f'__**{cog}**__', value=cogDesc, inline=False)
                embed.add_field(name='\n', value="\n", inline=False)
            
            return await ctx.send(embed=embed)

        
        elif command[0].lower() != "all":
            try:
                commands = self.bot.get_cog(command[0].lower().capitalize()).get_commands()
            except:
                return await ctx.send(embed=discord.Embed(description="That module doesn't exist!", color=0x7DF9FF))
            else:
                embed = discord.Embed(title=f'{command[0].lower().capitalize()} - Commands', description=f'{self.bot.cogs[command[0].lower().capitalize()].description}', colour=0x7DF9FF)
                for command in commands:
                    if command.hidden:
                        continue
                    embed.add_field(name=f'`{self.prefix}{command.name}`', value=command.description, inline=False)
            
            return await ctx.send(embed=embed)

async def setup(bot):
	await bot.add_cog(Help(bot))