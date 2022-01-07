from typing_extensions import final
from discord import player
import requests, json, time
from . import RSO_Auth
# from .Utils import files_util, messages
from Utils import files_util, messages
import discord
from discord.ext import commands
from models import ValorantUsers

class Valorant(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = Client()
        self.engine = bot.engine
        self.Session = bot.Session
        self.last_auth_user = None

    @commands.command(help="Add user's valorant account in order to use .valstore")
    async def valadd(self, ctx):
        await ctx.author.send("Reply with your id and password and ingame name with tag seperated by a space! \nExample: [benn123 mypassword BenGorr#1234]")
        # create a check for messages from author only
        check = messages.message_check(channel=ctx.author.dm_channel)
        # wait for reponse
        response = await self.bot.wait_for('message', check=check)
        try:
            id, pw, ign = response.content.split(' ')
            # add user to db
            if self.addUser({'id': id, 'pw': pw, 'ign': ign.lower()}):
                await ctx.author.send("Added :)")
            else: await ctx.author.send("Something went wrong!")

        except Exception as e:
            await ctx.author.send("Invalid input :/ Error:" + e)

    @commands.command(help="Display user's valorant daily store")
    async def valstore(self, ctx, username='', image=''):
        try: 
            # if username is empty
            if not username:
                await ctx.send("Usage: .valstore [in-game-name without #tag]")
                return

            name = username.lower()
            # get user from db
            valoUsers = self.getUser()
            print(f"Name: {name} \nvaloUsers: {valoUsers} \n")
            if not valoUsers: # if the query is empty
                await ctx.send("Id not found")
                return

            id = None
            # search for the user with the user given ign
            for user in valoUsers: 
                if name in user.ign:
                    id = user
                    break

            if not id: # if user not found
                await ctx.send("Id not found. Use .valadd to add your valorant id")
                return

            print(f"id: {id} \n username: {id.username} ign: {id.ign}")
            print(f"Last auth user: {self.last_auth_user}")
            # Get Auth with username and password
            # If last auth time is more than 1 hour or it is not previously auth'd
            if (int(time.time()) - id.last_auth > 3600) or username.lower() != self.last_auth_user:
                await self.client.get_auth(id.username, id.password)    # Get auth
                self.update_last_auth(id.username, int(time.time()))    # update user's last auth time
                self.last_auth_user = username.lower()                  # update last auth'd user

            name, tag = id.ign.split("#") 
            # Get player store (list of dict with 'name' and 'img' key)
            player_store = self.client.get_player_store(name, tag, id.ppuid)

            # Create and setup embed
            embed = discord.Embed(title=f"{id.ign}'s Store:")
            player_card = id.player_card
            embed.set_thumbnail(url=player_card)

            if image == '': # Send one embed with text-only
                # if user does not want weapon image
                for item in player_store:
                    embed.add_field(name=item['name'], value=15*'-', inline=False)
                
                await ctx.send(embed = embed)
            elif image.lower() == 'img': # Send multiple embeds with weapon images
                await ctx.send(embed = embed)
                for item in player_store:
                    embed = discord.Embed(title=item['name'])
                    embed.set_image(url=item['img'])

                    await ctx.send(embed = embed)

        except Exception as e:
            print(e)
            await ctx.send("Something went wrong!")

    @commands.command(help="Show all currently added valorant users")
    async def valusers(self, ctx):
        valoUsers = self.getUser()  # Get users from db
        if valoUsers:
            users = [user.ign for user in valoUsers]
            await ctx.send(users)
        else:
            await ctx.send("There is no users.")

    def addUser(self, entry: dict):
        s = self.Session()  # Create db session
        isAdded = False
        try:
            username, password, ign = entry.values()
            # Get player info
            player = self.client.get_player(*ign.split('#')).json()
            ppuid = player['data']['puuid']
            player_card = player['data']['card']['small']
            # Create new entry
            new_user = ValorantUsers(
                username = username, 
                password = password, 
                ign = ign, 
                ppuid = ppuid,
                player_card = player_card, 
                last_auth = 0
            )
            s.add(new_user) # Add entry
            s.commit()
            isAdded = True
        except Exception as e:
            s.rollback()
            print(e)
        finally:
            s.close()
            return isAdded

    def getUser(self):
        s = self.Session()
        valoUsers = []
        try:
            valoUsers = s.query(ValorantUsers).all()
        except:
            raise
        finally:
            s.close()
            return valoUsers

    def update_last_auth(self, username, time):
        s = self.Session()
        try:
            valoUsers = s.query(ValorantUsers).all()
            for user in valoUsers:
                if user.username == username:
                    user.last_auth = time   # Update user's last auth time to db
                    s.commit()
                    break
        except:
            s.rollback()
            raise
        finally:
            s.close()

    @commands.command(help="Delete all currently added valorant users")
    async def valdelall(self, ctx):
        s = self.Session()
        try:
            s.query(ValorantUsers).delete()
            s.commit()
            ValorantUsers.__table__.drop(self.engine)   # drop the whole table
        except:
            s.rollback()
            await ctx.send("Something went wrong!")
            raise
        finally:
            s.close()
            await ctx.send("All ids deleted")


class Client():
    def __init__(self, base_url='', access_token='', entitlements_token=''):
        self.set_base_url(base_url)
        self.access_token = access_token
        self.entitlements_token = entitlements_token
        self.contentFile = "ValorantAPI\content.txt"
        self.skinsFile = "ValorantAPI\skinsIDS.txt"

    async def get_auth(self, username, password):
        # data = asyncio.get_event_loop().run_until_complete(RSO_Auth.auth(username, password))
        print(f"Getting auth for {username}")
        data = await RSO_Auth.auth(username, password)
        if data:
            print("Authorization done!")
        self.access_token, self.entitlements_token = data   # Set tokens that we get from RSO_Auth

    def set_base_url(self, base_url):
        if base_url == '':
            base_url = r"https://api.henrikdev.xyz"
        self.base_url = base_url.rstrip('/')

    def do(self, method, path, req=None, auth=False):
        try:
            params = json.loads(json.dumps(req))
        except Exception:
            params = None
        headers = {"Authorization": "Bearer " + self.access_token, "X-Riot-Entitlements-JWT": self.entitlements_token} if auth else {}
        headers['Accept'] = 'application/json'
        headers['Content-Type'] = 'application/json'
        
        args = dict(params=params, headers=headers)

        url = self.base_url + path
        resp = requests.request(method, url, **args)
        if resp.status_code == 200:
            return resp
        else:
            print(resp.status_code, resp.headers, url)

    def get_content(self):
        self.set_base_url(r"https://api.henrikdev.xyz")
        return self.do('GET', r'/valorant/v1/content')

    def get_skins_content(self):
        allSkinNames = []
        self.set_base_url(r'https://valorant-api.com/v1')
        content = self.do('GET', r'/weapons/skins').json()
        for item in content['data']:
            allSkinNames.append({'uuid': item['levels'][0]['uuid'].upper(), 'name': item['displayName'], 'img': item['levels'][0]['displayIcon']})
        return allSkinNames

    def get_player(self, name='', tag=''):
        print(f"{name}/{tag}")
        self.set_base_url(r"https://api.henrikdev.xyz")
        return self.do('GET', r'/valorant/v1/account/'+ f"{name}/{tag}")

    def get_store_from_id(self, id=''):
        self.set_base_url(r"https://pd.AP.a.pvp.net/")
        return self.do('GET', r'/store/v2/storefront/' + id, auth=True)

    def get_player_store(self, name, tag, ppuid):
        # player_id = self.get_player(name, tag).json()['data']['puuid']
        player_id = ppuid
        print("Got player id")
        store_ids = self.get_store_from_id(player_id).json()['SkinsPanelLayout']['SingleItemOffers']
        print("Got player store ids")
        try:
            #skins_ids = files_util.read_Json(self.contentFile)['skinLevels']
            skins_ids = files_util.read_Json(self.skinsFile)
        except:
            # self.update_content(self.contentFile)
            # skins_ids = files_util.read_Json(self.contentFile)['skinLevels']
            self.update_skins(self.skinsFile)   # Update skins file if file does not exist
            skins_ids = files_util.read_Json(self.skinsFile)

        skins = []
        tries = 0
        found = False
        while not found and tries <= 1:
            for store_id in store_ids:
                #skins_name.append(next(skin for skin in skins_ids if skin['id'] == store_id.upper())['name'])
                try:
                    skin = next(skin_id for skin_id in skins_ids if skin_id['uuid'] == store_id.upper())
                    skins.append({'name': skin['name'], 'img': skin['img']})
                except Exception as e:
                    print(e)
            if len(skins) != len(store_ids): # if not all skins is found
                tries += 1
                self.update_skins(self.skinsFile)   # Update skins file incase there is update
                skins_ids = files_util.read_Json(self.skinsFile)
            else: found = True
        
        return skins

    def update_content(self, file):
        data = self.get_content()
        # write_Json(file, data.json())
        files_util.write_Json(file, data.json())
        print("Updated content")

    def update_skins(self, file):
        data = self.get_skins_content()
        files_util.write_Json(file, data)
        print("Updated skins")

def setup(bot):
    bot.add_cog(Valorant(bot))
