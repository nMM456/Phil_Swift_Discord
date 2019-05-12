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
    async def emotes(self, ctx):
        """List of ASCII emotes."""
        data = json.load(open("Emotes.json"))
        message="```\n"
        for i in data:
            message+=i+"\n"
        message+="```"
        await ctx.send(message)
        
    @commands.command()
    async def showemote(self, ctx, emote):
        """Shows ASCII art based off of the following parameter."""
        data = json.load(open("Emotes.json"))
        try:
            await ctx.send(data[emote])
        except:
            await ctx.send(emote+" does not exist.")
        await ctx.message.delete()
                
#Not part of class:
def setup(bot):
    bot.add_cog(Emotes(bot))
