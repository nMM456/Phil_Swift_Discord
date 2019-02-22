import discord
from discord.ext import commands
import asyncio
import urllib.request

class Radio():
    def __init__(self, bot):
        self.bot = bot
    #commands for this module go here, in this class
    @commands.command()
    async def join(self, ctx):
            """Flex Seal the call!"""
            await ctx.send("Joining...")
            channel = ctx.author.voice.channel
            await channel.connect()

     @commands.command()
        async def leave(self, ctx):
            """Leave voice channel"""
            channel = ctx.author.voice.channel
            await channel.disconnect()


#Not part of class:
def setup(bot):
    bot.add_cog(Radio(bot))
