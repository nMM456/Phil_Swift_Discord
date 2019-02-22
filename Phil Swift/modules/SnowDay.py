import discord
from discord.ext import commands
import asyncio
import urllib.request

class SnowDay():
    def __init__(self, bot):
        self.bot = bot
    #commands for this module go here, in this class
    @commands.command()
    async def snow(self, ctx, zip, days):
        """Checks snow day chance for a zip code and how many days. ONLY does public schools."""
        await ctx.send("Checking...")
        link = "https://www.snowdaycalculator.com/prediction.php?zipcode=" + zip
        + "&snowdays=" + days + "&extra=0&"
        data = str(urllib.request.urlopen(link).read())
        
#Not part of class:
def setup(bot):
    bot.add_cog(SnowDay(bot))
