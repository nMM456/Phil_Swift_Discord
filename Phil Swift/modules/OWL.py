import discord
from discord.ext import commands
import urllib.request
import asyncio


class OWL():
    def __init__(self, bot):
        self.bot = bot
    #commands for this module go here, in this class
    @commands.command()
    async def player(self, ctx, playername):
        """Put in a players name, returns picture of player, such as fissure."""
        playlink = 'https://api.overwatchleague.com/teams/'
        rawData = str(urllib.request.urlopen(playlink).read()).lower()
        await ctx.send('Fetching data...')
        player = rawData.find('"name":"' + playername.lower())
        playerlink = rawData.find('headshot":"', player) + 11
        playerlinktwo = rawData.find('","erased', player)
        rawData = str(urllib.request.urlopen(playlink).read())
        headshot = str(rawData[playerlink:playerlinktwo])
        urllib.request.urlretrieve(headshot, 'player.png')
        await ctx.send(file=discord.File('player.png', filename='player.png'))

    @commands.command()
    async def OWL(self, ctx):
        
        """Returns the current Overwatch League score"""
        try:
            rawData = str(urllib.request.urlopen("https://api.overwatchleague.com/live-match").read())
            await ctx.send('Fetching data...')
            
            nameOne = rawData.index('"name":"') + 8
            nameTwo = rawData.index('","primaryColor')
            team1 = rawData[nameOne:nameTwo]

            nameOne = rawData.index('"name":"', 400) + 8
            nameTwo = rawData.index('","primaryColor', 400)
            team2 = rawData[nameOne:nameTwo]

            scorePOne = rawData.index('{"value":') + 9
            scorePTwo = rawData.index('{"value":') + 10
            scoreOne = str(rawData[scorePOne:scorePTwo])

            scorePOne = rawData.index('{"value":') + 21
            scorePTwo = rawData.index('{"value":') + 22
            scoreTwo = str(rawData[scorePOne:scorePTwo])
        
            await ctx.send((('Current game: ' + team1) + ' V. ') + team2)
            await ctx.send((team1 + ': ') + scoreOne)
            await ctx.send((team2 + ': ') + scoreTwo)
        except:
            await ctx.send("No current game.")
    @commands.command()
    async def stats(self, ctx, player):
        """Find some stats about OWL players"""
        await ctx.send('Fetching data...')
        playerL = player.lower()
        data = str(urllib.request.urlopen('https://api.overwatchleague.com/stats/players').read()).lower()
        location = data.find(playerL)
        info1 = data.find("eliminations_avg_per_10m", location,) + 26
        info2 = data.find(',', info1)
        elims = data[info1:info2]
        elims = data[info1:data.find(".",info1)]
        embed=discord.Embed(title=player +" " + "Stats", url="https://overwatchleague.com/en-us/stats", description="See this players stats during the Overwatch League.")
        embed.set_author(name="OWL", url="https://overwatchleague.com", icon_url="https://vignette.wikia.nocookie.net/overwatch/images/c/cc/Competitive_Grandmaster_Icon.png/revision/latest?cb=20161122023845")
        embed.add_field(name="Average Elims Per 10 Minutes: ", value=str(elims), inline=True)
        embed.set_footer(text="It's 3AM and Jake has a riptire in your room")
        await ctx.send(embed=embed)

    @commands.command()
    async def players(self, ctx):
      """Get a list of OWL players from the API"""
      await ctx.send('Fetching data...')
      playerlink = 'https://api.overwatchleague.com/players/'
      coolData = str(urllib.request.urlopen(playerlink).read())
      rawData = str(urllib.request.urlopen(playerlink).read())
      player = 10
      playerlist = []
      playMessage = "```Players:\n"
      while True:
        player = rawData.find('","name":', player)
        playerEnd = rawData.find('","homeLocation":"', player)
        name = coolData[player+10:playerEnd]
        if player == -1:
            break
        if playerEnd != -1 and len(name) < 100 and name.find(" ") == -1:
            playerlist.append(name)
            player = player + len(name)
        else:
            player = player+100
      for i in playerlist:
        playMessage = playMessage + "\n" + i
      await ctx.send(playMessage+"```")
    
#Not part of class:
def setup(bot):
    bot.add_cog(OWL(bot))
