from django.shortcuts import render
import urllib.request
import urllib.parse
import requests
import json
from django.http import HttpResponse, JsonResponse
from django.utils import dateparse
from django.contrib.humanize.templatetags.humanize import naturalday
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Create your views here.
API_URL = 'http://models-api:8000/api/v1/'


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
    post_encoded = urllib.parse.urlencode(data).encode('utf-8')
    req = requests.post(url, json=data)
    #req = urllib.request.Request(url, data=post_encoded, method='POST')
    json_response = req.json()
    #urllib.request.urlopen(req).read().decode('utf-8')
    #return json.loads(json_response)
    return json_response

def json_encode_dict_and_status(dictionary, status):
    response_dict = {}
    response_dict["status"] = status
    response_dict["response"] = dictionary
    return response_dict

DATE_FORMAT = '%b %d, %Y %H:%M %p'

def obj_date_to_string(obj, field_list):
    if isinstance(obj, dict):
        for field in field_list:
            str_datetime = dateparse.parse_datetime(obj[field])
            obj[field + '_readable'] = str_datetime.strftime(DATE_FORMAT)
    elif isinstance(obj, list):
        for item in obj:
            for field in field_list:
                str_datetime = dateparse.parse_datetime(item[field])
                item[field + '_readable'] = str_datetime.strftime(DATE_FORMAT)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))

        email = json_data.get('email', None)
        password = json_data.get('password', None)
        post_data = {
            'email': email,
            'password': password
        }

        if email and password:
            print("making request")
            response = post_request(['login'], post_data)
            if response['status']:
                authenticator = {"authenticator": response['response']['token']}
                return JsonResponse(json_encode_dict_and_status(authenticator, True))
            else:
                return JsonResponse(response)
        else:
            data = {"message": "Missing email/password"}
            return JsonResponse(data, False)

def get_categories(request, pk=None):
    path_list = ['categories',pk]
    response = get_request(path_list)
    if pk:
        category_data = response['response']
        path_list = ['products']
        response = get_request(path_list)
        product_data = response['response']
        product_list = []
        for product in product_data:
            if product['category_id'] == int(pk):
                product_list.append(product)
        obj_date_to_string(product_list, ['time_posted', 'time_updated'])
        category_data['product_list'] = product_list
        return JsonResponse(json_encode_dict_and_status(category_data, True))
    else:
        return JsonResponse(response)

def get_products(request, pk=None):
    print('Getting products')
    path_list = ['products',pk]
    response = get_request(path_list)
    product_data = response['response']
    obj_date_to_string(product_data, ['time_posted', 'time_updated'])

    # Get name of category from id
    path_list = ['categories', product_data['category_id']]
    response = get_request(path_list)
    category_data = response['response']
    product_data['category_name'] = category_data['name']

    # Get owner info from id
    path_list = ['users', product_data['owner_id']]
    response = get_request(path_list)
    owner_data = response['response']
    product_data['owner'] = owner_data

    return JsonResponse(json_encode_dict_and_status(product_data, True))

def get_latest_products(request, num=None):
    if num is None:
        num = 3
    response = get_request(['products',])
    product_data = response['response']
    print(type(product_data))
    sorted_products = sorted(product_data, key = lambda x: x["time_posted"], reverse=True)[:int(num)]
    return JsonResponse(json_encode_dict_and_status(sorted_products, True))


def register_user(request):
    #response = post_request(['users',])
    post_data = {"email": "tanul@email.com", "password": "password555", "school_id": "1", "phone_number": "555-555-5555", "pk" : "9"}
    post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
    req = urllib.request.Request('http://models-api:8000/api/v1/users/', data=post_encoded, method='POST')
    resp_json = urllib.request.urlopen(req).read()
    #resp = json.loads(resp_json)
    return JsonResponse(json_encode_dict_and_status(post_data, True))
