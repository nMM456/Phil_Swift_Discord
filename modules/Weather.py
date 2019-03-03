import discord
from discord.ext import commands
import asyncio
import requests

class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    #commands for this module go here, in this class
    @commands.command()
    async def alerts(self, ctx):
        """Get Alerts for the Worcester area."""
        url = 'https://api.weather.gov/alerts/active/zone/MAZ012'
        url_get = requests.get(url)
        data = url_get.json()
        message="```"+data["features"][0]["properties"]["event"]+"\n"+"\n"
        message+=data["features"][0]["properties"]["headline"]+"\n"+"\n"
        message+=data["features"][0]["properties"]["description"]+"```"
        await ctx.send(message)

#Not part of class:
def setup(bot):
    bot.add_cog(Weather(bot))
