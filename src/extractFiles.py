import os
import json

LOGINS_PATH  =  'logins.json'
CONFIG_PATH  =  'config.json'

def extractFiles():
    logins  = getJsonFile(LOGINS_PATH)
    config  = getJsonFile(CONFIG_PATH)
    return logins, config


def getJsonFile(filePath):
    # Check if the file exists
    if not os.path.isfile(filePath):
        # If the file doesn't exist, create it
        with open(filePath, 'w') as file:
            # Write an empty list as the initial content
            json.dump(default_data, file, indent=4)
        print(f"{filePath} created.")
    else:
        print(f"{filePath} already exists.")

    # Open the file and read the data
    with open(filePath, 'r') as file:
        data = json.load(file) 

    return data


default_data = [
    {
        "username": "Flats#11344",
        "password": "Put Email Here",
        "email": "Put Password Here"
    },
    {
        "username": "emongg#11183",
        "password": "Put Email Here",
        "email": "Put Password Here"
    },   
    {
        "username": "super#12850",
        "password": "Put Email Here",
        "email": "Put Password Here"
    },  
    {
        "username": "Jay3#11894",
        "password": "Put Email Here",
        "email": "Put Password Here"
    },  
    {
        "username": "mL7#21877",
        "password": "Put Email Here",
        "email": "Put Password Here"
    }
]