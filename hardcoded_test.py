import json

keys = {}
with open("./keys/all_keys.json","r") as f:
    keys = json.load(f)

from cryptography.fernet import Fernet
import requests
key = keys["8002"]["8003"]
cipher = Fernet(key)
payload_8003_to_server_string = json.dumps({
    "dst_ip":"server",
    "src_ip":"8003",
    "payload":"hello"
}).encode()
print(payload_8003_to_server_string)
encrypted_8003_to_server = cipher.encrypt(payload_8003_to_server_string).decode()

key = keys["8001"]["8002"]
cipher = Fernet(key)
payload_8002_to_8003_string = json.dumps({
    "dst_ip":"8003",
    "src_ip":"8002",
    "encrypted_payload":encrypted_8003_to_server
}).encode()
print(payload_8002_to_8003_string)
encrypted_8002_to_8003 = cipher.encrypt(payload_8002_to_8003_string).decode()

key = keys["client"]["8001"]
cipher = Fernet(key)
payload_8001_to_8002_string = json.dumps({
    "src_ip":"8001",
    "dst_ip":"8002",
    "encrypted_payload":encrypted_8002_to_8003
}).encode()
print(payload_8001_to_8002_string)

encrypted_8001_to_8002 = cipher.encrypt(payload_8001_to_8002_string).decode()


payload_to_8001 = {
    "encrypted_payload":encrypted_8001_to_8002,
    "src_ip":"client",
    "dst_ip":"8001",
}
print(payload_to_8001)

response = requests.post("http://localhost:8001/route_packets",json=payload_to_8001)

print(response.content)












