import discord
from discord.ext import commands
import asyncio
import urllib.request

class FlexSeal():
    def __init__(self, bot):
        self.bot = bot
    #commands for this module go here, in this class
    @commands.command()
    async def flextape(self, ctx):
        """Find out about Flex Tape!"""
        urllib.request.urlretrieve("https://cdn.glitch.com/74e2ec8d-3eb3-4996-9ac4-655fca6e9f6a%2Fphil.txt?1540241809798", "phil.txt")
        quote = open("phil.txt","r")
        await ctx.message.delete()
        await ctx.send(quote.read())
        quote.close()

#    @commands.command()
#    async def flexseal(self, ctx):
#        """Flex Seal the call!"""
#        await ctx.send("Joining...")
#        channel = ctx.author.voice.channel
#        await channel.connect()


#Not part of class:
def setup(bot):
    bot.add_cog(FlexSeal(bot))
