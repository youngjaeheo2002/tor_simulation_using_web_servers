"""
URL configuration for router project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
import requests
import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError, SchemaError
from django.views.decorators.csrf import csrf_exempt
from cryptography.fernet import Fernet
import os
import sys
from .utils import read_local_json
from .utils import write_payload
BASE = 'http://localhost:'
SERVER_ERROR = JsonResponse({"message":"something went wrong"},status = 500)
def ping(request):
    return JsonResponse({"message":"Router is active"})

@csrf_exempt
def routePackets(request):
    '''
    the body that is recieved shoudl look something like this

    {src_ip:"",
    dst_ip:"",
    encrypted_payload:""}
    '''
    '''
    at this current point teh payload is not encrypted
    '''
    # schema = {
    #     "type": "object",
    #     "properties": {
    #         "dst_ip": {"type": "string"},
    #         "encrypted_payload": {"type": "string"}
    #     },
    #     "required": ["dst_ip","encrypted_payload"]
    # }
    if request.method != 'POST':
        return SERVER_ERROR
    


    raw_body = request.body
    body_str = raw_body.decode('utf-8')
    print(raw_body)
    try:
        body_json = json.loads(body_str)
        write_payload(body_json,"payload_received.json")
        print(body_json,file = sys.stderr)
        # validate(instance=body_json,schema= schema)
        src_ip = body_json['src_ip']


        encrypted_payload = body_json['encrypted_payload'].encode('utf-8')
        
        #when encyrpted you put the code to decrypt using a shared key method
        key_path = os.path.join(os.path.dirname(__file__), "local_data", "data.json")
        print(read_local_json('keys.json'),file = sys.stderr)
        session_key = read_local_json('keys.json')[src_ip].encode()


        #after decryption
        cipher = Fernet(session_key)
        decrypted_payload = json.loads(cipher.decrypt(encrypted_payload).decode())

        write_payload(decrypted_payload,"decrypted_payload.json")
        dst_ip  = decrypted_payload['dst_ip']

        if (dst_ip == "server"):
            #re-encrypt response back to client
            response_body = response.content
            encrypted_response = cipher.encrypt(response_body).decode()
            send_backwards = {
                "encrypted_payload":encrypted_response
            }
            write_payload(send_backwards,"payload_sent_to_previous_layer.json")
            return JsonResponse({"message":"some content"})

        next_payload = decrypted_payload['encrypted_payload']

        write_payload({
            "src_ip":body_json['dst_ip'],
            "dst_ip":dst_ip,
            "encrypted_payload":next_payload},
            "payload_for_next_send.json")

        url = "http://router" + dst_ip+":8000"+ "/route_packets"
        response = requests.post(url,json={
            "src_ip":body_json['dst_ip'],
            "dst_ip":dst_ip,
            "encrypted_payload":next_payload})
        response.raise_for_status()


        return JsonResponse(send_backwards,safe = False)
    
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    except ValidationError as e:
        return JsonResponse({"error":"schema validation faield"},status = 400)
    
    except SchemaError as e:
        return JsonResponse({"error":"schema is invalid"},status = 400)
    
    except KeyError as e:
        return JsonResponse({'error':'something wrong with dicitonary key '},status = 400)
    

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ping',ping),
    path('route_packets',routePackets)
]
