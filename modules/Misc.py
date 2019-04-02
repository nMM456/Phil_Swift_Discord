import discord
from discord.ext import commands
import asyncio
import re
import requests
import urllib.request

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    #commands for this module go here, in this class
    @commands.command()
    async def help(self, ctx, *commands : str):
        """Shows this message."""
        bot = self.bot
        destination = ctx.message.author if bot.pm_help else ctx.message.channel
        pageNum = 1
        if len(commands) == 1:
            try:
                pageNum = int(commands[0])
                commands = []
            except:
                pass
        pageNum -=1
        
        _mentions_transforms = {'@everyone': '@\u200beveryone','@here': '@\u200bhere'}
        _mention_pattern = re.compile('|'.join(_mentions_transforms.keys()))

        def repl(obj):
            return _mentions_transforms.get(obj.group(0), '')

        # help by itself just lists our own commands.
        if len(commands) == 0:
            pages = await bot.formatter.format_help_for(ctx, bot)
        elif len(commands) == 1:
            # try to see if it is a cog name
            name = _mention_pattern.sub(repl, commands[0])
            command = None
            if name in bot.cogs:
                command = bot.cogs[name]
            else:
                command = bot.all_commands.get(name)
                if command is None:
                    await destination.send(bot.command_not_found.format(name))
                    return

            pages = await bot.formatter.format_help_for(ctx, command)
        else:
            name = _mention_pattern.sub(repl, commands[0])
            command = bot.all_commands.get(name)
            if command is None:
                await destination.send(bot.command_not_found.format(name))
                return

            for key in commands[1:]:
                try:
                    key = _mention_pattern.sub(repl, key)
                    command = command.all_commands.get(key)
                    if command is None:
                        await destination.send(bot.command_not_found.format(key))
                        return
                except AttributeError:
                    await destination.send(bot.command_has_no_subcommands.format(command, key))
                    return

            pages = await bot.formatter.format_help_for(ctx, command)

        if bot.pm_help is None:
            characters = sum(map(len, pages))
            # modify destination based on length of pages.
            if characters > 1000:
                destination = ctx.message.author


        myEmbed = discord.Embed(title="Phil Swift Help", description=str(pages[pageNum]))
        myEmbed.set_footer(text="Page " + str(pageNum+1) + "/" + str(len(pages)))

        await ctx.send(embed=myEmbed)

    @commands.command()
    async def JAKE(self, ctx):
        """JAKE IS MAD BECAUSE HE IS BAD"""
        await ctx.send('J <:LUL:421063402094329858> K E')
        
    @commands.command()
    async def kanye(self, ctx):
        """Thank you Kanye, very cool!"""
        url = 'https://api.kanye.rest/'
        url_get = requests.get(url)
        data = url_get.json()
        await ctx.send('"'+data["quote"]+'"')
        
    @commands.command()
    async def getServerID(self, ctx):
        """Get ID of current server"""
        await ctx.send(ctx.guild.id)
    
    @commands.command()
    async def getUserID(self, ctx):
        """Get ID of yourself."""
        await ctx.send(ctx.author.id)
    
#Not part of class:
def setup(bot):
    bot.add_cog(Misc(bot))
