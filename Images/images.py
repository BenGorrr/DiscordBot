import os, requests, json, discord
from discord.ext import commands

class ImagesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = ImagesClient()
        self.nsfw = False

    @commands.command()
    async def imageNSFW(self, ctx, state=""):
        if state.lower() in ["yes", "no"]:
            self.nsfw = True if state.lower() == "yes" else False
            await ctx.send("Image NSFW: " + str(self.nsfw))
        else: await ctx.send("usage: .imageNSFW (yes | no)")

    @commands.command()
    async def image(self, ctx, tag=None):
        if tag != None:
            img = self.client.get_random_image(tag, self.nsfw)
            if img != None:
                await ctx.send(img)
            else: await ctx.send("Can't find any :c")
        else: await ctx.send("usage: .image tag_name")

    @commands.command()
    async def imagetags(self, ctx):
        tags = self.client.get_tags_list()
        if tags != None:
            normal_tags = ', '.join(tags['tags'])
            nsfw_tags = ', '.join(tags['nsfw_tags'])
            await ctx.send("Tags: " + normal_tags + "\nNSFW Tags: " + nsfw_tags)
        else: await ctx.send("Can't find any :c")

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

    def get_random_image(self, tag, nsfw):
        req = { 'tag':tag , 'nsfw':nsfw }
        resp = self.do('GET', '/random-image', req)

        if resp != None:
            return resp['url']

    def get_tags_list(self):
        resp = self.do('GET', '/tags')

        if resp != None:
            return resp

def setup(bot):
    bot.add_cog(ImagesCog(bot))
