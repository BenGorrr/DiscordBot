import requests
import json


class R6():
    def __init__(self, name, platform="uplay"):
        self.name = name
        self.platform = platform

    def getStats(self):
        url = f'https://r6.apitab.com/search/{self.platform}/{self.name}'
        resp = requests.get(url)
        if (resp.status_code == 200):
            stats = json.loads(resp.text)
            if (not stats['foundmatch']):
                return {}
            else:
                #self.writeTofile(stats)
                return list(stats['players'].keys())[0]

    def writeTofile(self, stats):
        with open('data.txt', 'w') as outfile:
            json.dump(stats, outfile, indent=4)


def main():
    r61 = R6('BenGorrrr')
    r61.getStats()


if __name__ == '__main__':
    main()
