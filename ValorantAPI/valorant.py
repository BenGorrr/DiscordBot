import requests, json, asyncio
import RSO_Auth
from ..Utils import files_util, messages
from discord.ext import commands

class Valorant(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = Client()

    @commands.command()
    async def valadd(self, ctx):
        await ctx.author.send("Send me your id and password seperated by a space! [user pass]")
        # wait for reponse
        check = messages.message_check(channel=ctx.author.dm_channel())
        response = await self.bot.wait_for('message', check=check)
        try:
            response.split(' ')
        except:
            await ctx.author.send("Invalid input :/")


class Client():
    def __init__(self, base_url='', access_token='', entitlements_token=''):
        self.set_base_url(base_url)
        self.access_token = access_token
        self.entitlements_token = entitlements_token

    def get_auth(self, username, password):
        data = asyncio.get_event_loop().run_until_complete(RSO_Auth.auth(username, password))
        self.access_token, self.entitlements_token = data

    def set_base_url(self, base_url):
        if base_url == '':
            base_url = r"https://api.henrikdev.xyz"
        self.base_url = base_url.rstrip('/')

    def do(self, method, path, req=None, auth=False):
        try:
            params = json.loads(json.dumps(req))
        except Exception:
            params = None

        headers = {"Authorization": "Bearer " + self.access_token, "X-Riot-Entitlements-JWT": self.entitlements_token} if auth else None
        args = dict(params=params, headers=headers)

        url = self.base_url + path
        resp = requests.request(method, url, **args)
        if resp.status_code == 200:
            return resp
        else:
            print(resp.status_code, resp.text)

    def get_content(self):
        self.set_base_url(r"https://api.henrikdev.xyz")
        return self.do('GET', r'/valorant/v1/content')

    def get_player(self, name='', tag=''):
        self.set_base_url(r"https://api.henrikdev.xyz")
        return self.do('GET', r'/valorant/v1/account/'+ f"{name}/{tag}")

    def get_store_from_id(self, id=''):
        self.set_base_url(r"https://pd.AP.a.pvp.net/")
        return self.do('GET', r'/store/v2/storefront/' + id, auth=True)

    def get_player_store(self, name, tag):
        player_id = self.get_player(name, tag).json()['data']['puuid']
        store_ids = self.get_store_from_id(player_id).json()['SkinsPanelLayout']['SingleItemOffers']
        # skins_ids = read_Json('content.txt')['skinLevels']
        skins_ids = files_util.read_Json('content.txt')['skinLevels']
        skins_name = []
        for store_id in store_ids:
            skins_name.append(next(skin for skin in skins_ids if skin['id'] == store_id.upper())['name'])
        return skins_name

    def update_content(self, file):
        data = self.get_content()
        # write_Json(file, data.json())
        files_util.write_Json(file, data.json())