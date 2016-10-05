from django.shortcuts import render
import urllib.request
import urllib.parse
#import requests
import json
from django.http import HttpResponse, JsonResponse

# Create your views here.
API_URL = 'http://models-api:8000/api/'


def append_to_url(path_list):
    url = API_URL
    if path_list is not None:
        for path in path_list:
            url = url + str(path) + '/'
    return url    

def make_request(path):
    req = urllib.request.Request(API_URL + path)
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    return json.loads(resp_json)

def get_request(path_list=None):
    url = append_to_url(path_list)
    #response = requests.get(url)
    req = urllib.request.Request(url)
    json_response = urllib.request.urlopen(req).read().decode('utf-8')
    return json.loads(json_response)

def post_request(path_list, data):
    url = append_to_url(path_list)
    return response.json()

def json_encode_dict_and_status(dictionary, status):
    response_dict = {}
    response_dict["status"] = status
    response_dict["response"] = dictionary
    return response_dict

def getCategories(request):
    response = get_request(['categories',])
    return JsonResponse(response)

def getProducts(request):
    response = get_request(['products',])
    return JsonResponse(response)

def getProduct(request, pk):
    response = get_request(['products',pk])
    return JsonResponse(response)

def getLatestProducts(request, num=3):
    response = get_request(['products',])
    product_data = response['response']
    sorted_products = sorted(product_data, key = lambda x: x["time_posted"], reverse=True)[:int(num)]
    return JsonResponse(json_encode_dict_and_status(sorted_products, True))