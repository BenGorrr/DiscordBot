import os, requests, json, discord
from discord.ext import commands

class ImagesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = ImagesClient()
        self.nsfw = False

    @commands.command(help="Enable/Disable NSFW for .image")
    async def imageNSFW(self, ctx, state=""):
        if state == "":
            await ctx.send("Image NSFW: " + str(self.nsfw))
        elif state.lower() in ["yes", "no"]:
            curNsfw = self.nsfw
            self.nsfw = True if state.lower() == "yes" else False
            if self.nsfw != curNsfw:
                await ctx.send("Image NSFW: " + str(curNsfw) + " -> " + str(self.nsfw))
            else: await ctx.send("Image NSFW: " + str(self.nsfw))
        else: await ctx.send("usage: .imageNSFW (yes | no)")

    @commands.command(help="Get a random image with a tag")
    async def image(self, ctx, tag=None):
        if tag != None:
            img = self.client.get_random_image(tag, self.nsfw)
            if img != None:
                await ctx.send(img)
            else: await ctx.send("Can't find any :c")
        else: await ctx.send("usage: .image tag_name")

    @commands.command(help="Get the list of tags that can be used with .image")
    async def imagetags(self, ctx):
        tags = self.client.get_tags_list()
        if tags != None:
            normal_tags = ', '.join(tags['tags'])
            nsfw_tags = ', '.join(tags['nsfw_tags'])
            await ctx.send("Tags: " + normal_tags + "\nNSFW Tags: " + nsfw_tags)
        else: await ctx.send("Can't find any :c")

    @commands.command(help="Get a random meme from reddit")
    async def meme(self, ctx):
        meme = self.client.get_random_meme()
        if meme != None:
            await ctx.send(meme)
        else: await ctx.send("Can't find any :c")

    @commands.command(help="Get a random image from wikihow", aliases=['wiki'])
    async def wikihow(self, ctx):
        wiki = self.client.get_random_wikihow(self.nsfw)
        if wiki != None:
            await ctx.send(wiki)
        else: await ctx.send("Can't find any :c")

class ImagesClient():
    """ API DOCS: https://docs.ksoft.si/api/images-api """

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
        else: print("ERROR: " + resp.text)

    def get_random_image(self, tag, nsfw):
        req = { 'tag':tag , 'nsfw':nsfw }
        resp = self.do('GET', '/random-image', req)

        if resp != None:
            return resp['url']

    def get_tags_list(self):
        resp = self.do('GET', '/tags')

        if resp != None:
            return resp

    def get_random_meme(self):
        resp = self.do('GET', '/random-meme')

        if resp != None:
            return resp['image_url']

    def get_random_wikihow(self, nsfw):
        req = { 'nsfw':nsfw }
        resp = self.do('GET', '/random-wikihow', req)

        if resp != None:
            return resp['url']

def setup(bot):
    bot.add_cog(ImagesCog(bot))
