from discord.ext import commands
import datetime
from discord.ext.commands.errors import CommandNotFound
import requests
from time import sleep
from discord_components import DiscordComponents, Button, ButtonStyle
from discord.ext.commands import has_permissions, MissingPermissions
import discord
from music import Player
import os

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='-', intents=intents)
bot.remove_command('help')

@bot.event
async def on_ready():
    print('LAME IS LAMIFYING')

async def setup():
    await bot.wait_until_ready()
    bot.add_cog(Player(bot))
    print('Music Listener Loaded!')

bot.loop.create_task(setup())

bot.run('ODQ3MTI3NDE0NjU1ODExNjI0.YK5i4g.AS17JhYU64PLQ1-Z4wb62A2rbpw')
