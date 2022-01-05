import requests, json, asyncio
from . import RSO_Auth
# from .Utils import files_util, messages
from Utils import files_util, messages
from discord.ext import commands
from models import ValorantUsers

class Valorant(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = Client()
        self.ids = []
        self.engine = bot.engine
        self.Session = bot.Session

    @commands.command()
    async def valadd(self, ctx):
        await ctx.author.send("Send me your id and password and ingame name with tag seperated by a space! [user pass BenGorr#1234]")
        # wait for reponse
        check = messages.message_check(channel=ctx.author.dm_channel)
        response = await self.bot.wait_for('message', check=check)
        try:
            id, pw, ign = response.content.split(' ')
            self.ids.append({'id': id, 'pw': pw, 'ign': ign.lower()})
        except Exception as e:
            await ctx.author.send("Invalid input :/ Error:" + e)

    @commands.command()
    async def valstore(self, ctx, username):
        try: 
            name = username.lower()
            print(name)
            id = self.search(name)
            print(type(id))
            if not id:
                await ctx.send("Id not found")
                return
            await self.client.get_auth(id['id'], id['pw'])
            name, tag = id['ign'].split("#")
            player_store = self.client.get_player_store(name, tag)
            await ctx.send(player_store)
        except Exception as e:
            print(e)

    # TODO: use addUser and getUser in the command method

    def addUser(self, entry):
        s = self.Session()
        try:
            username, password, ign = entry.values()
            new_user = ValorantUsers(
                username = username, 
                password = password, 
                ign = ign
            )
            s.add(new_user)
            s.commit()
        except:
            s.rollback()
            raise
        finally:
            s.close()

    def getUser(self):
        s = self.Session()
        try:
            valoUsers = s.query(ValorantUsers).all()
        except:
            raise
        finally:
            s.close()
            return valoUsers


    @commands.command()
    async def valdelall(self, ctx):
        self.ids = []
        await ctx.send("All ids deleted")

    def search(self, name):
        for id in self.ids:
            if name in id['ign']:
                return id



class Client():
    def __init__(self, base_url='', access_token='', entitlements_token=''):
        self.set_base_url(base_url)
        self.access_token = access_token
        self.entitlements_token = entitlements_token

    async def get_auth(self, username, password):
        # data = asyncio.get_event_loop().run_until_complete(RSO_Auth.auth(username, password))
        data = await RSO_Auth.auth(username, password)
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
        try:
            skins_ids = files_util.read_Json('content.txt')['skinLevels']
        except:
            self.update_content('content.txt')
            skins_ids = files_util.read_Json('content.txt')['skinLevels']
        skins_name = []
        for store_id in store_ids:
            skins_name.append(next(skin for skin in skins_ids if skin['id'] == store_id.upper())['name'])
        return skins_name

    def update_content(self, file):
        data = self.get_content()
        # write_Json(file, data.json())
        files_util.write_Json(file, data.json())

def setup(bot):
    bot.add_cog(Valorant(bot))
