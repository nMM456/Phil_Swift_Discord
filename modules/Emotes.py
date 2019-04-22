import discord
from discord.ext import commands
import asyncio
import json

#Untested! emotes are stored in Emotes.json and will be added as strings. Other ways to store 
#data are to be considered unless this is the best option. (poorly made this in math class in a few minutes)
class Emotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    #commands for this module go here, in this class
    @commands.command()
    async def showemote(self, ctx, emote):
        """Shows ASCII art based off of the following parameter."""
        f = open("r", "Emotes.json")
        data = json.loads(f)
        try:
            await ctx.send(data[emote])
        except:
            await ctx.send("Emote '"+emote+"' does not exist.")
        
#Not part of class:
def setup(bot):
    bot.add_cog(Emotes(bot))
