import json
import yaml
import os
nodes = ['client','8000','8001','8002','8003','8004','8005','8006','8007','8008','8009']
routers = ['8000','8001','8002','8003','8004','8005','8006','8007','8008','8009']
from cryptography.fernet import Fernet
#8080 is the server client is a script and 800 0-9 are routers in between
keys = {}

for i in range(len(nodes)):
    keys[nodes[i]] = {}
    for j in range(len(nodes)):
        keys[nodes[i]][nodes[j]] = None

for i in range(len(nodes)):
    for j in range(i + 1,len(nodes)):

        key = Fernet.generate_key().decode('utf-8')
        keys[nodes[j]][nodes[i]] = key
        keys[nodes[i]][nodes[j]] = key

#put the keys in each router, client and server
try:

    for filename in os.listdir("./keys"):
        file_path = os.path.join("./keys",filename)

        if os.path.isfile(file_path):
            os.remove(file_path)

except Exception as e:
    print("an error has occured, build has failed")
    exit(0)

for ip in keys.keys():

    path = f'./keys/{ip}.json'

    with open(path,'w') as f:
        json.dump(keys[ip],f,indent=4)

path = f'./keys/all_keys.json'

with open(path,'w') as f:
    json.dump(keys,f,indent = 4)

#generate my docker-compose.yml


services = {}

for router in routers:
    services[f"router{router}"] = {
        "build":{
            "context":"./router"
        },
        "container_name":f"router{router}",
        "ports":[
            f"{router}:8000"
        ],
        "volumes":[
            f"./keys/{router}.json:/app/router/local_data/keys.json"
        ]
    }

docker_compose = {
    "version":"3.3",
    "services":services
}
with open("docker-compose.yml", "w") as f:
    f.write("version: '3.3'\n")
    yaml.dump({"services": services}, f, default_flow_style=False)

print("build finished")



