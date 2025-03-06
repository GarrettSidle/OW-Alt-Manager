import os
import json

LOGINS_PATH  = 'logins.json'
FRIENDS_PATH = 'freinds.json'

def extractFiles():
    logins  = getOrCreateLogins()
    friends = getOrCreatefriends()
    return logins, friends


def getOrCreateLogins():
    # Check if the file exists
    if not os.path.isfile(LOGINS_PATH):
        # If the file doesn't exist, create it
        with open(LOGINS_PATH, 'w') as file:
            # Write an empty list as the initial content
            file.write('[]')  # Empty JSON array
        print(f"{LOGINS_PATH} created.")
    else:
        print(f"{LOGINS_PATH} already exists.")

    # Open the file and read the data
    with open(LOGINS_PATH, 'r') as file:
        data = json.load(file)  # Parse the JSON data into a Python list

    # Print the data
    print("Data from the JSON file:")
    return data

def getOrCreatefriends():

    # Check if the file exists
    if not os.path.isfile(FRIENDS_PATH):
        # If the file doesn't exist, create it
        with open(FRIENDS_PATH, 'w') as file:
            # Write an empty list as the initial content
            file.write('[]')  # Empty JSON array
        print(f"{FRIENDS_PATH} created.")
    else:
        print(f"{FRIENDS_PATH} already exists.")

    # Open the file and read the data
    with open(FRIENDS_PATH, 'r') as file:
        data = json.load(file)  # Parse the JSON data into a Python list

    # Print the data
    print("Data from the JSON file:")
    return data