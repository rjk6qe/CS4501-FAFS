from django.shortcuts import render
from django.http import HttpResponse
import urllib.request
import urllib.parse
import json


def index(request):
                                                                                                                  
    print ("About to do the GET...")
    cat_req = urllib.request.Request('http://exp-api:8000/fafs/categories/')
    cat_resp_json = urllib.request.urlopen(cat_req).read().decode('utf-8')
    cat_resp = json.loads(cat_resp_json)
    product_req = urllib.request.Request('http://exp-api:8000/fafs/products/')
    product_resp_json = urllib.request.urlopen(product_req).read().decode('utf-8')
    product_resp = json.loads(product_resp_json)
    context_dict = {'categories': cat_resp, 'products' : product_resp }
    return render(request, 'fafs_api/index.html', context_dict)
