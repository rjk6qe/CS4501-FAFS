from django.shortcuts import render
import urllib.request
import urllib.parse
import json
from django.http import HttpResponse, JsonResponse

# Create your views here.
API_URL = 'http://models-api:8000/api/'

def json_encode_dict_and_status(dictionary, status):
	response_dict = {}
	response_dict["status"] = status
	response_dict["response"] = dictionary
	return response_dict

def getCategories(request):

    req = urllib.request.Request('http://models-api:8000/api/categories/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    #resp = json.loads(resp_json)
    return HttpResponse(resp_json)

def getProducts(request):

    req = urllib.request.Request('http://models-api:8000/api/products/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    #resp = json.loads(resp_json)
    return HttpResponse(resp_json)

def getLatestProducts(request, num=3):
    req = urllib.request.Request(API_URL + 'products/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    product_data = resp['response']
    sorted_products = sorted(product_data, key = lambda x: x["time_posted"], reverse=True)[:int(num)]

    return JsonResponse(json_encode_dict_and_status(sorted_products, True))
