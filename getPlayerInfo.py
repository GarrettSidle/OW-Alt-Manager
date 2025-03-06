import requests


def getPlayerInfo(user_data):
    return_data = None
    
    base_url = f"https://overfast-api.tekrop.fr/players/{user_data['username']}/summary"

    response = requests.get(base_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        player_data = response.json()
        
        # Print the player's data (or just the player_id if you need it)
        if player_data:
            print("Player found:")
            print(player_data)
            return_data = player_data
            
        else:
            print("Player not found.")
    else:
        print(f"Error: {response.status_code}")
        
    return return_data