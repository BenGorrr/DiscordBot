import requests, json

class R6Stats():
    def __init__(self, username, platform="pc", generic=True, seasonal=True):
        self.baseURL = 'https://api2.r6stats.com/public-api/stats/' #/<username>/<platform>/<type>
        self.headers = {'Authorization': 'Bearer ***REMOVED***'}
        self.username = username
        self.platform = platform
        if (generic):
            self.genericStats = self.getStats(type="generic")
            self.level = self.genericStats['progression']['level']
        if (seasonal):
            self.seasonalStats = self.getStats(type="seasonal")
            self.statsAsia = self.seasonalStats['regions']['apac'][0]
            if self.statsAsia['deaths'] == 0:
                self.statsAsia['deaths'] = 1
            self.statsAsia['kd'] = round(self.statsAsia['kills'] / self.statsAsia['deaths'], 2)

    def getStats(self, type="generic", season="neon_dawn"):
        formatURL = self.baseURL + "/".join([self.username, self.platform, type])
        #print(formatURL)
        resp = requests.get(formatURL, headers=self.headers)
        stats = json.loads(resp.text)
        self.writeToFile(stats)
        print(resp.status_code, end=' ')
        print(resp.elapsed.total_seconds())
        if(resp.status_code != 200):
            print(stats['error'])
            return {}
        if (type=="seasonal"):
            return stats['seasons'][season]
        else:
            return stats

    def writeToFile(self, data):
        with open('data1.txt', 'w') as outfile:
            json.dump(data, outfile, indent=4)

#player = R6Stats("BenGorr")
def main():
    r6 = R6Stats('BenGorr')
    print(r6.statsAsia)


if __name__ == '__main__':
    main()
