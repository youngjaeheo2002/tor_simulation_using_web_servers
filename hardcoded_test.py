key = "neA7feaqsSXR_tdgOdiEWUnxYYDN1kss4MM4ufcbPes=".encode('utf-8')
import json
from cryptography.fernet import Fernet
import requests
cipher = Fernet(key)
payload_8003_to_server_string = json.dumps({
    "dst_ip":"server",
    "payload":"hello"
}).encode()
print(payload_8003_to_server_string)
encrypted_8003_to_server = cipher.encrypt(payload_8003_to_server_string).decode()

payload_8002_to_8003_string = json.dumps({
    "dst_ip":"8003",
    "encrypted_payload":encrypted_8003_to_server
}).encode()
print(payload_8002_to_8003_string)
encrypted_8002_to_8003 = cipher.encrypt(payload_8002_to_8003_string).decode()

payload_8001_to_8002_string = json.dumps({
    "dst_ip":"8002",
    "encrypted_payload":encrypted_8002_to_8003
}).encode()
print(payload_8001_to_8002_string)

encrypted_8001_to_8002 = cipher.encrypt(payload_8001_to_8002_string).decode()
payload_to_8001 = {
    "encrypted_payload":encrypted_8001_to_8002
}
print(payload_to_8001)

response = requests.post("http://localhost:8001/route_packets",json=payload_to_8001)

print(response.content)












