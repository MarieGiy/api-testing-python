import requests
import bitly_cli

HERMIONE_GRANGER_API = 'https://hp-api.onrender.com/api/character/4c7e6819-a91a-45b2-a454-f931e4a7cce3'

######## INTEGRATION SUITES ########
# FYI: <.../shorten> -  only shorts link (no meta data setup), will be used in all flows but CREATE
def shorten_payload():
    return {'long_url': HERMIONE_GRANGER_API}
 
# RETRIEVE Flow
def test_can_retrieve_bit_link():
    # shorten link
    shorten_resp = bitly_cli.shorten_link(shorten_payload())
    # for simplicity sake first call retruns 201:created, all next: 200:ok for same <long_url> 
    assert shorten_resp.status_code in (201, 200)
    
    # retrive bit_link
    shorten_dict = shorten_resp.json()
    retrive_resp = bitly_cli.retrieve_link(shorten_dict['id'])
    
    # check retrived data
    assert retrive_resp.status_code == 200
    # hust rough check for keeping guide simple
    assert shorten_dict['link'] == retrive_resp.json()['link']
    
# CREATE Flow
def test_can_create_bit_link():
    create_payload = {
        'long_url': HERMIONE_GRANGER_API,
        'title': 'Wingardium Leviosa',
        'tags': ['Hermy', 'Know-it-all', 'Miss Grant', 'Herm-own-ninny']
    }

    # retrive Hermione data from HPAPI
    hermione_resp = requests.get(HERMIONE_GRANGER_API)
    assert hermione_resp.status_code == 200

    # returns 0-length list
    hermione_dict = hermione_resp.json()[0]    
    
    # create bit_link
    create_resp = bitly_cli.create_link(create_payload)
    # for simplicity sake first call retruns 201:created, all next: 200:ok for for same <long_url> 
    assert create_resp.status_code in (201, 200)
    
    # check created data
    create_dict = create_resp.json()
    assert create_dict['long_url'] == create_payload['long_url']
    assert create_dict['title'] == create_payload['title']
    assert create_dict['tags'] == create_payload['tags']

    # retrieve created data
    retrive_resp = bitly_cli.retrieve_link(create_dict['id'])
    assert retrive_resp.status_code == 200

    # check created data against retrieved
    assert create_dict['link'] == retrive_resp.json()['link']
    
    # check bit_link validity
    hermione_bitly = requests.get(create_dict['link'])
    assert hermione_dict == hermione_bitly.json()[0]

# UPDATE Flow
def test_can_update_bit_link():
    # shorten link
    shorten_resp = bitly_cli.shorten_link(shorten_payload())
    assert shorten_resp.status_code in (201, 200)
    
    # check if current value doesn't match one for edit
    shorten_dict = shorten_resp.json()
    leviosa = "it's leviosa not leviosa"    
    assert shorten_dict.get('title') == None

    # update bit_link
    uppdate_resp = bitly_cli.update_link(shorten_dict['id'], {'title': leviosa})
    assert uppdate_resp.status_code == 200
    assert uppdate_resp.json()['title'] == leviosa

    # validate updated data via retrieve api
    retrive_resp = bitly_cli.retrieve_link(shorten_dict['id'])
    retrive_dict = retrive_resp.json()
    assert retrive_resp.status_code == 200
    assert retrive_dict['title'] == leviosa
    assert retrive_dict['long_url'] == HERMIONE_GRANGER_API

# DELETE Flow
def test_can_delete_bit_link():
    # shorten link
    shorten_resp = bitly_cli.shorten_link(shorten_payload())
    shorten_dict = shorten_resp.json()
    # for simplicity sake first call retruns 201:created, all next: 200:ok for for same <long_url> 
    assert shorten_resp.status_code in (201, 200)
    
    # delete bit_link
    delete_resp = bitly_cli.delete_link(shorten_dict['id'])    
    assert delete_resp.status_code == 200
    
    # validate deletion via retrieve api
    retrive_resp = bitly_cli.retrieve_link(shorten_dict['id'])
    assert retrive_resp.status_code == 410
