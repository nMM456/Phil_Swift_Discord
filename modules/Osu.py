import discord
from discord.ext import commands
import asyncio
import urllib.request
import requests

class Osu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    #commands for this module go here, in this class
    @commands.command()
    async def osustats(self, ctx, user):
      """Find out how much pp someone has in osu!"""
      url = 'https://osu.ppy.sh/api/get_user?k=KEY_HERE&u='+user
      url_get = requests.get(url)
      data = url_get.json()
      formattedMes=""
      for i in data[0]:
        if i != "events":
          formattedMes+=i+": ``"+data[0][i]+"``\n"
      embed=discord.Embed(title="**"+data[0]["username"]+"'s " + "Stats**", description=formattedMes)
      embed.set_author(name="osu!")
      embed.set_footer(text="blue zenith 727 lol")
      await ctx.send(embed=embed)

#Not part of class:
def setup(bot):
    bot.add_cog(Osu(bot))
