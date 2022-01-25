# -*- coding: utf-8 -*-
import discord, asyncio, os, time
from discord.ext import commands
from run import isBen, is_bot

class MainCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # def isBen(self, ctx):
    #     return ctx.author.id == 171175305036300299

    # def is_bot(self, ctx):
    #     return ctx.author == self.bot.user

    @commands.command(help="pingpong test")
    async def ping(self, ctx):
        await ctx.send(f"pong!")

    @commands.command(help="kekw, try it")
    async def kekw(self, ctx):
        kekw = "<:7529_KEKW:734986562030403666> "
        if ctx.author == 318221117640671234:
            await ctx.send(kekw + "Nope.")
            return
        msgs = []
        j = [i for i in range(1, 6)]# + [i for i in range(4, 0, -1)]
        for i in j:
            msgs.append(await ctx.send(i*kekw))
        #print("sleeping for 3 secs")
        #await asyncio.sleep(3.0)
        for m in msgs:
            await m.delete()
        await ctx.message.delete()

    @commands.command(help="Purge bot messages, Usage: .purge limit")
    @commands.check(isBen)
    async def purge(self, ctx, limit=100):
        deleted = await ctx.channel.purge(limit=limit, check=is_bot)
        await ctx.channel.send('Deleted {} message(s)'.format(len(deleted)))

    @commands.command(help="Clear messages, Usage: .clear limit")
    async def clear(self, ctx, limit=100):
        deleted = await ctx.channel.purge(limit=limit)
        await ctx.channel.send('Cleared {} message(s)'.format(len(deleted)))

    @commands.command()
    async def fuck(self, ctx, *, name="me"):
        await ctx.send("Fuck " + name)
        await ctx.message.delete()

    @commands.command(aliases=['reee', 'reeee', 'reeeee', 'reeeeee'])
    async def ree(self, ctx):
        ree = "<:RRRRRRRRRREEEEEEEEEEEEEEEEE:704541193610068053>"
        await ctx.send(ree*15)

    @commands.command()
    async def stare(self, ctx):
        stare = "<:4097_Mike_Sully_Face_Swap:700599136906379297>"
        await ctx.send(stare*15)

    @commands.command()
    async def sad(self, ctx):
        sad = "<:monka10:700244126699880558>"
        await ctx.send(sad*15)

    @commands.command()
    async def clown(self, ctx):
        clown = 15*"<:ClownJin:793818012167831592> "
        await ctx.send(clown)

    @commands.command()
    async def smd(self, ctx):
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

    @commands.command(help="Set bot playing status")
    @commands.check(isBen)
    async def setplaying(self, ctx, *, text="Your pp"):
        await self.bot.change_presence(activity=discord.Game(name=text))

    @commands.command(help="Set bot watching status")
    @commands.check(isBen)
    async def setwatching(self, ctx, *, text="Your nudes"):
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=text))

    @commands.command(aliases=['close'])
    @commands.check(isBen)
    async def quit(self, ctx):
        await self.bot.close()
        print("Bot closed.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id != 234395307759108106:
            print('Message from {0.author}: {0.content}'.format(message))
        #print(type(message.author))
        if message.author == self.bot.user:
            return
        # if ":7529_KEKW:" in message.content:
        #     kekw = 6*"<:7529_KEKW:734986562030403666> "
        #     msg = await message.channel.send(f"Yo {message.author.mention}, GTFO with the kekw")
        #     await asyncio.sleep(5.0)
        #     await msg.edit(content=kekw)
        # if "clown" in message.content.lower():
        #     clown = 15*"<:ClownJin:793818012167831592> "
        #     await message.channel.send(clown)
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
        if "haha" == message.content.lower() and message.author.id == 458649160623718400:
            await message.channel.send("https://tenor.com/view/kettle-tea-morning-gif-7894132")


def setup(bot):
    bot.add_cog(MainCog(bot))
