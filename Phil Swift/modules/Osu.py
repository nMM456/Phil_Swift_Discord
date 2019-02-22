import discord
from discord.ext import commands
import asyncio
import urllib.request
import json

class Osu():
    def __init__(self, bot):
        self.bot = bot
    #commands for this module go here, in this class
    @commands.command()
    async def pp(self, ctx, user):
        url = "https://osu.ppy.sh/api/get_user?k=KEY&u="
        url += user
        data = str(urllib.request.urlopen(url).read())
        data = data[3:len(data)-2]
        data = json.loads(data)
        await ctx.send(data['username'] + ": " + data['pp_raw'])

#Not part of class:
def setup(bot):
    bot.add_cog(Osu(bot))
