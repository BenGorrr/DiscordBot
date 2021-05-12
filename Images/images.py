import os, requests, json, discord
from discord.ext import commands

class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def image(self, ctx, tag=None):
        print(tag)
        if tag != None:
            img = self.get_random_image(tag)
            await ctx.send(img)
        else: await ctx.send("usage: .image tag_name")

    def get_random_image(self, tag):
        url = "https://api.ksoft.si/images/random-image?tag=" + tag
        headers = {'Authorization': 'Bearer ' + os.environ.get('KSOFT_KEY', '-1')}
        resp = requests.get(url, headers=headers)
        content = json.loads(resp.text)
        #print(content)
        if(resp.status_code != 200):
            print(content['message'])
            return
        return content["url"]

def setup(bot):
    bot.add_cog(Images(bot))
