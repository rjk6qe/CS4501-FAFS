from django.shortcuts import render
from django.http import HttpResponse
import urllib.request
import urllib.parse
import json

API_URL = 'http://exp-api:8000/fafs/'

def index(request):

    print ("About to do the GET...")
    cat_req = urllib.request.Request(API_URL + 'categories/')
    cat_resp_json = urllib.request.urlopen(cat_req).read().decode('utf-8')
    cat_resp = json.loads(cat_resp_json)
    print('requesting the products')
    latest_product_req = urllib.request.Request(API_URL + 'products/latest/3/')
    latest_product_resp_json = urllib.request.urlopen(latest_product_req).read().decode('utf-8')

    print(latest_product_resp_json)
    latest_product_resp = json.loads(latest_product_resp_json)
    context_dict = {'categories': cat_resp, 'products' : latest_product_resp }
    return render(request, 'fafs_api/index.html', context_dict)
