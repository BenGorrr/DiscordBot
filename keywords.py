import discord
from discord.ext import commands
from models import Keyword

class Keywords(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.keywords = []
        self.engine = bot.engine
        #Base.metadata.create_all(self.engine)
        self.Session = bot.Session

    async def on_ready():
        self.updateBotKeywords()

    def updateBotKeywords(self, s=None):
        if s == None:
            s = self.Session()
            try:
                self.keywords = s.query(Keyword).all()
            except:
                raise
            finally:
                s.close()
        else:
            try:
                self.keywords = s.query(Keyword).all()
            except:
                raise

    @commands.command(help="Show all keywords")
    async def allkw(self, ctx):
        s = self.Session()
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

    @commands.command(help="Add keyword response")
    async def addkw(self, ctx, word=' ', link=' '):
        s = self.Session()
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
                    self.updateBotKeywords(s)
            else:
                await ctx.send("Usage: .addkw keyword link")
        except:
            s.rollback()
            await ctx.send("Something went wrong!")
            raise
        finally:
            s.close()

    @commands.command(help="Edit keyword link")
    async def editkw(self, ctx, word=' ', link=' '):
        s = self.Session()
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
                    self.updateBotKeywords(s)
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

    @commands.command(help="Delete keyword response")
    async def delkw(self, ctx, word=' '):
        s = self.Session()
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
                    self.updateBotKeywords(s)
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

    @commands.Cog.listener()
    async def on_message(self, message):
        for kw in self.keywords: #loop tru all keywords from db
            if kw.word == message.content: #if the arg word is found, delete that keyword from db
                await message.channel.send(kw.link)

def setup(bot):
    bot.add_cog(Keywords(bot))
