from django.shortcuts import render
from django.http import HttpResponse
import urllib.request
import urllib.parse
import json
from fafs_api.forms import UserRegister

API_URL = 'http://exp-api:8000/fafs/'

def make_request(path):
    req = urllib.request.Request(API_URL + path)
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    return json.loads(resp_json)

def append_to_url(path_list):
    url = API_URL
    if path_list is not None:
        for path in path_list:
            if path is not None:
                url = url + str(path) + '/'
    return url

def get_request(path_list=None):
    url = append_to_url(path_list)
    #response = requests.get(url)
    req = urllib.request.Request(url)
    json_response = urllib.request.urlopen(req).read().decode('utf-8')
    return json.loads(json_response)

def post_request(path_list, data):
    url = append_to_url(path_list)
    post_encoded = urllib.parse.urlencode(data).encode('utf-8')
    #req = requests.post(url, json=data)
    req = urllib.request.Request(url, data=post_encoded, method='POST')
    #json_response = req.json()
    json_response = urllib.request.urlopen(req).read().decode('utf-8')
    return json_response

def index(request):

    cat_req = urllib.request.Request(API_URL + 'categories/')
    cat_resp_json = urllib.request.urlopen(cat_req).read().decode('utf-8')
    cat_resp = json.loads(cat_resp_json)
    latest_product_req = urllib.request.Request(API_URL + 'products/latest/3/')
    latest_product_resp_json = urllib.request.urlopen(latest_product_req).read().decode('utf-8')

    latest_product_resp = json.loads(latest_product_resp_json)
    context_dict = {'categories': cat_resp, 'products' : latest_product_resp }
    return render(request, 'fafs_api/index.html', context_dict)

def product_detail(request, pk):
    cat_resp = make_request('categories/')
    product_resp = make_request('products/' + pk)
    context_dict = {'categories': cat_resp, 'product': product_resp['response']}
    return render(request, 'fafs_api/product_detail.html', context_dict)

def category_detail(request, pk):
    cat_resp = get_request(['categories'])
    this_category = get_request(['categories', pk])
    context_dict = {'categories': cat_resp, 'category': this_category['response']}
    return render(request, 'fafs_api/category_detail.html', context_dict)


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserRegister(data=request.POST)
        if user_form.is_valid():
            result = {}
            result= user_form.cleaned_data
            user = post_request(['register'], result)
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserRegister()

    return render(request, 'fafs_api/register.html', {'user_form': user_form, 'registered': registered})
