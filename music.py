from discord.ext import commands
import youtube_dl
import discord
import random
import pafy


class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.song_queue = {}
        self.setup()

    def setup(self):
        for guild in self.bot.guilds:
            self.song_queue[guild.id] = []


    async def check_queue(self, ctx):
        if len(self.song_queue[ctx.guild.id]) > 0:
            await self.play_song(ctx, self.song_queue[ctx.guild.id][0])
            self.song_queue[ctx.guild.id].pop(0)

    async def search_song(self, amount, song, get_url=False):
        info = await self.bot.loop.run_in_executor(None,lambda:youtube_dl.YoutubeDL({"format" : "bestaudio", "quiet" : True}).extract_info(f"ytsearch{amount}:{song}", download=False, ie_key='YoutubeSearch'))
        if len(info["entries"]) == 0: return None

        return [entry["webpage_url"] for entry in info["entries"]] if get_url else info

    async def play_song(self, ctx, song):
        url = pafy.new(song).getbestaudio().url
        ctx.voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(url)), after=lambda error: self.bot.loop.create_task(self.check_queue(ctx)))
        ctx.voice_client.source.volume = 0.5

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            replies = ['Bruh WTF ARE YOU DOING 🤦‍♂️\nJOIN THE CHANNEL FIRST DOOMBAZ!', 'USE YOUR FRICKING BRAINS AND JOIN THE CHANNEL FIRST IDIOT', 'IS YOUR BRAIN TURNED OFF OR WHAT? JOIN THE FRICKING CHANNEL']
            return await ctx.send(embed=discord.Embed(title='DOOMBAZ', description=random.choice(replies), color=0xFF0000))
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
        
        await ctx.author.voice.channel.connect()


    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client is not None:
            return await ctx.voice_client.disconnect()

        await ctx.send(embed=discord.Embed(title='URGH',description="I'M NOT CONNECTED TO THE VOICE CHANNEL DOOMBAZ", color=0xFF0000))

    @commands.command()
    async def play(self, ctx, *, song=None):
        if song is None:
            return await ctx.send("WHAT'S THE FRICKING SONG YOU IDIOT!")
        if ctx.voice_client is None:
            try:
                await ctx.author.voice.channel.connect()
            except:
                replies = ['Bruh WTF ARE YOU DOING 🤦‍♂️\nJOIN THE CHANNEL FIRST DOOMBAZ!', 'USE YOUR FRICKING BRAINS AND JOIN THE CHANNEL FIRST IDIOT', 'IS YOUR BRAIN TURNED OFF OR WHAT? JOIN THE FRICKING CHANNEL']
                return await ctx.send(embed=discord.Embed(title='DOOMBAZ', description=random.choice(replies), color=0xFF0000))

        if not("youtube.com/watch?" in song or "https://youtu.be/" in song):
            await ctx.send(embed=discord.Embed(title="Searching...", description="Gimme a sec I'm searching for the song", color=0x7800FF))
            result = await self.search_song(1, song, get_url=True)

            if result is None:
                return await ctx.send(embed=discord.Embed(title='Search Failed', description="Nig, you sure that's the right name of the song?", color=0xFF0000))

            song = result[0]

        if ctx.voice_client.source is not None:
            queue_len = len(self.song_queue[ctx.guild.id])

            if queue_len < 10:
                self.song_queue[ctx.guild.id].append(song)
                return await ctx.send(embed=discord.Embed(title='Queue', description=f"Song has been added to the queue :thumbsup:\nPosition :arrow_right: {queue_len+1}", color=0x7800FF))

        await self.play_song(ctx, song)
        await ctx.send(f"Now playing: {song}")


    @commands.command()
    async def search(self, ctx, *, song=None):
        if song is None: return await ctx.send("WHAT 👏 IS 👏 THE 👏 FRICKING SONG")

        await ctx.send(embed=discord.Embed(title="Searching...", description="Gimme a sec I'm searching for the song", color=0x7800FF))

        info = await self.search_song(5, song)

        embed = discord.Embed(title=f"Results for '{song}':", description="*You can use these URL's to play an exact song if the one you want isn't the first result.*\n", color=0x7800FF)
        
        amount = 0
        for entry in info["entries"]:
            embed.description += f"[{entry['title']}]({entry['webpage_url']})\n"
            amount += 1

        embed.set_footer(text=f"Displaying the first {amount} results.")
        await ctx.send(embed=embed)


    @commands.command()
    async def queue(self, ctx): # display the current guilds queue
        if len(self.song_queue[ctx.guild.id]) == 0:
            return await ctx.send(embed=discord.Embed(title='Queue',description="No queue at the moment", color=0x7800FF))

        embed = discord.Embed(title="Queue", description="", color=0x7800FF)
        i = 1
        for url in self.song_queue[ctx.guild.id]:
            embed.description += f"{i}) {url}\n"

            i += 1

        embed.set_footer(text="ONCE A DUMBASS, ALWAYS A DUMBASS")
        await ctx.send(embed=embed)


    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send(embed=discord.Embed(title='URGH THIS FRICKIN DUMBASS',description="ARE YOU DEAF OR WHAT? CAN'T YOU HEAR IF I'M PLAYING A SONG OR NOT?", color=0xFF0000))

        if ctx.author.voice is None:
            replies = ['Bruh WTF ARE YOU DOING 🤦‍♂️\nJOIN THE CHANNEL FIRST DOOMBAZ!', 'USE YOUR FRICKING BRAINS AND JOIN THE CHANNEL FIRST IDIOT', 'IS YOUR BRAIN TURNED OFF OR WHAT? JOIN THE FRICKING CHANNEL']
            return await ctx.send(embed=discord.Embed(title='DOOMBAZ', description=random.choice(replies), color=0xFF0000))

        if ctx.author.voice.channel.id != ctx.voice_client.channel.id:
            return await ctx.send(embed=discord.Embed(title='DOOMBAZ', description=random.choice(replies), color=0xFF0000))

        ctx.voice_client.stop()


    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client.is_paused():
            return await ctx.send(embed=discord.Embed(title="BRUHHH", description="I'M NOT EVEN PLAYING THE SONG YOU DUMBASS", color=0xFF0000))

        ctx.voice_client.pause()
        await ctx.send(embed=discord.Embed(title="Paused Song", color=0x7800FF))

    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send(embed=discord.Embed(title="URGH THIS GUY", description="DO YOU EVEN HAVE A BRAIN? HUH? I'M ASKING YOU", color=0xFF0000))

        if not ctx.voice_client.is_paused():
            return await ctx.send(embed=discord.Embed(title="BRAIN 💥", description="THIS GUY IS DEAF, LEGIT", color=0xFF0000))
        
        ctx.voice_client.resume()
        await ctx.send(embed=discord.Embed(title="Resumed Song", color=0x7800FF))

    @commands.command()
    async def stop(self, ctx):
        self.song_queue[ctx.guild.id].clear()
        await ctx.voice_client.disconnect()


