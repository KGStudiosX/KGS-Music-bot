from youtube_dl.extractor import once
import loguru
import discord, os, time, json, asyncio, json, pafy, random, threading
from discord.ext import commands
from discord.utils import get
from vars import *
from funcs import *
from fastapi import FastAPI
from youtube_search import YoutubeSearch
from typing import TypedDict
from loguru import logger
from yaml import load, CLoader

__name__ = "KGS-Music-bot"

# ! Types
class Status(TypedDict):
    status: str
    type: str
    title: str
    author: str
    url: str

class Queue(TypedDict):
    type: str
    url: str
    title: str
    author: str
    full_name: str

class ServerState(TypedDict):
    vc: discord.VoiceClient
    queue: list[Queue]
    status: Status

# ! Initialized

logger.info("Starting...")
config = load(open("conf.yaml"), CLoader)

app = FastAPI()
intents = discord.Intents.all()
bot = commands.Bot(command_prefix = "url!", help_command=None, intents=intents)
client = discord.Client(intents=None)

servers: dict[int, ServerState] = {}
# ! Flask Section
@app.get("/") # TODO: Switch to static file serving
def index():
    print(f"Headers{request.headers}")
    return """
<style>
html, body{
    background: #212121;
    color: #fff;
}
</style>
<br>Документация по бота(api)</br>
<br></br>
<br>Содержание:
<br>ytdl
<br>play
<br>record
<br>recordq
<br></br>
<br></br>
<br>http://kgstudios.ddns.net:9090/play?url=<ваша опция></br>
<br>Метод: GET</br>
<br>На место <ваша опция надо вставить url для воспроизведения</br>
<br>Для воспроизведения прямой ссылки на файл(музыка, видео)</br>
<br></br>
<br>http://kgstudios.ddns.net:9090/ytdl?url=<ваша опция></br>
<br>Метод: GET</br>
<br>На место <ваша опция надо вставить url на видео ютуба</br>
<br>Для воспроизведения видео из ютуба</br>
<br></br>
<br>http://kgstudios.ddns.net:9090/record?r=<опция></br>
<br>Метод: GET</br>
<br>на место <опция> надо вставить либо main(Record dance radio) или phonk(Record phonk)</br>
<br>Для воспроизведения радио</br>
<br></br>
<br>http://kgstudios.ddns.net:9090/recordq?r=<опция></br>
<br>Метод: GET</br>
<br>Возврашает: json</br>
<br>на место <опция> надо вставить либо main(Record dance radio) или phonk(Record phonk)</br>
<br>Для получения что сейчас играет на радио</br>
<br></br>
<br>http://kgstudios.ddns.net:9090/status</br>
<br>Метод: GET</br>
<br>Возврашаает статус воспроизведения</br>
"""

@app.get("/status")
async def apistatus():
    print(f"Headers{request.headers}")
    if "niggers" == "niggers":
        return json.dumps(apistatusjson)
    else:
        return "Suck your fucking dick nigga"
@app.get("/queue")
async def apiqueue():
    return json.dumps(queuelist)

@app.get("/recordq")
def apirecordq():
    print(f"Headers{request.headers}")
    needradio = request.args.get('r')
    return json.dumps(parsejson(radiodb[needradio]))

@app.get("/play")
def apiplay():
    print(f"Headers{request.headers}")
    try:
        url = request.args.get('url')
        apistatusjson["playing"] = "true"
        apistatusjson["type"] = "url"
        apistatusjson["url"] = str(url)
        servers[ctx.guild.id]['vc'].play(discord.FFmpegPCMAudio(url), after=lambda e: on_complete_playing(e))
        return compjson
    except Exception as e:
        print(e)
        return errorjson

@app.get("/ytdl")
def apiytdl():
    print(f"Headers{request.headers}")
    if "niggers" == "niggers":
        try:
            url = request.args.get('url')
            video = pafy.new(url)
            apistatusjson["playing"] = "true"
            apistatusjson["type"] = "ytdl"
            apistatusjson["name"] = str(video.title)
            apistatusjson["author"] = str(video.author)
            apistatusjson["url"] = str(url)
            audio = video.getbestaudio()
            servers[ctx.guild.id]['vc'].play(discord.FFmpegPCMAudio(audio.url), after=lambda e: on_complete_playing(e))
            return compjson
        except Exception as e:
            print(e)
            return errorjson
    else:
        return errorjson

@app.get("/record")
def apirecord():
    print(f"Headers{request.headers}")
    if "niggers" == "niggers":
        try:
            needradio = request.args.get("r")
            servers[ctx.guild.id]['vc'].play(discord.FFmpegPCMAudio(radioldb[needradio]), after=lambda e: on_complete_playing(e))  
            return compjson
        except Exception as e:
            print(e)
            return errorjson
    else:
        return errorjson

@app.get("/stop")
def apistop():
    print(f"Headers{request.headers}")
    if "niggers" == "niggers":
        try:
            servers[ctx.guild.id]['vc'].stop()
            apistatusjson["playing"] = "false"
            apistatusjson["type"] = "idle"
            apistatusjson["url"] = "none"
            apistatusjson["name"] = "none"
            apistatusjson["author"] = "none"
            return compjson
        except:
            return errorjson
    else:
        return "Suck your fucking dick nigga"

@app.get("/pause")
def apipause():
    global pausestate
    global oldtypestatusjson
    print(f"Headers{request.headers}")
    if "niggers" == "niggers":
        try:
            if pausestate == False:
                servers[ctx.guild.id]['vc'].pause()
                pausestate = True
                apistatusjson["playing"] = "false"
                oldtypestatusjson = apistatusjson["type"]
                apistatusjson["type"] = "pause"
                return json.dumps({
                "result": "true", "playing": "false"
                })
            elif pausestate == True:
                servers[ctx.guild.id]['vc'].resume()
                pausestate = False
                apistatusjson["playing"] = "true"
                apistatusjson["type"] = oldtypestatusjson
                return json.dumps({
                "result": "true", "playing": "true"
                })
        except Exception as e:
            print(e)
            return errorjson
    else:
        return errorjson

def startapi():
    #app.run(port=9090, host="0.0.0.0")
    pass

#Disocrd py section

print("Intializating diskord.py")

def on_complete_playing(e, gid: int):
    print(e)
    global apistatusjson
    if servers[gid]['queue'] == []:
        print("Clearing api status...")
        servers[gid]['status']['status'] = 'idle'
    else:
        print("Is queue has a file to play?")
        if servers[gid]['queue'] == []:
            print("No!")
            print("Clearing api status...")
            apistatusjson["playing"] = "false"
            apistatusjson["type"] = "idle"
            apistatusjson["url"] = "none"
            apistatusjson["name"] = "none"
            apistatusjson["author"] = "none"
        else:
            print("Yes!")
            print("Playing file...")
            i = servers[gid]['queue'][0]
            servers[gid]['vc'].play(discord.FFmpegPCMAudio(process_url(i['url'], True)['playback_url']), after=lambda e: on_complete_playing(e, gid))
            del servers[gid]['queue'][0]


async def senddebug(ctx,message):
	if botdebug == True:
		ctx.send(message)
	if botdebug == False:
		print("Debug disabled.")

@bot.event
async def on_ready():
    print("Запуск api сервера...")
    startkey = random.randint(1, 9999)
    await bot.change_presence(activity=discord.Game(name="Starting api server"))
    flaskthread = threading.Thread(target=startapi)
    flaskthread.start()
    print("Бот готов!")
    await bot.change_presence(activity=discord.Game(name="Bot is ready! Start key: {}".format(startkey)))    
    #while True:
    #    await bot.change_presence(activity=discord.Game(name=f"{input()} | Start key: {startkey}"))   

def queuefor():
    global queuelist
    while True:
        for i in ["a"]:
            for i in queuelist:
                while True:
                    try:
                        servers[ctx.guild.id]['vc'].play(discord.FFmpegPCMAudio(i), after=lambda e: on_complete_playing(e))
                        break
                    except:
                        pass
            try:
                queuelist = []
            except:
                pass


#@bot.event #  TendingStream73: disable this for now
async def on_message(message):
    global userstate
    if (message.content.startswith('url!')):
        if message.guild.id == 676339202245525505:
            print("Command!") # Не обращайте внимание...
            for i in blockedusers:
                print(i)
                print(type(i))
                print(message.author.id)
                print(type(message.author.id))
                if message.author.id == int(i):
                    await message.channel.send("Ты заблокирован")
                    userstate = "blockedusers"
                    break
            if userstate != "blockedusers":
                try:
                    await bot.process_commands(message)
                except Exception as e:
                    print("Error!")
                    print(e)
            else:
                userstate = "none"
                print("User blocked!")   
        else:
            await message.channel.send("This bot cannot work with multiply servers.")
            await message.channel.send("Bot developer contacts:\nDiscord: TendingStream73#5806")    
            await message.channel.send("Этот бот не моэет работать с несколькими серверами.")
            await message.channel.send("Данные для контакта с разработчиком бота:\nDiscord: TendingStream73#5806")

    else:
        print("+-------------------------+")
        print(f"Server: {message.guild.name}")
        print(f"Channel: {message.channel.name}")
        print("Message author: {}".format(message.author.name))
        print("Message content: {}".format(message.content))
        print("AI Disabled.")
        print("+-------------------------+")
        if message.content.lower() == "meme" and message.channel.id == 856203481760530452:
            try:
                print("User sended meme!\nAdding meme to memedb...")
                await message.channel.send("Adding to meme db...")
                memedb = json.load(open("memedb.json"))
                memedb.append(str(message.attachments[0]))
                json.dump(memedb, open("memedb.json", "w"))
                await message.channel.send("Done!")
            except:
                await message.channel.send("Error!")
        else:
            print("Not a meme.")

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

@bot.command(aliases=["q"])
async def queue(ctx):
    if queuelist == []:
        await ctx.send("Nothing is playing now.")
    else:
        await ctx.send("Queue:")
        for i in queuelist:
            if i["type"] == "url":
                await ctx.send("Something url")
            if i["type"] == "ytdl":
                await ctx.send(f'{i["name"]} by {i["author"]}')

@bot.command(aliases=["eval", "exec"])
@commands.is_owner()
async def command_exec(ctx, *, commandexec=None):
    if False:
        await ctx.send("Ты не автор бота!")
    else:
        if commandexec == None:
            await ctx.send("""
                ```
                Using:
                url!exec python code
                ```
                """)
        else:
            try:
                outexec = eval(commandexec)
                await ctx.send(f"""
                    Out:
                    ```{outexec}```
                    """)
            except Exception as e:
                await ctx.send(f"""
                    ERROR!!!
                    ```{e}```
                    """)

class Casino:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def casino(ctx,something: int):
        await ctx.send(f"{something} Говоришь?")
        for i in range(1, 7):
            something2 = random.randint(1, 100)
        if something2 == something:
            await ctx.send("Ты выиграл!")
        else:
            await ctx.send("Ты проиграл!")

@bot.command()
async def block(ctx, userid):
    if ctx.author.id != 773136208439803934:
        await ctx.send("Ты не автор бота")
    else:
        if userid == 773136208439803934:
            await ctx.send("Error!")
        else:
            await ctx.send("Adding to blocked users...")
            blockedusers.append(userid)
            await ctx.send("Done!")

@bot.command()
async def unblock(ctx, userid):
    if ctx.author.id == 773136208439803934:
        await ctx.send("Unblocking...")
        for i in range(len(blockedusers)):
            if userid == blockedusers[i]:
                del blockedusers[0]
                await ctx.send("Done!")
                break
    else:
        await ctx.send("Ты не автор бота!")

class ProcessedURL(TypedDict):
    playback_url: str
    embed: discord.Embed
    q_entry: Queue

@logger.catch
def process_url(url: str, want_playback: bool) -> ProcessedURL:
    if url.startswith("https://youtube.com"):
        raise Exception("YT currently not supported")
    else:
        embed = discord.Embed(color=0x0080ff)
        embed.add_field(value=f"{url}", name="Now playing")
        ret: ProcessedURL = {
            "playback_url": url,
            "embed": embed,
            "q_entry": {
                "type": "direct",
                "url": url,
                "title": url,
                "full_name": url,
                "author": "Unknown"
            }
        }
        return ret

@bot.command(aliases=["p"])
async def play(ctx: commands.Context, *, url):
    if servers.get(ctx.guild.id, None) == None: # If there is no server...
        # Initialize it's state in servers dict
        servers[ctx.guild.id] = {'queue': [], 'status': {'status': 'idle'}}
    try:
        connected: discord.member.VoiceState = ctx.author.voice
        if connected != None:
            servers[ctx.guild.id]['vc'] = await connected.channel.connect()
        else:
            await ctx.send('Сначала зайди в войс.')
    except Exception as e:
        print(e)
    await ctx.send("CURRENTLY DISABLED")
    if antihack(url) == False:
        await ctx.send("Please check your url, as it may contain stuff that triggered anti-shell injection")
        return
    processed = process_url(url, len(servers[ctx.guild.id].get("queue", [])) == 0)
    if servers[ctx.guild.id]['status']['status'] != 'idle':
        servers[ctx.guild.id]['queue'].append(processed['q_entry'])
        print("added")
    else:
        logger.info(processed)
        servers[ctx.guild.id]['status']['type'] = processed['q_entry']['type']
        servers[ctx.guild.id]['status']['title'] = processed['q_entry']['title']
        servers[ctx.guild.id]['status']['author'] = processed['q_entry']['author']
        servers[ctx.guild.id]['status']['url'] = processed['q_entry']['url']
        servers[ctx.guild.id]['status']['status'] = 'playing'
        servers[ctx.guild.id]['vc'].play(discord.FFmpegPCMAudio(processed['playback_url']), after=lambda e: on_complete_playing(e, ctx.guild.id))
        await ctx.send(embed=processed['embed'])
    return
    await senddebug(ctx, "Проверка на попытку взлома севрера...")
    test = antihack(url)
    if test == False:
        await ctx.send("!!! WARNING !!!")
        await ctx.send("!!! ОБНАРУЖЕНА ПОПЫТКА ВЗЛОМА БОТА !!!")
    else:
        if checkyoutubeurl(url) == "ytdl": # TODO: Unify this
            await senddebug(ctx, "Получение url...")
            #os.system('yt-dlp --output /tmp/song.mp3 --force-overwrites -f 140 "{}"'.format(url))
            try:
                print("Trying to get audio url...")
                video = pafy.new(url)
                if queuelist == []:
                    print("Queue is empty.")
                    apistatusjson["playing"] = "true"
                    apistatusjson["type"] = "ytdl"
                    apistatusjson["name"] = str(video.title)
                    apistatusjson["author"] = str(video.author)
                    apistatusjson["url"] = str(url)
                    audio = video.getbestaudio()
                    print("Playing...")
                    queuefile = {
                        "playing": "true",
                        "type": "ytdl",
                        "name": video.title,
                        "author": video.author,
                        "url": url,
                        "playurl": audio.url
                    }
                    queuelist.append(queuefile)
                    #await ctx.send("Воспроизведение...")
                    servers[ctx.guild.id]['vc'].play(discord.FFmpegPCMAudio(audio.url), after=lambda e: on_complete_playing(e))
                    _embed = discord.Embed(color=0x0080ff)
                    _embed.add_field(value=f"[{video.title} by {video.author}]({url})", name="Will now play")
                    _embed.set_image(url=video.thumb)
                    await ctx.send(embed=_embed)
                else:
                    audio = video.getbestaudio()
                    queuefile = {
                        "playing": "true",
                        "type": "ytdl",
                        "name": video.title,
                        "author": video.author,
                        "url": url,
                        "playurl": audio.url
                    }
                    queuelist.append(queuefile)
            except:
                print("This is not a url")
                print("Trying to search...")
                videosSearch = VideosSearch(url, limit = 1)
                videosResult = await videosSearch.next()
                vidurl = videosResult["result"][0]['link']
                video = pafy.new(vidurl)
                print("Getting audio url...")
                if queuelist == []:
                    print("Queue is empty.")
                    apistatusjson["playing"] = "true"
                    apistatusjson["type"] = "ytdl"
                    apistatusjson["name"] = str(video.title)
                    apistatusjson["author"] = str(video.author)
                    apistatusjson["url"] = str(vidurl)
                    audio = video.getbestaudio()
                    print("Playing...")
                    #await ctx.send("Воспроизведение...")
                    queuefile = {
                        "playing": "true",
                        "type": "ytdl",
                        "name": video.title,
                        "author": video.author,
                        "url": vidurl,
                        "playurl": audio.url
                    }
                    servers[ctx.guild.id]['vc'].play(discord.FFmpegPCMAudio(audio.url), after=lambda e: on_complete_playing(e))
                    queuelist.append(queuefile)
                    _embed = discord.Embed(color=0x0080ff)
                    _embed.add_field(value=f"[{video.title} by {video.author}]({vidurl})", name="Will now play")
                    _embed.set_image(url=video.thumb)
                    await ctx.send(embed=_embed)
                else:
                    audio = video.getbestaudio()
                    queuefile = {
                        "playing": "true",
                        "type": "ytdl",
                        "name": video.title,
                        "author": video.author,
                        "url": vidurl,
                        "playurl": audio.url
                    }
                    queuelist.append(queuefile)
                    _embed = discord.Embed(color=0x0080ff)
                    _embed.add_field(value=f"[{video.title} by {video.author}]({vidurl})", name="Added to queue!")
                    _embed.set_image(url=video.thumb)
                    await ctx.send(embed=_embed)
        elif checkyoutubeurl(url) == "playlist":
            print("Getting videos from playlist...")

        else:
            connected = ctx.author.voice
            # grab the user who sent the command
            user=ctx.message.author
            voice_channel=user.voice.channel
            channel=None
            apistatusjson["playing"] = "true"
            apistatusjson["type"] = "url"
            apistatusjson["url"] = str(url)
            # only play music if user is in a voice channel
            if voice_channel!= None:
                if queuelist == []:
                    queuefile = {
                        "playing": "true",
                        "type": "url",
                        "name": "none",
                        "author": "none",
                        "url": url,
                        "playurl": url
                    }
                    queuelist.append(queuefile)
                    servers[ctx.guild.id]['vc'].play(discord.FFmpegPCMAudio(url), after=lambda e: on_complete_playing(e))
                else:
                    queuefile = {
                        "playing": "true",
                        "type": "url",
                        "name": "none",
                        "author": "none",
                        "url": url,
                        "playurl": url
                    }
                    queuelist.append(queuefile)
            else:
                await ctx.send('Сначала войди в войс.')

@bot.command(aliases=["np"])
async def nowplaying(ctx):
    if apistatusjson["type"] == "ytdl":
        _embed = discord.Embed(title=apistatusjson["name"], description=apistatusjson["author"], color=0x0080ff)
        await ctx.send(embed=_embed)
    elif apistatusjson["type"] == "url":
        await ctx.send("Something playing")
    elif apistatusjson["type"] == "pause":
        await ctx.send("Music on pause")
    elif apistatusjson["type"] == "idle":
        await ctx.send("Nothing is playing")
    elif apistatusjson["type"] == "radio":
        await ctx.send("Radio is playing now.")

@bot.command()
async def join(ctx: discord.ext.commands.Context):
    if servers.get(ctx.guild.id, None) == None: # If there is no server...
        # Initialize it's state in servers dict
        servers[ctx.guild.id] = {}
    connected: discord.member.VoiceState = ctx.author.voice
    if connected != None:
        servers[ctx.guild.id]['vc'] = await connected.channel.connect()
    else:
        await ctx.send('Сначала зайди в войс.')

@bot.command()
async def leave(ctx):
    await ctx.send("Ок, выхожу...")
    await servers[ctx.guild.id]['vc'].disconnect()

@bot.command()
async def pause(ctx):
    global pausestate
    global oldtypestatusjson
    try:
        if pausestate == False:
            servers[ctx.guild.id]['vc'].pause()
            pausestate = True
            apistatusjson["playing"] = "false"
            oldtypestatusjson = apistatusjson["type"]
            apistatusjson["type"] = "pause"
        elif pausestate == True:
            servers[ctx.guild.id]['vc'].resume()
            pausestate = False
            apistatusjson["playing"] = "true"
            apistatusjson["type"] = oldtypestatusjson
    except Exception as e:
        print(e)
        await ctx.send("Error!")

@bot.command(aliases=["skip"])
async def stop(ctx):
    apistatusjson["playing"] = "false"
    apistatusjson["type"] = "idle"
    apistatusjson["url"] = "none"
    apistatusjson["name"] = "none"
    apistatusjson["author"] = "none"
    servers[ctx.guild.id]['vc'].stop()

@bot.command()
async def hello(ctx):
    await ctx.send("Привет!")

@bot.command()
async def hi(ctx):
    await ctx.send("Привет!")


async def ytdl(ctx, *, url):
    await ctx.send("Command disabled!")
    raise RuntimeError("Command disabled!")
    await senddebug(ctx, "Проверка на попытку взлома севрера...")
    test = antihack(url)
    if test == False:
        await ctx.send("!!! WARNING !!!")
        await ctx.send("!!! ОБНАРУЖЕНА ПОПЫТКА ВЗЛОМА СЕРВЕРА !!!")
    else:
        await senddebug(ctx, "Получение url...")
        #os.system('yt-dlp --output /tmp/song.mp3 --force-overwrites -f 140 "{}"'.format(url))
        try:
            print("Trying to get audio url...")
            video = pafy.new(url)
            apistatusjson["playing"] = "true"
            apistatusjson["type"] = "ytdl"
            apistatusjson["name"] = str(video.title)
            apistatusjson["author"] = str(video.author)
            apistatusjson["url"] = str(url)
            audio = video.getbestaudio()
            print("Playing...")
            queuefile = {}
            await ctx.send("Воспроизведение...")
            servers[ctx.guild.id]['vc'].play(discord.FFmpegPCMAudio(audio.url), after=lambda e: on_complete_playing(e))
        except:
            print("This is not a url")
            print("Trying to search...")
            videosSearch = VideosSearch(url, limit = 1)
            videosResult = await videosSearch.next()
            vidurl = videosResult["result"][0]['link']
            print("Getting audio url...")
            video = pafy.new(vidurl)
            apistatusjson["playing"] = "true"
            apistatusjson["type"] = "ytdl"
            apistatusjson["name"] = str(video.title)
            apistatusjson["author"] = str(video.author)
            apistatusjson["url"] = str(url)
            audio = video.getbestaudio()
            print("Playing...")
            await ctx.send("Воспроизведение...")
            servers[ctx.guild.id]['vc'].play(discord.FFmpegPCMAudio(audio.url), after=lambda e: on_complete_playing(e))


@bot.command()
async def record(ctx, needradio="main"):
    global currentradio
    connected = ctx.author.voice
    # grab the user who sent the command
    user=ctx.message.author
    voice_channel=user.voice.channel
    channel=None
    apistatusjson["playing"] = "true"
    apistatusjson["type"] = "radio"
    # only play music if user is in a voice channel
    if voice_channel!= None:
        servers[ctx.guild.id]['vc'].play(discord.FFmpegPCMAudio(radioldb[needradio]), after=lambda e: on_complete_playing(e))
        currentradio=needradio
    else:
        await ctx.send('Сначала войди в войс.')


@bot.command()
async def nightride(ctx):
    connected = ctx.author.voice
    # grab the user who sent the command
    user=ctx.message.author
    voice_channel=user.voice.channel
    channel=None
    apistatusjson["playing"] = "true"
    apistatusjson["type"] = "radio"
    # only play music if user is in a voice channel
    if voice_channel!= None:
        servers[ctx.guild.id]['vc'].play(discord.FFmpegPCMAudio("https://stream.nightride.fm/nightride.m4a"), after=lambda e: on_complete_playing(e))
    else:
        await ctx.send('Сначала войди в войс.')

@bot.command()
async def radio(ctx, c1, c2):
    radio_list = json.load(open("radio.json"))
    servers[ctx.guild.id]['vc'].play(discord.FFmpegPCMAudio(radio_list[c1][c2]), after=lambda e: on_complete_playing(e))

@bot.command()
async def radio_list(ctx):
    radio_list = json.load(open("radio.json"))
    await ctx.send(radio_list)

@bot.command()
async def recordq(ctx):
    # await ctx.send("Парсинг, пожалуйста подождите...")
    tracklist = parsejson(radiodb[currentradio])
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

@bot.command()
async def playfile(ctx):
    url = ctx.message.attachments[0]
    print(url)
    await senddebug(ctx, "Проверка на попытку взлома севрера...")
    test = antihack(str(url))
    if test == False:
        await ctx.send("!!! WARNING !!!")
        await ctx.send("!!! ОБНАРУЖЕНА ПОПЫТКА ВЗЛОМА СЕРВЕРА !!!")
    else:
        connected = ctx.author.voice
        # grab the user who sent the command
        user=ctx.message.author
        voice_channel=user.voice.channel
        channel=None
        apistatusjson["playing"] = "true"
        apistatusjson["type"] = "url"
        apistatusjson["url"] = str(url)
        # only play music if user is in a voice channel
        if voice_channel!= None:
            if queuelist == []:
                queuefile = {
                    "playing": "true",
                    "type": "file",
                    "name": "none",
                    "author": "none",
                    "url": url,
                    "playurl": url
                }
                queuelist.append(queuefile)
                servers[ctx.guild.id]['vc'].play(discord.FFmpegPCMAudio(url), after=lambda e: on_complete_playing(e))
            else:
                queuefile = {
                    "playing": "true",
                    "type": "file",
                    "name": "none",
                    "author": "none",
                    "url": url,
                    "playurl": url
                }
                queuelist.append(queuefile)
        else:
            await ctx.send('Сначала войди в войс.')

@bot.command()
async def getmeme(ctx):
    memedb = json.load(open("memedb.json"))
    memefile = random.choice(memedb)
    await ctx.send(memefile)

@bot.command()
async def addmeme(ctx, url=None):
    await ctx.send("Adding to memedb...")
    try:
        print("Checking for attachments...")
        if ctx.message.attachments != []:
            print("This is a attachement!")
            print("Adding to memedb...")
            memedb = json.load(open("memedb.json"))
            memedb.append(str(ctx.message.attachments[0]))
            json.dump(memedb, open("memedb.json", "w"))
            await ctx.send("Done!")
        else:
            print("Not a attachement.\nTrying to add as url...")
            if url != None:
                print("This is url!\nTrying to add...")
                memedb = json.load(open("memedb.json"))
                memedb.append(url)
                json.dump(memedb, open("memedb.json", "w"))
                await ctx.send("Done!")
            else:
                await ctx.send("Error!: You're sended nothing.")
    except Exception as e:
        print("ERR!: {}".format(e))
        await ctx.send("Error!: {}".format(e))

# Start cogs section

print("Intializating cogs...")
#bot.load_extension("cogs.casino") # TODO: This has now become a corountine

# End cogs section
 
print("Starting bot...")

bot.run(config['token'])
