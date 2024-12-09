import os
import json

def read_local_json(file_name):
    file_path = os.path.join(os.path.dirname(__file__), "local_data", file_name)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_name} not found.")
    with open(file_path, "r") as json_file:
        return json.load(json_file)

def write_payload(payload,file_name):

    path = os.path.join(os.path.dirname(__file__),"local_data",file_name)
    try:
        with open(path,"w") as file:
            json.dump(payload, file, indent = 4)

    except Exception as e:
        print(f"An error has occured: {e}")

    return