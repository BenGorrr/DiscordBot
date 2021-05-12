# -*- coding: utf-8 -*-
import discord, asyncio, os, time, random, images
from discord.ext import commands
#from r6stats import R6Stats
import config
from classes import *

bot = commands.Bot(command_prefix = '.')
#Global variable
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

def updateBotKeywords(s=None):
    if s == None:
        s = Session()
        try:
            bot.keywords = s.query(Keyword).all()
        except:
            raise
        finally:
            s.close()
    else:
        try:
            bot.keywords = s.query(Keyword).all()
        except:
            raise


@bot.command(help="Show all keywords")
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
                updateBotKeywords(s)
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
                s.commit()
                updateBotKeywords(s)
            else:
                await ctx.send(f"{word} is not a keyword!")
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
                updateBotKeywords(s)
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


bot.load_extension("r6stats")
bot.load_extension("lyrics")
bot.run(os.environ.get('DISCORD_KEY', '-1'))
