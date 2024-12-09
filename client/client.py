import sys
import json
import random
from cryptography.fernet import Fernet
import requests
# Path to the JSON file
json_file_path = "keys/client.json"



MY_IP = "0.0.0.0"

DNS_TABLE = {
    'www.malicious.onion':"0.0.0.1",'www.regular_website.com':"0.0.0.2",'toronto_news.com':"0.0.0.3"
}

#normal request to website
def requestWithoutTor(dst):

    return


# Load keys from JSON file
keys = {}
with open("./keys/all_keys.json", "r") as f:
    keys = json.load(f)

# Function to simulate encrypting and sending data between routers
def create_encrypted_payload(src_ip, dst_ip, payload):
    # Extract the key for the current hop (src_ip -> dst_ip)
    key = keys[src_ip][dst_ip]
    
    if not key:
        print(f"Error: Key missing for {src_ip} -> {dst_ip}")
        return None

    cipher = Fernet(key)  # Initialize the cipher with the key
    payload_string = json.dumps(payload).encode()  # Convert payload to string
    encrypted_payload = cipher.encrypt(payload_string).decode()  # Encrypt the payload
    return encrypted_payload

# request picking three routers out of 10
def requestUsingTor(dst):
    # Randomly select three routers
    random_selection = random.sample(range(10), 3)
    first = "800" + str(random_selection[0])
    second = "800" + str(random_selection[1])
    third = "800" + str(random_selection[2])
    print(first,second,third)
    client = "client"

    p3 = {
        "payload": "Hi its Bob",
        "src_ip": third,
        "dst_ip": dst,
    }

    encrypted_p3 = create_encrypted_payload(second, third, p3)
    # Step 2: Encrypt payload from second router to third router
    p2 = {
        "encrypted_payload": encrypted_p3,
        "src_ip": second,
        "dst_ip": third,
    }
    
    encrypted_p2 = create_encrypted_payload(first, second, p2)
    # Step 3: Encrypt payload from first router to second router
    p1 = {
        "encrypted_payload": encrypted_p2,
        "src_ip": first,
        "dst_ip": second,
    }
    
    encrypted_p1 = create_encrypted_payload(client,first,p1)

    # Step 4: Encrypt payload from client to first router
    p0 = {
        "encrypted_payload": encrypted_p1,
        "src_ip": "client",
        "dst_ip": first,
    }

    #url = f"http://router{first}:8000/route_packets"
    # If you're running client.py on your host (outside Docker):
    url = "http://localhost:"+first+"/route_packets"
    response = requests.post(url, json=p0)
    print(response.content)
    # Send the HTTP POST request
    #response = requests.post(url, json={"encrypted_payload": encrypted_p0, "src_ip":"client","dst_ip": first})
    #response.raise_for_status()

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

    if DESTINATION not in ['www.malicious.onion','www.regular_website.com','www.toronto_news.com']:

        exit(0)

    if MODE == 'regular':

        requestWithoutTor(DESTINATION)
        exit(0)

    if MODE == 'tor':
        requestUsingTor(DESTINATION)
        
    





