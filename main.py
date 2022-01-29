import discord
from discord.ext import commands
import time
import asyncio
from discord.utils import get
#from youtube_dl import YoutubeDL
import json
import os
from funcs import *

bot = commands.Bot(command_prefix = "url2!", help_command=None)
client = discord.Client()

@bot.event
async def on_ready():
    print("Бот готов!")

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if (message.content.startswith('url2!')):
        print("Command!") # Не обращайте внимание.. 
        pass

@bot.command()
async def help(ctx):
    _embed = discord.Embed(title="Help", description="List of commands", color=0x0080ff)
    _embed.add_field(name="help", value="Shows this message.", inline=True)
    _embed.add_field(name="join", value="Join voice channel.", inline=True)
    _embed.add_field(name="leave", value="Leave voice channel.", inline=True)
    _embed.add_field(name="play [URL...]", value="Starts playing song, provided in url.", inline=True)
    _embed.add_field(name="pause", value="Pause current song.", inline=True)
    _embed.add_field(name="resume", value="Resume current song.", inline=True)
    _embed.add_field(name="stop", value="Stops current song.", inline=True)
    _embed.add_field(name="record", value='Starts playing "Radio Record" (Russia).', inline=True)
    _embed.add_field(name="ytdl", value='Playing video from youtube.', inline=True)
    _embed.add_field(name="recordq", value='Current track playing in Radio Record.', inline=True)
    _embed.add_field(name="changelog", value='Bot changelog.', inline=False)
    await ctx.send(content="Syntax:\n    url!<command> [Options...]\n\nType url!help [Command...] to get more info of a command.\nYou can also type url!help [Category...] for more info of a category.", embed=_embed)

@bot.command()
async def play(ctx, *, url):
#    await ctx.send("Проверка на попытку взлома севрера...")
    test = antihack(url)
    if test == False:
        await ctx.send("!!! WARNING !!!")
        await ctx.send("!!! ОБНАРУЖЕНА ПОПЫТКА ВЗЛОМА СЕРВЕРА !!!")
    else:
        connected = ctx.author.voice
        # grab the user who sent the command
        user=ctx.message.author
        voice_channel=user.voice.channel
        channel=None
        # only play music if user is in a voice channel
        if voice_channel!= None:
            vc.play(discord.FFmpegPCMAudio(url), after=lambda e: print('done', e))
        else:
            await ctx.send('Сначала войди в войс.')

@bot.command()
async def join(ctx):
    global vc
    connected = ctx.author.voice
    if connected != None:
        vc = await connected.channel.connect()
    else:
        await ctx.send('Сначала зайди в войс.')

@bot.command()
async def leave(ctx):
    await ctx.send("Ок, выхожу...")
    await vc.disconnect()

@bot.command()
async def pause(ctx):
    vc.pause()

@bot.command()
async def resume(ctx):
    vc.resume()

@bot.command()
async def stop(ctx):
    vc.stop()

@bot.command()
async def ytdl(ctx, *, url):
#    await ctx.send("Проверка на попытку взлома севрера...")
    test = antihack(url)
    if test == False:
        await ctx.send("!!! WARNING !!!")
        await ctx.send("!!! ОБНАРУЖЕНА ПОПЫТКА ВЗЛОМА СЕРВЕРА !!!")
    else:
        await ctx.send("Загрузка...")
        os.system('yt-dlp --output /tmp/song.mp3 --force-overwrites -f 140 "{}"'.format(url))
        await ctx.send("Воспроизведение...")
        vc.play(discord.FFmpegPCMAudio("/tmp/song.mp3"), after=lambda e: print('done', e))


@bot.command()
async def record(ctx):
    connected = ctx.author.voice
    # grab the user who sent the command
    user=ctx.message.author
    voice_channel=user.voice.channel
    channel=None
    # only play music if user is in a voice channel
    if voice_channel!= None:
        vc.play(discord.FFmpegPCMAudio("http://radiorecord.hostingradio.ru/rr_main96.aacp"), after=lambda e: print('done', e))
    else:
        await ctx.send('Сначала войди в войс.')


@bot.command()
async def nightride(ctx):
    connected = ctx.author.voice
    # grab the user who sent the command
    user=ctx.message.author
    voice_channel=user.voice.channel
    channel=None
    # only play music if user is in a voice channel
    if voice_channel!= None:
        vc.play(discord.FFmpegPCMAudio("https://stream.nightride.fm/nightride.m4a"), after=lambda e: print('done', e))
    else:
        await ctx.send('Сначала войди в войс.')

@bot.command()
async def radio(ctx, c1, c2):
    radio_list = json.load(open("radio.json"))
    vc.play(discord.FFmpegPCMAudio(radio_list[c1][c2]), after=lambda e: print('done', e))

@bot.command()
async def radio_list(ctx):
    radio_list = json.load(open("radio.json"))
    await ctx.send(radio_list)

@bot.command()
async def recordq(ctx):
    # await ctx.send("Парсинг, пожалуйста подождите...")
    tracklist = parsejson()
    # await ctx.send("Создание embed...")
    # _embed = discord.Embed(title="Song name", description="Что сейчас играет?", color=0x0080ff)
    _embed = discord.Embed(title=tracklist["song"], description=tracklist["artist"], color=0x0080ff)
    # _embed.add_field(name=tracklist["artist"], value=tracklist["song"], inline=True)
    await ctx.send(embed=_embed)

@bot.command()
async def changelog(ctx):
    _embed = discord.Embed(title="Bot changelog", description="Bot changelog", color=0x0080ff)
    changelogfile = json.load(open("changelog.json"))
    for i in changelogfile:
        _embed.add_field(name=i["ver"], value=i["changelog"], inline=True)
    await ctx.send(embed=_embed)


bot.run('Token here')
