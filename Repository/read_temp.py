from urllib import response
import requests
import json

URL = ''

def get_temp():
    response = requests.get(URL)  # request data from this side 
    return json.loads(response.text) #load that data with json and return/convert to text 
