from django.shortcuts import render
import urllib.request
import urllib.parse
import requests
import json
import redis
from django.http import HttpResponse, JsonResponse
from django.utils import dateparse
from django.utils.timezone import now, localtime
from django.contrib.humanize.templatetags.humanize import naturalday
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.serializers.json import DjangoJSONEncoder
from elasticsearch import Elasticsearch

from kafka import KafkaProducer

# Create your views here.
API_URL = 'http://models-api:8000/api/v1/'
CACHE_EXP_TIME_SECS = 3600 # Default 1 hour

redis_cache = redis.StrictRedis(host='redis', port=6379, db=0)

# Paths that will be cached
# If a GET request is made, the cache is checked
# If a POST request is made, the cache is cleared
CACHE_PATHS = ['products', 'users', 'categories']


es = Elasticsearch(['es'])

def append_to_url(path_list):
    url = API_URL
    if path_list is not None:
        for path in path_list:
            if path is not None:
                url = url + str(path) + '/'
    return url

def redis_key_name(path_list):
    key_name = None
    if path_list:
        if path_list[0] in CACHE_PATHS:
            key_name = ''
            for path in path_list:
                if path is not None:
                    key_name = key_name + str(path) + ':'
            key_name = key_name[:-1]
    return key_name

def get_request(path_list=None):
    url = append_to_url(path_list)
    key_name = redis_key_name(path_list)
    json_response = None
    if key_name:
        # If path is cacheable, see if it is in the cache
        key_name = redis_key_name(path_list)
        json_response = redis_cache.get(key_name)

    if not json_response:
        req = urllib.request.Request(url)
        json_response = urllib.request.urlopen(req).read().decode('utf-8')
        if key_name:
            print("Setting cache: " + key_name)
            redis_cache.set(key_name, json_response)
            redis_cache.expire(key_name, CACHE_EXP_TIME_SECS)
    else:
        json_response = json_response.decode('utf-8')
        print("From cache:" + key_name)
    return json.loads(json_response)

def post_request(path_list, data):
    key_name = redis_key_name(path_list)
    url = append_to_url(path_list)
    req = requests.post(url, data=json.dumps(data, cls=DjangoJSONEncoder))
    json_response = req.json()
    # If a change has been made to a cacheable path (via post request) clear the cache
    if key_name:
        redis_cache.flushall()
    return json_response

def delete_request(path_list):
    url = append_to_url(path_list)
    req = requests.delete(url)
    json_response = req.json()
    return json_response

def json_encode_dict_and_status(dictionary, status):
    response_dict = {}
    response_dict["status"] = status
    response_dict["response"] = dictionary
    return response_dict

DATE_FORMAT = '%b %d, %Y %H:%M %p'
DAYS_BEFORE_EXPIRE = 1

def obj_date_to_string(obj, field_list):
    if isinstance(obj, dict):
        for field in field_list:
            datetime_obj = localtime(dateparse.parse_datetime(obj[field]))
            obj[field + '_readable'] = datetime_obj.strftime(DATE_FORMAT)
    elif isinstance(obj, list):
        for item in obj:
            for field in field_list:
                str_datetime = localtime(dateparse.parse_datetime(item[field]))
                item[field + '_readable'] = str_datetime.strftime(DATE_FORMAT)

@csrf_exempt
def login(request):
    status = False
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        email = json_data.get('email', None)
        password = json_data.get('password', None)
        post_data = {
            'email': email,
            'password': password
        }

        if email and password:
            # Call model layer to verify password
            post_response = post_request(['users', 'check_pass'], post_data)
            if post_response['status']:
                user_id = post_response['response']['user_id']
                # Create authenticator based on user id
                post_data = {"user_id": user_id}
                post_response = post_request(['auth'], post_data)
                # Get token back
                token = post_response['response']['token']
                status = True
                response_data = {"authenticator": token}
            else:
                response_data = post_response['response']
        else:
            response_data = {"message": "Missing email/password"}
    else:
        response_data = {"message": "Must be a POST request"}
    return JsonResponse(json_encode_dict_and_status(response_data, status))

@csrf_exempt
def logout(request):
    status = False
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        authenticator = json_data.get('authenticator', None)
        if authenticator:
            # Delete authenticator
            response = delete_request(['auth', authenticator])
            if response['status']:
                response_data = {"message": "logout success"}
                status = True
            else:
                response_data = response['response']
        else:
            response_data = {"message": "Missing authenticator"}
    else:
        response_data = {"message": "Must be a POST request"}
    return JsonResponse(json_encode_dict_and_status(response_data, status))

@csrf_exempt
def auth_check(request):
    status = False
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        authenticator = json_data.get('authenticator', None)
        post_data = {
            'authenticator': authenticator
        }
        if authenticator:
            # Check authenticator
            post_response = post_request(['auth_check'], post_data)
            if post_response['status']:
                # Check to see if authenticator is too old
                auth = get_request(['auth', authenticator])['response']

                datetime = dateparse.parse_datetime(auth['date_created'])
                time_diff = (now() - datetime).days
                if time_diff > DAYS_BEFORE_EXPIRE:
                    delete_request(['auth', authenticator])
                    response_data = {"message": "Expired authenticator"}
                else:
                    # Get user based on returned user id
                    user_id = post_response['response']['user_id']
                    get_response = get_request(['users', user_id])
                    if get_response['status']:
                        status = True
                        # Take out password data
                        get_response['response'].pop('password', None)
                    response_data = get_response['response']
            else:
                response_data = post_response['response']
        else:
            response_data = {"message": "Missing authenticator"}
    else:
        response_data = {"message": "Must be a POST request!"}
    return JsonResponse(json_encode_dict_and_status(response_data, status))

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
    status = False
    path_list = ['products',pk]
    response = get_request(path_list)
    product_data = response['response']
    if response['status']:
        obj_date_to_string(product_data, ['time_posted', 'time_updated'])
        if pk:
            # Get name of category from id
            path_list = ['categories', product_data['category_id']]
            response = get_request(path_list)
            category_data = response['response']
            product_data['category_name'] = category_data['name']

            # Get owner info from id
            path_list = ['users', product_data['owner_id']]
            response = get_request(path_list)
            owner_data = response['response']
            owner_data.pop('password', None)
            product_data['owner'] = owner_data
        status = True
    else:
        product_data = {'message': 'Invalid product id'}

    return JsonResponse(json_encode_dict_and_status(product_data, status))

def create_product(request):
    if request.method == "POST":
        json_data = json.loads(request.body.decode('utf-8'))
        post_data = {
            'name': json_data['name'],
            'description': json_data['description'],
            'category_id': json_data['category_id'],
            'pick_up': json_data['pick_up'],
            'price': json_data['price'],
            'owner_id': json_data['owner_id']
        }
        response = post_request(['products'], post_data)

        producer = KafkaProducer(bootstrap_servers='kafka:9092')
        producer.send('new-listings-topic', json.dumps(response['response']).encode('utf-8'))
        return JsonResponse(response)

def get_latest_products(request, num=None):
    if num is None:
        num = 3
    response = get_request(['products',])
    product_data = response['response']
    print(type(product_data))
    sorted_products = sorted(product_data, key = lambda x: x["time_posted"], reverse=True)[:int(num)]
    return JsonResponse(json_encode_dict_and_status(sorted_products, True))


def register_user(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        email = json_data.get('email', None)
        school = json_data.get('school_id', None)
        password = json_data.get('password', None)
        post_data = {
            'email': email,
            'school_id' : school,
            'password': password
        }
        if email and password:
            response = post_request(['users'], post_data)
            if response['status']:
                return JsonResponse(json_encode_dict_and_status(response, True))
            else:
                return JsonResponse(response)
        else:
            data = {"message": "Missing email/password"}
            return JsonResponse(data, False)


#Dummy method for testing purposes
def create_school(request):
    school_data = {'name':'UVA','city':'cville','state':'va'}
    response_data = post_request(['schools'], school_data)
    data = json_encode_dict_and_status(response_data, response_data['status'])
    return JsonResponse(data)


def search_products(request, pk=None):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        keyword = json_data.get('keyword', None)
        
        if es.indices.exists(index="listing_index"):
            es.indices.refresh(index="listing_index")
            search_results = es.search(index='listing_index', body={'query': {'query_string': {'query': keyword}}, 'size': 10})
            search_results = search_results["hits"]
        else:
            #search_results = json.dumps({'status': 0})
            try:
                search_results = es.indices.create(index='listing_index')
            except:
                search_results = {'hits':[]}

        return JsonResponse(search_results)
