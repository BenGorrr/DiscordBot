import discord
from discord.ext import commands
import asyncio
from r6 import R6
import os

bot = commands.Bot(command_prefix = '.')
rankList = [
    'Unranked', 'Copper IV', 'Copper III', 'Copper II', 'Copper I',
    'Bronze IV', 'Bronze III', 'Bronze II', 'Bronze I',
    'Silver V', 'Silver IV', 'Silver III', 'Silver II', 'Silver I',
    'Gold III', 'Gold II', 'Gold I', 'Platinum III', 'Platinum II', 'Platinum I',
    'Diamond', 'Champions',
    ]
def_playerList = {
    'BenGorr':'044e7ff2-67d6-4706-8bfd-b1503af00b9b', 'Pingu_525':'bfaf9738-2401-4d5c-918b-c460b8760cdc',
    'LilCh33tos':'8def768d-dae1-4c06-9e02-7e1b6d8b15f0', 'Benboojini':'c9bb4e6b-1a3e-4ba0-95db-7af886f2916f'
    }

@bot.event
async def on_ready():
    print('Logged on as {0}!'.format(bot.user))

def isBen(ctx):
    return ctx.author.id == 171175305036300299

@bot.command(aliases=['r'])
@commands.check(isBen)
async def restart(ctx):
    try:
        await ctx.send("Restarting :)")
        await bot.close()
    except:
        pass
    finally:
        os.system("python run.py")

@bot.command()
async def hi(ctx):
    await ctx.send(f"Hi! {ctx.author.mention}")

@bot.command()
async def bye(ctx):
    await ctx.send(f"Bye! {ctx.author.mention}")

@bot.command()
async def r6(ctx, name, platform="uplay"):
    player = R6(name, platform)
    print(player.data)
    if (not player.data):
        await ctx.send(f"Couldn't find user: {name}")
        return
    else:
        for x, y in player.data.items():
            print(f"{x} : {y}")
        embed = discord.Embed(
            title = f"Rank: {rankList[int(player.data['ranked']['rank'])]}",
            description = f"Level: {player.data['stats']['level']}"
        )
        rank_url = f"https://tabstats.com/images/r6/ranks/?rank={player.data['ranked']['rank']}&champ={player.data['ranked']['champ']}"
        icon_url = f"https://ubisoft-avatars.akamaized.net/{player.data['profile']['p_id']}/default_146_146.png"
        embed.set_thumbnail(url=rank_url)
        embed.set_author(name=player.data['profile']['p_name'], icon_url=icon_url)
        embed.add_field(name="Current MMR: ", value=f"{player.data['ranked']['mmr']}", inline=False)
        embed.add_field(name="KD: ", value=f"{player.data['ranked']['kd']}", inline=False)
        await ctx.send(embed=embed)

@bot.command()
async def us(ctx, platform="uplay"):
    players = []
    for i in def_playerList:
        player = R6(i, platform)
        if (not player.data):
            await ctx.send(f"Couldn't find user: {i}")
            continue
        else:
            print(player.data['ranked']['mmr'])
            player.data['mmr'] = player.data['ranked']['mmr']
            players.append(player.data)
    players = sorted(players, key = lambda i: i['mmr'], reverse=True)
    desc = ""
    for i in range(len(players)):
        desc = desc + f"#{i+1} {players[i]['profile']['p_name']} Rank: {rankList[players[i]['ranked']['rank']]}({players[i]['mmr']}) \n"

    embed = discord.Embed(
        title = "Ranking Among Us:",
        description = desc
    )
    embed.set_thumbnail(url=f"https://tabstats.com/images/r6/ranks/?rank={players[-1]['ranked']['rank']}&champ={players[-1]['ranked']['champ']}")
    await ctx.send(embed=embed)

@bot.event
async def on_message(message):
    print('Message from {0.author}: {0.content}'.format(message))
    if message.author == bot.user:
        return
    if ":7529_KEKW:" in message.content:
        kekw = 6*"<:7529_KEKW:734986562030403666> "
        msg = await message.channel.send(f"Yo {message.author.mention}, GTFO with the kekw")
        await asyncio.sleep(5.0)
        await msg.edit(content=kekw)
    await bot.process_commands(message)


bot.run('NzY2NjI0Nzk3MjQ5NTAzMjMz.X4mE-g.SRG1cWPfz-0fjpr18LDFqN8Stmg')
