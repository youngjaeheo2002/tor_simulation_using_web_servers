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
BASE = 'http://localhost:'
SERVER_ERROR = JsonResponse({"message":"something went wrong"},status = 500)
def ping(request):
    return JsonResponse({"message":"Router is active"})

def sendtoNext(dst_ip,payload,)
@csrf_exempt
def routePackets(request):
    '''
    the body that is recieved shoudl look something like this

    {src_ip:"",
    dst_ip:"",
    encrypted_payload:""}
    '''
    '''
    at thsi current point teh payload is not encrypted
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
    try:
        body_json = json.loads(body_str)
        # validate(instance=body_json,schema= schema)
        host = request.get_host()
        
        if not ":" in host:
            return SERVER_ERROR
        
        src_ip = host.split(":")[1]
        encrypted_payload = body_json['encrypted_payload']
        
        #when encyrpted you put the code to decrypt using a shared key method


        #after decryption

        dst_ip = encrypted_payload['dst_ip']
        if dst_ip == 'server':
            return JsonResponse({"message":"some content"})
        next_payload = encrypted_payload['encrypted_payload']

        try:
            url = BASE + dst_ip + "/route_packets"



        return JsonResponse({"message":"everything is good so far"})
    
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
