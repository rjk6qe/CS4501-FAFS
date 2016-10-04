from django.shortcuts import render
from django.http import HttpResponse
import urllib.request
import urllib.parse
import json


def index(request):
    #return HttpResponse("Hello, world. You're at the polls index.")
                                                                                                                  
    print ("About to do the GET...")
    req = urllib.request.Request('http://exp-api:8000/fafs/categories/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    print(resp)
    context_dict = {'contents': resp}
    return render(request, 'fafs_api/index.html', context_dict)
