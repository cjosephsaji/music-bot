from discord.ext import commands
import discord
from music import Player
import os

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='-', intents=intents)

@bot.event
async def on_ready():
    print('LAME IS LAMIFYING')

async def setup():
    await bot.wait_until_ready()
    bot.add_cog(Player(bot))
    print('Music Listener Loaded!')

bot.loop.create_task(setup())

bot.run('TOKEN')
