import os, requests, json

def get_random_image(tag):
    url = "https://api.ksoft.si/images/random-image?tag=" + tag
    headers = {'Authorization': 'Bearer ' + os.environ.get('KSOFT_KEY', '-1')}
    resp = requests.get(url, headers=headers)
    content = json.loads(resp.text)
    #print(content)
    if(resp.status_code != 200):
        print(content['message'])
        return
    return content["url"]
