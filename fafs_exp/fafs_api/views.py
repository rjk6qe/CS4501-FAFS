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
            if path is not None:
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

def get_categories(request, pk=None):
    path_list = ['categories',pk]
    if pk is not None:
        path_list.append(pk)
    response = get_request(path_list)
    return JsonResponse(response)

def get_products(request, pk=None):
    path_list = ['products',pk]
    response = get_request(path_list)
    return JsonResponse(response)

def get_latest_products(request, num=None):
    if num is None:
        num = 3
    response = get_request(['products',])
    product_data = response['response']
    sorted_products = sorted(product_data, key = lambda x: x["time_posted"], reverse=True)[:int(num)]
    return JsonResponse(json_encode_dict_and_status(sorted_products, True))