import discord
from discord.ext import commands
import asyncio
import requests
import time
import urllib.request


class OWL(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    #commands for this module go here, in this class
    @commands.command()
    async def player(self, ctx, playerName):
        """Put in a players name, returns picture of player, such as fissure."""
        try:
          url = 'https://api.overwatchleague.com/teams'
          url_get = requests.get(url)
          data = url_get.json()
          await ctx.send('Fetching data...')
          for x in range(len(data["competitors"])):
            for i in range(len(data["competitors"][x]["competitor"]["players"])):
              if data["competitors"][x]["competitor"]["players"][i]["player"]["name"].lower() == playerName:
                headshot = data["competitors"][x]["competitor"]["players"][i]["player"]["headshot"]
                break
          urllib.request.urlretrieve(headshot, 'player.png')
          await ctx.send(file=discord.File('player.png', filename='player.png'))
        except:
          await ctx.send("Player not found.")

    @commands.command()
    async def currentgame(self, ctx):
        """Returns the current Overwatch League score"""
        try:
            url = 'https://api.overwatchleague.com/live-match'
            url_get = requests.get(url)
            data = url_get.json()
            await ctx.send('Fetching data...')
            
            team1 = data["data"]["liveMatch"]["competitors"][0]["name"]
            team2 = data["data"]["liveMatch"]["competitors"][1]["name"]
            scoreOne = str(data["data"]["liveMatch"]["scores"][0]["value"])
            scoreTwo = str(data["data"]["liveMatch"]["scores"][1]["value"])
        
            await ctx.send((('Current game: ' + team1) + ' V. ') + team2)
            await ctx.send((team1 + ': ') + scoreOne)
            await ctx.send((team2 + ': ') + scoreTwo)
        except:
            await ctx.send("No current game.")
    @commands.command()
    async def stats(self, ctx, player):
      """Find some stats about OWL players"""
      try:
        await ctx.send('Fetching data...')
        url = 'https://api.overwatchleague.com/stats/players'
        url_get = requests.get(url)
        data = url_get.json()
        niceName=" "
        for x in range(len(data["data"])):
          if data["data"][x]["name"].lower() == player.lower():
            niceName=data["data"][x]["name"]
          else:
            break
        formattedMes = " "
        for x in range(len(data["data"])):
          if data["data"][x]["name"].lower() == player.lower():
            for y in data["data"][x]:
              if type(data["data"][x][y]) is float:
                formattedMes = formattedMes + y.replace("_", " ").capitalize() +": ``"+str(int(data["data"][x][y]))+"``\n"
              else:
                formattedMes = formattedMes + y.capitalize() +": ``"+str(data["data"][x][y])+"``\n"
                
        embed=discord.Embed(title="**"+niceName+"'s " + "Stats**", description=formattedMes)
        embed.set_author(name="OWL", url="https://overwatchleague.com", icon_url="https://bnetcmsus-a.akamaihd.net/cms/page_media/JEUWQ6CN33BR1507857496436.svg")
        embed.set_footer(text="It's 3AM and Jake has a riptire in your room")
        await ctx.send(embed=embed)
      except:
        await ctx.send("No data found for the player.")

    @commands.command()
    async def players(self, ctx):
      """Get a list of OWL players from the API"""
      await ctx.send('Fetching data...')
      url = 'https://api.overwatchleague.com/players'
      url_get = requests.get(url)
      data = url_get.json()
      playerlist = []
      playMessage = "```Players:\n"
      for x in range(len(data["content"])):
        playerlist.append(data["content"][x]["name"])
      for i in playerlist:
        playMessage = playMessage + "\n" + i
      await ctx.send(playMessage+"```")
      
    @commands.command()
    async def schedule(self, ctx):
        """Find out when the next 4 OWL game starts"""
        await ctx.send("Fetching data...")
        url = 'https://api.overwatchleague.com/schedule'
        url_get = requests.get(url)
        data = url_get.json()
        current = int(time.time())
        found=False    
        for x in range(len(data["data"]["stages"])):        
            for i in range(len(data["data"]["stages"][x]["matches"])):
                if data["data"]["stages"][x]["matches"][i]["startDateTS"]/1000 > current:
                    count=i
                    message=""
                    while count<i+4:
                        gametime = data["data"]["stages"][x]["matches"][count]["startDateTS"]/1000
                        atime = time.strftime('%Y-%m-%d %I:%M:%S', time.localtime(gametime-18000))
                        team1 = data["data"]["stages"][x]["matches"][count]["competitors"][0]["name"]
                        team2 = data["data"]["stages"][x]["matches"][count]["competitors"][1]["name"]
                        message = message+ team1+" V. "+team2+"\n"
                        message = message+ atime+" EST\n"
                        found=True
                        count+=1
                    await ctx.send(message)
                    break
            if found:
                break
                
    @commands.command()
    async def rankings(self, ctx):
      """Display the current rankings in the OWL based off of map differential"""
      await ctx.send("Fetching data...")
      url = 'https://api.overwatchleague.com/rankings'
      url_get = requests.get(url)
      data = url_get.json()
      message="```OWL ranking by map differential:\n"
      for i in data["content"]:
        message+=str(i["placement"])+". "+i["competitor"]["name"]+": "+str(i["records"][0]["comparisons"][1]["value"])+"\n"
      message+="```"
      await ctx.send(message)
      
    @commands.command()
    async def teams(self, ctx):
        """List all teams in the OWL"""
        await ctx.send("Fetching data...")
        url = 'https://api.overwatchleague.com/teams'
        url_get = requests.get(url)
        data = url_get.json()
        message="```"
        for teams in data["competitors"]:
            message+= teams["competitor"]["name"]+"\n"
        message+="```"
        await ctx.send(message)
        
    @commands.command()
    async def CSV(self, ctx):
        """Grab all the players stats and export them as a CSV"""
        url = 'https://api.overwatchleague.com/stats/players'
        url_get = requests.get(url)
        data = url_get.json()
        f = open("stats.csv", "w")
        for i in data["data"][0]:
            if str(i) != "time_played_total":
                f.write(str(i)+", ")
            else:
                f.write(str(i))
        f.write("\n")
        for x in data["data"]:
            for i in x:
                if str(i) != "time_played_total":
                    f.write(str(x[i])+", ")
                else:
                    f.write(str(x[i]))
            f.write("\n")
        await ctx.send(file=discord.File('stats.csv', filename='stats.csv'))
#Not part of class:
def setup(bot):
    bot.add_cog(OWL(bot))
