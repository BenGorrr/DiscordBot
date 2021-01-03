import discord, config
from discord.ext import commands
import asyncio
#from r6 import R6
from r6stats import R6Stats
import os, time

bot = commands.Bot(command_prefix = '.')
colorRGB = [(230, 70, 30), (107, 62, 50), (237, 240, 238), (247, 250, 75), (84, 252, 255), (138, 112, 255), (255, 20, 126)]
# rankList = [
#     'Unranked', 'Copper IV', 'Copper III', 'Copper II', 'Copper I',
#     'Bronze IV', 'Bronze III', 'Bronze II', 'Bronze I',
#     'Silver IV', 'Silver III', 'Silver II', 'Silver I',
#     'Gold III', 'Gold III', 'Gold II', 'Gold I', 'Platinum III', 'Platinum II', 'Platinum I',
#     'Diamond', 'Champions',
#     ]


@bot.event
async def on_ready():
    print('Logged on as {0}!'.format(bot.user))

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
            color = discord.Color.from_rgb(*colorRGB[0])
        elif (rank <= 10): #bronze
            color = discord.Color.from_rgb(*colorRGB[1])
        elif (rank <= 15): #silver
            color = discord.Color.from_rgb(*colorRGB[2])
        elif (rank <= 18): #gold
            color = discord.Color.from_rgb(*colorRGB[3])
        elif (rank <= 21): #plat
            color = discord.Color.from_rgb(*colorRGB[4])
        elif (rank == 22): #diamond
            color = discord.Color.from_rgb(*colorRGB[5])
        elif (rank == 23): #champion
            color = discord.Color.from_rgb(*colorRGB[6])

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
    for username in config.def_playerList.keys():
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

@bot.command(help="Purge messages, Usage: .purge limit")
@commands.check(isBen)
async def purge(ctx, limit=100):
    deleted = await ctx.channel.purge(limit=limit, check=is_bot)
    await ctx.channel.send('Deleted {} message(s)'.format(len(deleted)))

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
async def setplaying(ctx, *, text="Your pp"):
    await bot.change_presence(activity=discord.Game(name=text))

@bot.command(help="Set bot watching status")
async def setwatching(ctx, *, text="Your nudes"):
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=text))

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
    if "noice" in message.content.lower():
        await message.channel.send("https://giphy.com/gifs/8Odq0zzKM596g")
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
    await bot.process_commands(message)


bot.run(config.discord_api_key)
