import json
import requests

# swapi setup
SWAPI_URL = 'https://swapi.dev/api'
SW_PEOPLE = SWAPI_URL + '/people/'

# bit_link setup
BIT_LINK_API_URL = 'https://api-ssl.bitly.com/v4'
SHORTEN_ENDPOINT = BIT_LINK_API_URL + "/shorten"
ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'
HEADERS = { 'Authorization': f'Bearer {ACCESS_TOKEN}', 'Content-Type': 'application/json'}

# get api cli
def get_req_cli(url):
  response = requests.get(url)
  rez_obj = json.loads(response.text)

  return(rez_obj)

# bit_link shoreten api cli
def shorten_link(url):
  payload = {'long_url': url}
  data = json.dumps(payload)
  
  response = requests.post(SHORTEN_ENDPOINT, headers=HEADERS, data=data)
  
  result = json.loads(response.text)
  
  bit_link = result['link']

  return(bit_link)

# obi_wan swapi id
obi_wan = SW_PEOPLE + '10' 
# get obi_wan data from swapi with long url
swapi_url_obj = get_req_cli(obi_wan)  

# bit_link shorten obi_wan url
bit_link = shorten_link(obi_wan)

# get obi_wan data with bit_link shorten url
bit_link_url_obj = get_req_cli(bit_link)

# compare result
print(bit_link_url_obj == swapi_url_obj)
