import discord
from discord.ext import commands
import asyncio
import r6

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))
        if message.author == client.user:
            return
        if ":7529_KEKW:" in message.content:
            kekw = 6*"<:7529_KEKW:734986562030403666> "
            msg = await message.channel.send(f"Yo {message.author.mention}, GTFO with the kekw")
            await asyncio.sleep(5.0)
            await msg.edit(content=kekw)

        if message.author == "171175305036300299":
            if message.content.startswith('$shh'):
                try:
                    message.channel.send("Restarting :)")
                    await self.close()
                except:
                    pass
                finally:
                    os.system("python run.py")



client = MyClient()
client.run('NzY2NjI0Nzk3MjQ5NTAzMjMz.X4mE-g.SRG1cWPfz-0fjpr18LDFqN8Stmg')
