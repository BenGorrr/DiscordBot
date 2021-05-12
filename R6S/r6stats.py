import requests, json, os, discord
from discord.ext import commands

class R6(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.COLOR_RGB = [(230, 70, 30), (107, 62, 50), (237, 240, 238), (247, 250, 75), (84, 252, 255), (138, 112, 255), (255, 20, 126)]
        #player id for the friends only stats
        self.def_playerList = {
            'BenGorr':'044e7ff2-67d6-4706-8bfd-b1503af00b9b', 'n1.Pigu':'bfaf9738-2401-4d5c-918b-c460b8760cdc',
            'LilCh33tos':'8def768d-dae1-4c06-9e02-7e1b6d8b15f0', 'JellyF1shBean':'c9bb4e6b-1a3e-4ba0-95db-7af886f2916f'
            }

    @commands.command(help="Check rainbow six siege stats. Usage: .r6 name")
    async def r6(self, ctx, name, platform="pc"):
        player = R6Stats(name, platform)
        #print(player.data)
        if (not player.genericStats):
            await ctx.send(f"Couldn't find user: {name}")
            return
        else:
            rank = player.statsAsia['rank']
            color = discord.Color.default()
            if (rank >= 1 and rank <= 5): #copper
                color = discord.Color.from_rgb(*self.COLOR_RGB[0])
            elif (rank <= 10): #bronze
                color = discord.Color.from_rgb(*self.COLOR_RGB[1])
            elif (rank <= 15): #silver
                color = discord.Color.from_rgb(*self.COLOR_RGB[2])
            elif (rank <= 18): #gold
                color = discord.Color.from_rgb(*self.COLOR_RGB[3])
            elif (rank <= 21): #plat
                color = discord.Color.from_rgb(*self.COLOR_RGB[4])
            elif (rank == 22): #diamond
                color = discord.Color.from_rgb(*self.COLOR_RGB[5])
            elif (rank == 23): #champion
                color = discord.Color.from_rgb(*self.COLOR_RGB[6])

            embed = discord.Embed(
                title = f"Rank: {player.statsAsia['rank_text']}",
                description = f"Level: {player.level}",
                color = color
            )
            if (player.statsAsia['rank'] != 23):
                linkRep = {'ranks': 'rank-imgs', 'svg': 'png'}
                rank_url = player.statsAsia['rank_image']
                for i, j in linkRep.items():
                    rank_url = rank_url.replace(i, j)
            else:
                rank_url = f"https://tabstats.com/images/r6/ranks/?rank=21&champ={player.statsAsia['champions_rank_position']}"
            icon_url = player.genericStats['avatar_url_146']
            embed.set_thumbnail(url=rank_url)
            embed.set_author(name=player.genericStats['username'], icon_url=icon_url)
            embed.add_field(name="Current MMR: ", value=f"{player.statsAsia['mmr']}", inline=False)
            embed.add_field(name="Ranked KD: ", value=player.statsAsia['kd'], inline=True)
            losses = 1 if player.statsAsia['losses'] == 0 else player.statsAsia['losses']
            # if player.statsAsia['losses'] == 0: losses = 1
            # else: losses = player.statsAsia['losses']
            embed.add_field(name="Wins/Losses: ", value="Wins: {}\n Losses: {}\n W/L: {}".format(player.statsAsia['wins'],
                    player.statsAsia['losses'],
                    "{:.2f}".format(player.statsAsia['wins'] / losses)),
                    inline=True
                )
            #embed.add_field(name="Casual KD: ", value="{:.2f}".format(player.genericStats['stats']['queue']['casual']['kd']), inline=True)
            embed.add_field(name="Overall KD: ", value="{:.2f}".format(player.genericStats['stats']['general']['kd']), inline=False)
            await ctx.send(embed=embed)

    @commands.command(help="r6 state with specific players")
    async def us(self, ctx, platform="pc"):
        players = []
        for username in self.def_playerList.keys():
            try:
                player = R6Stats(username, platform, generic=False)
            except Exception as e:
                await ctx.send("API is broken D:")
                print(e)
                return
            if (not player.seasonalStats):
                await ctx.send(f"Couldn't find user: {username}")
                continue
            else:
                #print(player.data['ranked']['mmr'])
                player.statsAsia['p_name'] = player.username
                players.append(player.statsAsia)
        players = sorted(players, key = lambda i: i['mmr'], reverse=True)
        desc = ""
        for i, e in enumerate(players):
            desc = desc + f"#{i+1} {e['p_name']} Rank: {e['rank_text']}({e['mmr']}) \n"
        # for i in range(len(players)):
        #     desc = desc + f"#{i+1} {players[i]['profile']['p_name']} Rank: {rankList[players[i]['ranked']['rank']]}({players[i]['mmr']}) \n"

        embed = discord.Embed(
            title = "Ranking Among Us:",
            description = desc
        )
        linkRep = {'ranks': 'rank-imgs', 'svg': 'png'}
        rank_url = players[0]['rank_image']
        for i, j in linkRep.items():
            rank_url = rank_url.replace(i, j)
        embed.set_thumbnail(url=rank_url)
        await ctx.send(embed=embed)

class R6Stats():
    def __init__(self, username, platform="pc", generic=True, seasonal=True):
        self.baseURL = 'https://api2.r6stats.com/public-api/stats/' #/<username>/<platform>/<type>
        self.headers = {'Authorization': 'Bearer ' + os.environ.get('R6STATS_KEY', '-1')}
        self.username = username
        self.platform = platform
        if (generic):
            self.genericStats = self.getStats(type="generic")
            try :
                self.level = self.genericStats['progression']['level']
            except Exception as e:
                print("Error : {} \nPlayer not found".format(e))
                return
        if (seasonal):
            self.seasonalStats = self.getStats(type="seasonal")
            self.statsAsia = self.seasonalStats['regions']['apac'][0]
            if self.statsAsia['deaths'] == 0:
                self.statsAsia['deaths'] = 1
            self.statsAsia['kd'] = "{:.2f}".format(self.statsAsia['kills'] / self.statsAsia['deaths'])

    def getStats(self, type="generic", season="crimson_heist"):
        formatURL = self.baseURL + "/".join([self.username, self.platform, type])
        #print(formatURL)
        resp = requests.get(formatURL, headers=self.headers)
        stats = json.loads(resp.text)
        print(resp.status_code, end=' ')
        print(resp.elapsed.total_seconds())
        if(resp.status_code != 200):
            print(stats['error'])
            return {}
        if (type=="seasonal"):
            self.writeToFile(stats, "./R6S/seasonal.txt")
            return stats['seasons'][season]
        else:
            self.writeToFile(stats, "./R6S/generic.txt")
            return stats

    def writeToFile(self, data, fileName):
        with open(fileName, 'w') as outfile:
            json.dump(data, outfile, indent=4)

def setup(bot):
    bot.add_cog(R6(bot))

#player = R6Stats("BenGorr")
def main():
    r6 = R6Stats('BenGorr')
    print(r6.statsAsia)

if __name__ == '__main__':
    main()
