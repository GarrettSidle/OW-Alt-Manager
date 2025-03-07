import requests
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import time

def getPlayersInfo(user_data):
    
    with ThreadPoolExecutor() as executor:
        results = executor.map(partial(getPlayerInfo, timer=1), user_data)
    
    return list(results)

def getPlayerInfo(user, timer):
    base_url = f"https://overfast-api.tekrop.fr/players/{user['username']}/summary"

    response = requests.get(base_url)
    
    if response.status_code == 429:
        print(f"Overloaded retrying for: {user['username']}")
        time.sleep(timer)
        return getPlayerInfo(user, timer*2)

    if response.status_code != 200:
        print(f"Error: {response.status_code} for {user['username']}")
        return None
    
    player_data = response.json()

    if not player_data:
        print(f"Player not found: {user['username']}")
        return None
    
    print(f"Player found: {user['username']}")
    return player_data
