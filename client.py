import json
routers = ['8000','8001','8002','8003','8004','8005','8006','8007','8008','8009']
keys = {}
with open("./keys/all_keys.json","r") as f:
    keys = json.load(f)

from cryptography.fernet import Fernet
import requests
import random
random_selection = random.sample(range(10), 3)
first = "800" + str(random_selection[0])
second = "800" + str(random_selection[1])
third = "800" + str(random_selection[2])
print(f"The total list of nodes are f{routers}")
print(f"A crucial part of the TOR is randomly selecting a 3 nodes path. The path chosen is {first}->{second}->{third}->server")

original_payload = {
    "message":"hello"
}
print(f"The payload that we want to send to the server is {original_payload}")

#encrypting second to third
print(f"First we are going to encrypt the payload using the session keys between routers {second} and {third}")
key = keys[second][third]
cipher = Fernet(key)
payload_from_third_to_server = json.dumps({
    "dst_ip":"server",
    "src_ip":third,
    "payload":original_payload
},indent = 4)

print(f"The payload that router {third} recieves and sends to the server will be \n{payload_from_third_to_server}")
encrypted_third_to_server = cipher.encrypt(payload_from_third_to_server.encode()).decode()

print(f"The encrypted payload that will be received by {third} and sent to server is {encrypted_third_to_server}")

#encrypting second to third
key = keys[first][second]
cipher = Fernet(key)
print()
print(f"Next we are going to encrypt the payload using the session keys between routers {first} and {second}")
payload_from_second_to_third = json.dumps({
    "dst_ip":third,
    "src_ip":second,
    "encrypted_payload":encrypted_third_to_server
},indent=4)

print(f"The payload that router {second} recieves and sends to router {third} will be \n{payload_from_second_to_third}")

encrypted_second_to_third = cipher.encrypt(payload_from_second_to_third.encode()).decode()

print(f"The encrypted payload that will be received by {second} and sent to {third} is {encrypted_second_to_third}")

#encrypting first and second
key = keys["client"][first]
cipher = Fernet(key)
print()
print(f"Next we are going to encrypt the payload using the session keys between the client and router {first}")
payload_from_first_to_second = json.dumps({
    "dst_ip":second,
    "src_ip":first,
    "encrypted_payload":encrypted_second_to_third
},indent = 4)

print(f"The payload that router {first} recieves from client and sends to router {second} will be \n{payload_from_first_to_second}")

encrypted_first_to_second = cipher.encrypt(payload_from_first_to_second.encode()).decode()

print(f"The encrypted payload that will be received by {first} and sent to {second} is {encrypted_second_to_third}")

#client to first
print()
payload_client_to_first = {
    "dst_ip":first,
    "src_ip":"client",
    "encrypted_payload":encrypted_first_to_second
}
print(f"The payload that router {first} recieves from client is {payload_client_to_first}")

response = requests.post(f"http://localhost:{first}/route_packets",json=payload_client_to_first)

print(f"An important thing to know is that routers will encrypt their responses back using the session key of themselves and the router or client that sent them a payload")
print(f"The payload recieved from the first router: {first} is {response.content}")
print(f"To see the response from the server to the third router: {third} we must decrypt the response three times")

print()

print(f"First we decrypt the response using the session key between client and router {first}")


first_response = json.loads(response.content.decode())

key = keys["client"][first]
cipher = Fernet(key)

after_first_decryption = json.loads(cipher.decrypt(first_response['encrypted_payload']).decode())
print()
print(f"After the first decryption using the session key between the client and first router, we have this : \n{after_first_decryption}")

key = keys[first][second]
cipher = Fernet(key)

after_second_decryption = json.loads(cipher.decrypt(after_first_decryption['encrypted_payload']).decode())
print()
print(f"After the second decryption using the session key between the first router and the second router, we have this: \n{after_second_decryption}")

# key = keys["8002"]["8003"]
# cipher = Fernet(key)
# after_third_decryption = json.loads(cipher.decrypt(after_second_decryption['encrypted_payload']).decode())

# print(f"after third decryption: {after_third_decryption}")

key = keys[second][third]
cipher = Fernet(key)

after_third_decryption = json.loads(cipher.decrypt(after_second_decryption['encrypted_payload']).decode())
print()
print(f"After the third decryption using the session key between the second router and the third router, we have this: \n{after_third_decryption}")

print(f"Now we have the response from the server that shows us that it recieved our original payload. The important part is that the server cannot see that the request original came from this client file since we routed it to 3 different nodes before sending it to the server. This allows for anonymity.")










# key = keys["8002"]["8003"]
# cipher = Fernet(key)
# payload_8003_to_server_string = json.dumps({
#     "dst_ip":"server",
#     "src_ip":"8003",
#     "payload":"hello"
# }).encode()
# print(payload_8003_to_server_string)
# encrypted_8003_to_server = cipher.encrypt(payload_8003_to_server_string).decode()

# key = keys["8001"]["8002"]
# cipher = Fernet(key)
# payload_8002_to_8003_string = json.dumps({
#     "dst_ip":"8003",
#     "src_ip":"8002",
#     "encrypted_payload":encrypted_8003_to_server
# }).encode()
# print(payload_8002_to_8003_string)
# encrypted_8002_to_8003 = cipher.encrypt(payload_8002_to_8003_string).decode()

# key = keys["client"]["8001"]
# cipher = Fernet(key)
# payload_8001_to_8002_string = json.dumps({
#     "src_ip":"8001",
#     "dst_ip":"8002",
#     "encrypted_payload":encrypted_8002_to_8003
# }).encode()
# print(payload_8001_to_8002_string)

# encrypted_8001_to_8002 = cipher.encrypt(payload_8001_to_8002_string).decode()


# payload_to_8001 = {
#     "encrypted_payload":encrypted_8001_to_8002,
#     "src_ip":"client",
#     "dst_ip":"8001",
# }
# print(payload_to_8001)

# response = requests.post("http://localhost:8001/route_packets",json=payload_to_8001)

# print(response.content)
# first_response = json.loads(response.content.decode())
# print(first_response)
# print("decrypting once")

# key = keys["client"]["8001"]
# cipher = Fernet(key)

# after_first_decryption = json.loads(cipher.decrypt(first_response['encrypted_payload']).decode())

# print(f"After first decryption: {after_first_decryption}")

# key = keys["8001"]["8002"]
# cipher = Fernet(key)

# after_second_decryption = json.loads(cipher.decrypt(after_first_decryption['encrypted_payload']).decode())

# print(f"After second decryption: {after_second_decryption}")

# key = keys["8002"]["8003"]
# cipher = Fernet(key)
# after_third_decryption = json.loads(cipher.decrypt(after_second_decryption['encrypted_payload']).decode())

# print(f"after third decryption: {after_third_decryption}")













