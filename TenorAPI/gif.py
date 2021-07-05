import requests, os, json, discord, random
from discord.ext import commands

class GIF(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = GIF_Client(api_key=os.environ.get('TENOR_API_KEY', '-1'))
        self.IDs_history = []

    @commands.command(help="Display a random dominic gif")
    async def family(self, ctx):
        gifs_result = self.client.gif_search("dominic toretto", 20)
        if gifs_result:
            gifs_result = json.loads(gifs_result.content)
            while 1:
                result = random.choice(gifs_result['results'])

                if result['id'] not in self.IDs_history:
                    if len(self.IDs_history) >= 10:
                        self.IDs_history.pop(0)
                    self.IDs_history.append(result['id'])
                    break
            await ctx.send(result["media"][0]["gif"]["url"])

    @commands.command(help="Display a random gif if no search term given")
    async def gif(self, ctx, search_term=""):
        if search_term == "":
            await ctx.send("Usage: .gif search_term")
            return
        gifs_result = self.client.gif_search(search_term, 20)
        if gifs_result:
            gifs_result = json.loads(gifs_result.content)
            while 1:
                result = random.choice(gifs_result['results'])

                if result['id'] not in self.IDs_history:
                    if len(self.IDs_history) >= 10:
                        self.IDs_history.pop(0)
                    self.IDs_history.append(result['id'])
                    break
            await ctx.send(result["media"][0]["gif"]["url"])

class GIF_Client:

    def __init__(self, base_url='', api_key='', media_filter='minimal'):
        self.set_base_url(base_url)
        self.api_key = api_key
        self.media_filter = media_filter

    def set_base_url(self, base_url):
        if base_url == '':
            base_url = "https://g.tenor.com/v1"
        self.base_url = base_url.rstrip('/')

    def do(self, method, path, req=None):

        try:
            params = json.loads(json.dumps(req))
            params['key'] = self.api_key
            params['media_filter'] = self.media_filter
        except Exception:
            params = None
        args = dict(params=params)

        url = self.base_url + path
        resp = requests.request(method, url, **args)

        if resp.status_code == 200:
            return resp
        else:
            print(resp.status_code)

    def gif_search(self, search_term, lmt, next=-1):
        req = { 'q':search_term, 'limit':lmt, 'pos':next}

        return self.do('GET', '/search', req=req)

    def random_gif_search(self, search_term, lmt):
        req = { 'q':search_term, 'limit':lmt }

        return self.do('GET', '/random', req=req)

def setup(bot):
    bot.add_cog(GIF(bot))
