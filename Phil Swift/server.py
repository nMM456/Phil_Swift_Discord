import discord
from discord.ext import commands
import asyncio
import sys
import io
import datetime

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
                      #continued
                    ]

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
  
async def background_task():
    await bot.wait_until_ready()
    while (not bot.is_closed()):
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
        await asyncio.sleep(1)

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
    bot.run('key_here')