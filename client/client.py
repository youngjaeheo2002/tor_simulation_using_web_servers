import sys
import json
import random

# Path to the JSON file
json_file_path = "keys/client.json"



MY_IP = "0.0.0.0"

DNS_TABLE = {
    'www.malicious.onion':"0.0.0.1",'www.regular_website.com':"0.0.0.2",'toronto_news.com':"0.0.0.3"
}

#normal request to website
def requestWithoutTor(dst):

    return


# request picking three routers out of 10
def requestUsingTor(dst):
    # Randomly select three routers
    random_selection = random.sample(range(10), 3)
    first = "800" + str(random_selection[0])
    second = "800" + str(random_selection[1])
    third = "800" + str(random_selection[2])

    # Load the JSON file with keys
    json_file_path = "keys/client.json"
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Retrieve public keys for each router
    key_first = data.get(first)
    key_second = data.get(second)
    key_third = data.get(third)

    return

if __name__ == "__main__":

    args = sys.argv

    #first argument is client.py, second is mode and third is serverlocation

    if len(args) != 3:

        exit(0)


    MODE = args[1]

    if not MODE in ['tor','regular']:

        exit(0)

    DESTINATION = args[2]

    if DESTINATION not in ['www.malicious.onion','www.regular_website.com','toronto_news.com']:

        exit(0)

    if MODE == 'regular':

        requestWithoutTor(DESTINATION)
        exit(0)

    if MODE == 'tor':
        requestUsingTor(DESTINATION)
        
    





