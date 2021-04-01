# -*- coding: utf-8 -*-
import discord, asyncio, os, time, random, images
from discord.ext import commands
from r6stats import R6Stats
import lyrics, config
from classes import *

bot = commands.Bot(command_prefix = '.')
#Global variable
bot.COLOR_RGB = [(230, 70, 30), (107, 62, 50), (237, 240, 238), (247, 250, 75), (84, 252, 255), (138, 112, 255), (255, 20, 126)]
bot.lyricsMethod = 1
#player id for the friends only stats
bot.def_playerList = {
    'BenGorr':'044e7ff2-67d6-4706-8bfd-b1503af00b9b', 'n1.Pigu':'bfaf9738-2401-4d5c-918b-c460b8760cdc',
    'LilCh33tos':'8def768d-dae1-4c06-9e02-7e1b6d8b15f0', 'JellyF1shBean':'c9bb4e6b-1a3e-4ba0-95db-7af886f2916f'
    }
bot.keywords = []

@bot.event
async def on_ready():
    print('Logged on as {0}!'.format(bot.user))
    updateBotKeywords()

def isBen(ctx):
    return ctx.author.id == 171175305036300299

@bot.command(aliases=['r'], help="Restart bot (only owner)")
@commands.check(isBen)
async def restart(ctx):
    try:
        await ctx.send("Restarting :)")
        await bot.close()
    except:
        pass
    finally:
        os.system("python run.py")

@bot.command(help="hi??")
async def hi(ctx):
    await ctx.send(f"Hi! {ctx.author.mention}")

@bot.command(help="??")
async def bye(ctx):
    await ctx.send(f"Bye! {ctx.author.mention}")

@bot.command(help="Check rainbow six siege stats. Usage: .r6 name")
async def r6(ctx, name, platform="pc"):
    player = R6Stats(name, platform)
    #print(player.data)
    if (not player.genericStats):
        await ctx.send(f"Couldn't find user: {name}")
        return
    else:
        rank = player.statsAsia['rank']
        color = discord.Color.default()
        if (rank >= 1 and rank <= 5): #copper
            color = discord.Color.from_rgb(*bot.COLOR_RGB[0])
        elif (rank <= 10): #bronze
            color = discord.Color.from_rgb(*bot.COLOR_RGB[1])
        elif (rank <= 15): #silver
            color = discord.Color.from_rgb(*bot.COLOR_RGB[2])
        elif (rank <= 18): #gold
            color = discord.Color.from_rgb(*bot.COLOR_RGB[3])
        elif (rank <= 21): #plat
            color = discord.Color.from_rgb(*bot.COLOR_RGB[4])
        elif (rank == 22): #diamond
            color = discord.Color.from_rgb(*bot.COLOR_RGB[5])
        elif (rank == 23): #champion
            color = discord.Color.from_rgb(*bot.COLOR_RGB[6])

        embed = discord.Embed(
            title = f"Rank: {player.statsAsia['rank_text']}",
            description = f"Level: {player.level}",
            color = color
        )
        if (player.statsAsia['rank'] != 23):
            linkRep = {'ranks': 'rank-imgs', 'svg': 'png'}
            rank_url = player.statsAsia['rank_image']
            for i, j in linkRep.items():
                rank_url = rank_url.replace(i, j)
        else:
            rank_url = f"https://tabstats.com/images/r6/ranks/?rank=21&champ={player.statsAsia['champions_rank_position']}"
        icon_url = player.genericStats['avatar_url_146']
        embed.set_thumbnail(url=rank_url)
        embed.set_author(name=player.genericStats['username'], icon_url=icon_url)
        embed.add_field(name="Current MMR: ", value=f"{player.statsAsia['mmr']}", inline=False)
        embed.add_field(name="Ranked KD: ", value=player.statsAsia['kd'], inline=True)
        if player.statsAsia['losses'] == 0: losses = 1
        else: losses = player.statsAsia['losses']
        embed.add_field(name="Wins/Losses: ", value="Wins: {}\n Losses: {}\n W/L: {}".format(player.statsAsia['wins'],
                player.statsAsia['losses'],
                "{:.2f}".format(player.statsAsia['wins'] / losses)),
                inline=True
            )
        #embed.add_field(name="Casual KD: ", value="{:.2f}".format(player.genericStats['stats']['queue']['casual']['kd']), inline=True)
        embed.add_field(name="Overall KD: ", value="{:.2f}".format(player.genericStats['stats']['general']['kd']), inline=False)
        await ctx.send(embed=embed)

@bot.command(help="r6 state with specific players")
async def us(ctx, platform="pc"):
    players = []
    for username in bot.def_playerList.keys():
        try:
            player = R6Stats(username, platform, generic=False)
        except Exception as e:
            await ctx.send("API is broken D:")
            print(e)
            return
        if (not player.seasonalStats):
            await ctx.send(f"Couldn't find user: {username}")
            continue
        else:
            #print(player.data['ranked']['mmr'])
            player.statsAsia['p_name'] = player.username
            players.append(player.statsAsia)
    players = sorted(players, key = lambda i: i['mmr'], reverse=True)
    desc = ""
    for i, e in enumerate(players):
        desc = desc + f"#{i+1} {e['p_name']} Rank: {e['rank_text']}({e['mmr']}) \n"
    # for i in range(len(players)):
    #     desc = desc + f"#{i+1} {players[i]['profile']['p_name']} Rank: {rankList[players[i]['ranked']['rank']]}({players[i]['mmr']}) \n"

    embed = discord.Embed(
        title = "Ranking Among Us:",
        description = desc
    )
    linkRep = {'ranks': 'rank-imgs', 'svg': 'png'}
    rank_url = players[0]['rank_image']
    for i, j in linkRep.items():
        rank_url = rank_url.replace(i, j)
    embed.set_thumbnail(url=rank_url)
    await ctx.send(embed=embed)

@bot.command(help="kekw, try it")
async def kekw(ctx):
    if ctx.author == 318221117640671234:
        await ctx.send(kekw + "Nope.")
        return
    kekw = "<:7529_KEKW:734986562030403666> "
    msgs = []
    j = [i for i in range(1, 6)]# + [i for i in range(4, 0, -1)]
    for i in j:
        msgs.append(await ctx.send(i*kekw))
    #print("sleeping for 3 secs")
    #await asyncio.sleep(3.0)
    for m in msgs:
        await m.delete()
    await ctx.message.delete()

def is_bot(m):
    return m.author == bot.user

@bot.command(help="Purge bot messages, Usage: .purge limit")
@commands.check(isBen)
async def purge(ctx, limit=100):
    deleted = await ctx.channel.purge(limit=limit, check=is_bot)
    await ctx.channel.send('Deleted {} message(s)'.format(len(deleted)))

@bot.command(help="Clear messages, Usage: .clear limit")
async def clear(ctx, limit=100):
    deleted = await ctx.channel.purge(limit=limit)
    await ctx.channel.send('Cleared {} message(s)'.format(len(deleted)))

@bot.command()
async def fuck(ctx, *, name="you"):
    await ctx.send("Fuck " + name)
    await ctx.message.delete()

@bot.command(aliases=['reee', 'reeee', 'reeeee', 'reeeeee'])
async def ree(ctx):
    ree = "<:RRRRRRRRRREEEEEEEEEEEEEEEEE:704541193610068053>"
    await ctx.send(ree*15)

@bot.command()
async def stare(ctx):
    stare = "<:4097_Mike_Sully_Face_Swap:700599136906379297>"
    await ctx.send(stare*15)

@bot.command()
async def sad(ctx):
    sad = "<:monka10:700244126699880558>"
    await ctx.send(sad*15)

@bot.command()
async def clown(ctx):
    clown = 15*"<:ClownJin:793818012167831592> "
    await ctx.send(clown)

@bot.command()
async def smd(ctx):
    d = "8====D"
    smd = d
    emoji = "<:lusty:720567594251452468>"
    emoji_after = "<:happy_hamlan:768710676679884820>"
    msg = await ctx.send(smd + emoji)
    for _ in range(5):
        smd = smd[:-1]
        time.sleep(0.3)
        await msg.edit(content=smd+emoji)
    for i in range(1, 5):
        smd = smd+d[i]
        time.sleep(0.3)
        await msg.edit(content=smd+d[i]+emoji)
    await msg.edit(content=d+emoji_after)

@bot.command(help="Set bot playing status")
@commands.check(isBen)
async def setplaying(ctx, *, text="Your pp"):
    await bot.change_presence(activity=discord.Game(name=text))

@bot.command(help="Set bot watching status")
@commands.check(isBen)
async def setwatching(ctx, *, text="Your nudes"):
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=text))

@bot.command(help="Set lyric search method, 1. mulanci, 2.kugeci, 3.genius")
async def method(ctx, m=None):
    if m:
        await ctx.send("Changed method: {} -> {}".format(bot.lyricsMethod, m))
        bot.lyricsMethod = m
    else:
        await ctx.send("Current method: {}".format(bot.lyricsMethod))

@bot.command(aliases=['lyrics'])
async def lyric(ctx, *, name=None):
    if name:
        content = lyrics.getLyric(name, int(bot.lyricsMethod))
        if content != "":
            #await ctx.send(content)
            embed = discord.Embed(
                title = "Lyrics:",
                description = content
            )
            await ctx.send(embed=embed)
    else:
        await ctx.send("Please type the song name as \".lyrics name\"")

@bot.command(aliases=['links'])
async def link(ctx, operation='all', code=' ', name=' '):
    """
        Operation:
        *Default* all (display all classes)  Usage: .link / .link all
        add (Add class)  Usage: .link add course_code course_name link type(L, T or P)
        delete (Delete Classes with course code)  Usage: .link delete course_code
    """
    # global s
    # s = Session() #create session object
    s = Session()
    try:
        if operation == "all":
            class_list = get_all_class(s)
            #print(class_list)
            embed = discord.Embed( #CREATE EMBED
                title = "Classes:",
                description = "Google Meet Links of Y2S3",
                color = discord.Color.green()
            )
            #Add fields into embed
            for c in class_list:
                class_links = c.urls
                links_embed = ""
                for class_link in class_links:
                    links_embed += "[{}]({}) ".format(class_link.url_name, class_link.url)
                embed.add_field(name = c.course_name,
                        value = "{}: {}"\
                        .format(c.course_code, links_embed),
                        inline=False
                    )
            await ctx.send(embed=embed)
        elif operation == "add":
            if not code == ' ' and not name == ' ':
                exist = False
                class_list = get_all_class(s)
                for c in class_list:
                    if c.course_code == code and c.course_name == name:
                        exist = True
                        await ctx.send("Class already exist!")
                        break
                if not exist:
                    if add_class(s, code, name):
                        await ctx.send(f"Added {code}")
                    else: await ctx.send("Something went wrong!")
                s.commit()
            else:
                await ctx.send("Usage: .link add course_code course_name")
        elif operation == "delete":
            if not code == ' ':
                if (delete_class_bycode(s, code)):
                    await ctx.send(f"Deleted {code}")
                else: await ctx.send("Class not found!")
                s.commit()
            else:
                await ctx.send("Usage: .link delete course_code")
    except:
        s.rollback()
        await ctx.send("Something went wrong!")
        raise
    finally:
        s.close()

@bot.command(help="Usage: .editlink course_code link_name/title new_link")
async def editlink(ctx, code=' ', url_name=' ', link=' ', type='link'):
    s = Session()
    try:
        if not code == ' ' and not link == ' ' and not url_name == ' ': #if all args given
            if type == 'link':
                if update_link(s, code, url_name, link):
                #if (update_classLink_bycode(s, code, link, c_type)):
                    await ctx.send(f"Updated {code} {url_name}")
                    s.commit()
                else: await ctx.send("Link not found!")
            elif type == 'title':
                if update_link_name(s, code, url_name, link):
                    await ctx.send(f"Updated {code} {link}")
                    s.commit()
        else:
            await ctx.send("Usage: .editlink course_code link_name new_link whattoedit(link(default), title)")
    except:
        s.rollback()
        await ctx.send("Something went wrong!")
        raise
    finally:
        s.close()

@bot.command(help="Usage: .addlink course_code link_name new_link")
async def addlink(ctx, code=' ', url_name=' ', link=' '):
    s = Session()
    try:
        if not code == ' ' and not link == ' ' and not url_name == ' ': #if all args given
            if add_link_bycode(s, code, url_name, link):
                await ctx.send(f"Added {code} {url_name}")
                s.commit()
            else: await ctx.send("Class not found!")
        else:
            await ctx.send("Usage: .addlink course_code link_name new_link")
    except:
        s.rollback()
        await ctx.send("Something went wrong!")
        raise
    finally:
        s.close()

@bot.command(help="Usage: .deletelink course_code link_name")
async def deletelink(ctx, code=' ', url_name=' '):
    s = Session()
    try:
        if not code == ' ' and not url_name == ' ': #if all args given
            if delete_link(s, code, url_name):
            # if add_link_bycode(s, code, url_name, link):
                await ctx.send(f"Deleted {code} {url_name}")
                s.commit()
            else: await ctx.send("Link not found!")
        else:
            await ctx.send("Usage: .deletelink course_code link_name")
    except:
        s.rollback()
        await ctx.send("Something went wrong!")
        raise
    finally:
        s.close()

@bot.command(help="Delete all the class links from DB (only owner)")
@commands.check(isBen)
async def deleteallclass(ctx):
    recreate_db()
    await ctx.send("Deleted everything.")


def updateBotKeywords():
        s = Session()
        try:
            bot.keywords = s.query(Keyword).all()
        except:
            raise
        finally:
            s.close()

@bot.command(help="Show all keywords")
@commands.check(isBen)
async def allkw(ctx):
    s = Session()
    try:
        c = s.query(Keyword).all()
        msg = ""
        for kw in c:
            msg = msg + kw.word + "\n"
        if msg != "":
            embed = discord.Embed(
                title = f"We currently have {len(c)} keywords:",
                description = msg,
                color = discord.Color.orange()
            )
            await ctx.send(embed=embed)
            #await ctx.send(msg)
        else: await ctx.send("There is 0 keyword rn!")
    except:
        await ctx.send("Something went wrong!")
        raise
    finally:
        s.close()
    #await ctx.send("Added {}.".format(word))

@bot.command(help="Add keyword response")
@commands.check(isBen)
async def addkw(ctx, word=' ', link=' '):
    s = Session()
    try:
        if not word == ' ' and not link == ' ': #if all args given
            exist = False
            c = s.query(Keyword).all()
            for kw in c:
                if kw.word == word:
                    await ctx.send(f"{word} already is a keyword, use .editkw to edit the link!")
                    exist = True
            if not exist:
                new_keyword = Keyword(
                    word = word,
                    link = link
                )
                s.add(new_keyword)
                await ctx.send(f"Added {word}.")
                s.commit()
        else:
            await ctx.send("Usage: .addkw keyword link")
    except:
        s.rollback()
        await ctx.send("Something went wrong!")
        raise
    finally:
        s.close()
    #await ctx.send("Added {}.".format(word))

@bot.command(help="Edit keyword link")
@commands.check(isBen)
async def editkw(ctx, word=' ', link=' '):
    s = Session()
    try:
        if not word == ' ' and not link == ' ': #if all args given
            edited = False
            c = s.query(Keyword).all()
            for kw in c: #loop tru all keywords from db
                if kw.word == word: #if the arg word is found, delete that keyword from db
                    kw.link = link
                    edited = True
            if edited:
                await ctx.send(f"Edited {word}.")
            else:
                await ctx.send(f"{word} is not a keyword!")
            s.commit()
        else:
            await ctx.send("Usage: .editkw keyword link")
    except:
        s.rollback()
        await ctx.send("Something went wrong!")
        raise
    finally:
        s.close()
    #await ctx.send("Added {}.".format(word))

@bot.command(help="Delete keyword response")
@commands.check(isBen)
async def delkw(ctx, word=' '):
    s = Session()
    try:
        if not word == ' ': #if all args given
            deleted = False
            c = s.query(Keyword).all()
            for kw in c: #loop tru all keywords from db
                if kw.word == word: #if the arg word is found, delete that keyword from db
                    s.delete(kw)
                    deleted = True
            if deleted: #if deleted, send msg and commit
                await ctx.send(f"Deleted {word}.")
                s.commit()
            else: #else send not found msg
                await ctx.send(f"{word} is not a keyword!")

        else:
            await ctx.send("Usage: .addkw keyword link")
    except:
        s.rollback()
        await ctx.send("Something went wrong!")
        raise
    finally:
        s.close()
    #await ctx.send("Added {}.".format(word))

@bot.command(aliases=['close'])
@commands.check(isBen)
async def quit(ctx):
    await bot.close()
    print("Bot closed.")

@bot.event
async def on_message(message):
    if message.author.id != 234395307759108106:
        print('Message from {0.author}: {0.content}'.format(message))
    #print(type(message.author))
    if message.author == bot.user:
        return
    # if ":7529_KEKW:" in message.content:
    #     kekw = 6*"<:7529_KEKW:734986562030403666> "
    #     msg = await message.channel.send(f"Yo {message.author.mention}, GTFO with the kekw")
    #     await asyncio.sleep(5.0)
    #     await msg.edit(content=kekw)
    if "clown" in message.content.lower():
        clown = 15*"<:ClownJin:793818012167831592> "
        await message.channel.send(clown)
    if ":4097_Mike_Sully_Face_Swap:" in message.content:
        stare = 15*"<:4097_Mike_Sully_Face_Swap:700599136906379297> "
        await message.channel.send(stare)
    # if "noice" in message.content.lower():
    #     await message.channel.send("https://giphy.com/gifs/8Odq0zzKM596g")
    if any(msg in message.content.lower() for msg in ["vibe", "vibing"]):
        await message.channel.send("https://tenor.com/view/cat-cat-vibing-cat-dancing-cat-jamming-cat-bopping-gif-18060934")
    if "bye" in message.content.lower() and message.author.id == 236815295610617856:
        await message.channel.send("Ah Chee, Bye")
    if "hi" == message.content.lower():
        if message.author.id == 171175305036300299:
            await message.channel.send("Ah Soh, Hi")
        elif message.author.id == 298650151860437023:
            await message.channel.send("Adrian, Hi")
        elif message.author.id == 236815295610617856:
            await message.channel.send("Clifford, Hi")
        elif message.author.id == 318221117640671234:
            await message.channel.send("Melvin, Hi")
        elif message.author.id == 722678030291435520:
            await message.channel.send("Diu, Hi")
        elif message.author.id == 458649160623718400 or message.author.id == 698072756033421402:
            await message.channel.send("Adu, Hi")
        else: await message.channel.send("Diam.")
    # if "diam" in message.content.lower():
    #     await message.channel.send("https://tenor.com/view/shut-the-fuck-up-gif-5518509")
    # if "lj" == message.content.lower():
    #     await message.channel.send('https://tenor.com/view/middle-finger-fuck-off-fuck-you-flip-off-screw-you-gif-12669379')
    # if "diao ni" == message.content.lower():
    #     await message.channel.send('https://tenor.com/view/middlefinger-mood-screwyou-leave-me-gif-10174031')
    for kw in bot.keywords: #loop tru all keywords from db
        if kw.word == message.content: #if the arg word is found, delete that keyword from db
            await message.channel.send(kw.link)
    await bot.process_commands(message)

@bot.command()
async def image(ctx, tag=None):
    print(tag)
    if tag != None:
        img = images.get_random_image(tag)
        await ctx.send(img)
    else: await ctx.send("usage: .image tag_name")


bot.run(os.environ.get('DISCORD_KEY', '-1'))
