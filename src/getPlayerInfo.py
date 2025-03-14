import requests
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import time

#Get info for all players
def getPlayersInfo(login):
    #create a thread for every coming API call
    with ThreadPoolExecutor() as executor:
        results = executor.map(partial(getPlayerInfo, timer=1), login)
    
    return list(results)

#Get info for individual player
def getPlayerInfo(user, timer):
    base_url = f"https://overfast-api.tekrop.fr/players/{user['username']}/summary"

    response = requests.get(base_url)
    
    #if we are overloading the server
    if response.status_code == 429:
        print(f"Overloaded retrying for: {user['username']}")
        #backoff and try again with longer intervals between
        time.sleep(timer)
        return getPlayerInfo(user, timer*2)

    #if the status code is not ok
    if response.status_code != 200:
        #print the error and conitnue
        print(f"Error: {response.status_code} for {user['username']}")
        return None
    
    player_data = response.json()

    if not player_data:
        print(f"Player not found: {user['username']}")
        return None
    
    print(f"Player found: {user['username']}")
    return player_data
