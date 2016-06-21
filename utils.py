import json

def read_config():
	with open('config.json') as data_file:    
		return json.load(data_file)

def read_searchConfig():
    with open('searchConfig.json') as data_file:
        return json.load(data_file)
        
def pretty_print(dict):
    print json.dumps(dict, indent=4, sort_keys=True)