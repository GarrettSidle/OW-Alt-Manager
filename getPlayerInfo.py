import requests


def getPlayerInfo(user_data):
    
    base_url = f"https://overfast-api.tekrop.fr/players/{user_data['username']}/summary"

    response = requests.get(base_url)

    # Check if the request was unsuccessful
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None
    
    # Parse the JSON response
    player_data = response.json()
    
    
    if not player_data:
        print("Player not found.")
        return None
    
    print(f"Player found:{user_data['username']}")
    return player_data
