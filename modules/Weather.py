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
        try:
            url_get = requests.get(url)
            data = url_get.json()
            message="```"+data["features"][0]["properties"]["event"]+"\n"+"\n"
            message+=data["features"][0]["properties"]["headline"]+"\n"+"\n"
            message+=data["features"][0]["properties"]["description"]+"```"
            await ctx.send(message)
        except:
            await ctx.send("No alerts.")
    
    @commands.command()
    async def weather(self, ctx):
        """Returns weather in Westborough, MA"""
        url = 'https://api.weather.gov/points/42.2695,-71.6161/forecast'
        url_get = requests.get(url)
        data = url_get.json()
        message="```\n"
        for i in data["properties"]["periods"]:
            if i["number"] < 3:
                message += i["name"]+"\n"
                message += i["detailedForecast"]+"\n\n"
        await ctx.send(message+"```")

#Not part of class:
def setup(bot):
    bot.add_cog(Weather(bot))
