import discord
from discord.ext import commands
import asyncio
import sys
import io
import datetime
import os
import json

def get_prefix(bot, message):
    '''A callable Prefix for our bot. This could be edited to allow per server prefixes.'''
    prefix = '!'
    if (not message.guild):  #Check to see if we are outside of a guild. e.g DM's etc.
        return '!' #Only allow ! to be used in DMs
    return commands.when_mentioned_or(prefix)(bot, message)

description = 'Phil Swift here to tell you about Flex Tape!'
startup_extensions = ['modules.Misc', #Default extensions (all enabled)
                      'modules.OWL',
                      'modules.Osu',
                      'modules.FlexSeal',
                      'modules.Weather',
                      #continued
                    ]
tokens = json.load(open("tokens.json"))
bot = commands.Bot(command_prefix=get_prefix, description=description)
bot.remove_command('help')

@bot.event
async def on_ready():
  print('**______----------------------------STARTING----------------------------______**')
  print('Logged in as')
  print(bot.user.name)
  print(bot.user.id)
  print("**Date:** " + str(datetime.datetime.now()))
  await bot.change_presence(activity=discord.Game(name='with Flex Tape'))
    
@bot.event
async def on_guild_join(guild):
    dir = os.getcwd()+"/servers/"
    os.mkdir(dir)
    os.makedirs(dir+str(guild.id))
    prefs = {}
    prefs["prefix"] = "!"
    f = open(dir+str(guild.id)+"/pref.json", "x")
    pref = json.dumps(prefs)
    f.write(pref)
    for x in guild.members:
        data = {}
        data["name"] = x.name
        data["id"] = x.id
        user = json.dumps(data)
        f = open(dir+str(guild.id)+"/"+str(x.id)+".json", "x")
        f.write(user)
        
@bot.event
async def on_member_join(member):
    data = {}
    data["name"] = member.name
    data["id"] = member.id
    user = json.dumps(data)
    f = open(dir+str(member.guild.id)+"/"+str(member.id)+".json", "x")
    f.write(user)
  
async def background_task():
    await bot.wait_until_ready()
    time = bot.get_channel(561686318501986314)
    while (not bot.is_closed()):
        cd = datetime.datetime.now() - datetime.timedelta(hours=4)
        await time.edit(name=cd.strftime("%I:%M:%S %p"))
        global logBuffer
        global errBuffer
        toChannel=bot.get_channel(497193723621277751)
        toSend = logBuffer.getvalue()
        toSend2 = errBuffer.getvalue()
        logBuffer.close()
        errBuffer.close()
        sys.stdout = logBuffer = io.StringIO()
        sys.stderr = errBuffer = io.StringIO()
        
        if toSend != "":
            await toChannel.send(toSend)
        if toSend2 != "":
            await toChannel.send(toSend2)
        await asyncio.sleep(.9)

if __name__ == '__main__':
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
    sys.stdout = logBuffer = io.StringIO()
    sys.stderr = errBuffer = io.StringIO()
    bot.loop.create_task(background_task())
    bot.run(tokens["discord"])