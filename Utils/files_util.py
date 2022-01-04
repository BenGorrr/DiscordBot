import json

def write_Json(file, data):
    with open(file, 'w') as outfile:
        json.dump(data, outfile, indent=4)

def read_Json(file):
    with open(file, 'r') as infile:
        #use try...except so we dont get error when the file is empty(it will return None if its empty)
        try:
            data = json.load(infile)
            return data
        except json.JSONDecodeError:
            pass