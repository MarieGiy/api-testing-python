# Simple BitLink API client
 
import requests
from dotenv import dotenv_values

config = dotenv_values('.env')

BIT_LINK_API = 'https://api-ssl.bitly.com/v4'
SHORTEN_URL = BIT_LINK_API + '/shorten'
BITLINKS_URL = BIT_LINK_API + '/bitlinks/'
# Loaded via <.env>
AUTH = { 'Authorization': 'Bearer ' + config['ACCESS_TOKEN'] }

# POST <.../shorten>
# 201 - Created | Init create
# 200 - Ok | All following for same long URL
def shorten_link(data):
    return requests.post(SHORTEN_URL, headers=AUTH, json=data)

# GET <.../bitlinks/<YOUR_BITLINK>
# 200 - Ok
# 410 - Gone
def retrieve_link(bit_link):
    return requests.get(BITLINKS_URL + bit_link, headers=AUTH)

# POST <.../bitlinks/<YOUR_BITLINK>
# 201 - Created
# 200 - Ok
def create_link(data):
    return requests.post(BITLINKS_URL, headers=AUTH, json=data)

# PATCH <.../bitlinks/<YOUR_BITLINK>
# 200 - Ok
def update_link(bit_link, data):
    return requests.patch(BITLINKS_URL + bit_link, headers=AUTH, json=data)

# DELETE <.../bitlinks/<YOUR_BITLINK>
# 200 - Ok
def delete_link(bit_link):
    return requests.delete(BITLINKS_URL + bit_link, headers=AUTH)
