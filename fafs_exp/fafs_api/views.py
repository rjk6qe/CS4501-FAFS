from django.shortcuts import render
import urllib.request
import urllib.parse
import json
from django.http import HttpResponse

# Create your views here.

def getCategory(request):
                                                                                                                  
    print ("About to do the GET...")
    req = urllib.request.Request('http://models-api:8000/api/categories/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    #resp = json.loads(resp_json)
    return HttpResponse(resp_json)
