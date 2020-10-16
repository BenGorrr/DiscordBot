import requests
import json


class R6():
    def __init__(self, name, platform):
        self.name = name
        self.platform = platform
        self.data = self.getStats()

    def getStats(self):
        url = f'https://r6.apitab.com/search/{self.platform}/{self.name}'
        print('Requesting to api')
        resp = requests.get(url)
        if (resp.status_code == 200):
            print('Request success (200)')
            stats = json.loads(resp.text)
            if (not stats['foundmatch']):
                print('Did not Found a match!')
                return {}
            else:
                self.writeTofile(stats)
                print('Found a match!')
                return stats['players'][list(stats['players'].keys())[0]]
        else:
            print('Request Error. Code: ', resp.status_code)
            return {}

    def writeTofile(self, stats):
        with open('data.txt', 'w') as outfile:
            json.dump(stats, outfile, indent=4)


def main():
    r61 = R6('BenGorrrr')
    r61.getStats()


if __name__ == '__main__':
    main()
