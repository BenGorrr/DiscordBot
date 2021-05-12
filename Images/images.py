import os, requests, json, discord
from discord.ext import commands

class ImagesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = ImagesClient()

    @commands.command()
    async def image(self, ctx, tag=None):
        print(tag)
        if tag != None:
            img = self.client.get_random_image(tag)
            if img != None:
                await ctx.send(img)
            else: await ctx.send("Can't find any :c")
        else: await ctx.send("usage: .image tag_name")


class ImagesClient():
    def __init__(self, base_url=''):
        self.set_base_url(base_url)
        self.api_key = os.environ.get('KSOFT_KEY', '-1')

    # set base url, if none are given, use default url
    def set_base_url(self, base_url):
        if base_url == '':
            base_url = "https://api.ksoft.si/images"
        self.base_url = base_url.rstrip('/')

    # send request and return it if status 200
    def do(self, method, path, req=None):
        try :
            params = json.loads(json.dumps(req))
        except Exception:
            params = None
        headers = {'Authorization': 'Bearer ' + self.api_key}
        args = dict(params=params, headers=headers)

        url = self.base_url + path
        resp = requests.request(method, url, **args)

        if resp.status_code == 200:
            return resp.json()
        else: print("ERROR: " + resp.json()['message'])

    def get_random_image(self, tag, nsfw=False):
        req = { 'tag':tag , 'nsfw':nsfw }
        resp = self.do('GET', '/random-image', req)

        if resp != None:
            return resp['url']

def setup(bot):
    bot.add_cog(ImagesCog(bot))
