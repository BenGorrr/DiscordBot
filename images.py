import os, requests, json

def get_random_image(tag):
    url = "https://api.ksoft.si/images/random-image"
    headers = {'Authorization': 'Bearer ' + os.environ.get('KSOFT_KEY', '-1'), 'tag': tag}
    resp = requests.get(url, headers=headers)
    content = json.loads(resp.text)
    if(resp.status_code != 200):
        print(stats['error'])
        return
    return content["url"]
