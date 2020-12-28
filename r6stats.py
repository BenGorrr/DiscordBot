import requests, json, config

class R6Stats():
    def __init__(self, username, platform="pc", generic=True, seasonal=True):
        self.baseURL = 'https://api2.r6stats.com/public-api/stats/' #/<username>/<platform>/<type>
        self.headers = {'Authorization': 'Bearer ' + config.r6stats_api_key}
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

    def getStats(self, type="generic", season="neon_dawn"):
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
            self.writeToFile(stats, "seasonal.txt")
            return stats['seasons'][season]
        else:
            self.writeToFile(stats, "generic.txt")
            return stats

    def writeToFile(self, data, fileName):
        with open(fileName, 'w') as outfile:
            json.dump(data, outfile, indent=4)

#player = R6Stats("BenGorr")
def main():
    r6 = R6Stats('BenGorr')
    print(r6.statsAsia)


if __name__ == '__main__':
    main()
