from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import urllib.request
import urllib.parse
import requests
import json
from fafs_api.forms import UserRegister, UserLoginForm

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
    req = requests.post(url, json=data)
    json_response = req.json()
    return json_response

def get_authenticator(request):
    authenticator = request.COOKIES.get('authenticator', None)
    return authenticator

def get_user_if_logged_in(request):
    authenticator = get_authenticator(request)
    post_data = {"authenticator": authenticator}
    user = post_request(['validate_auth'], post_data)
    if user['status']:
        user = user["response"]
    else:
        user = None
    return user

def login_required(f):
    def wrap(request, *args, **kwargs):
        # try authenticating the user
        user = get_user_if_logged_in(request)
        if user:
            request.user = user
            return f(request, *args, **kwargs)
        else:
            current_url = request.path
            return HttpResponseRedirect(reverse('login')+'?next='+current_url)
    return wrap

def index(request):
    user = get_user_if_logged_in(request)

    cat_req = urllib.request.Request(API_URL + 'categories/')
    cat_resp_json = urllib.request.urlopen(cat_req).read().decode('utf-8')
    cat_resp = json.loads(cat_resp_json)
    latest_product_req = urllib.request.Request(API_URL + 'products/latest/3/')
    latest_product_resp_json = urllib.request.urlopen(latest_product_req).read().decode('utf-8')

    latest_product_resp = json.loads(latest_product_resp_json)
    context_dict = {'categories': cat_resp, 'products' : latest_product_resp }
    context_dict['user'] = user
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

@login_required
def product_create(request):
    return render(request, 'fafs_api/product_create.html')

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

def login(request):
    if request.user:
        return HttpResponseRedirect(reverse('index'))
    if request.method == 'POST':
        login_form = UserLoginForm(data=request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']
            #next = request.GET.get('next') or reverse('index')
            next = login_form.cleaned_data.get('next') or reverse('index')
            post_data = {
                "email": email,
                "password": password
            }
            response = post_request(['login'], post_data)
            if not response['status']:
                # Add message to non_field error
                login_form.add_error(None, response['response']['message'])
            else:
                authenticator = response['response']['authenticator']
                request_response = HttpResponseRedirect(next)
                request_response.set_cookie("authenticator", authenticator)
                return request_response
    else:
        next = request.GET.get('next') or reverse('index')
        login_form = UserLoginForm(initial={'next': next})

    context_dict = {}
    context_dict['login_form'] = login_form
    return render(request, 'fafs_api/login.html', context_dict)

@login_required
def logout(request):
    authenticator = get_authenticator(request)
    post_data = {"authenticator": authenticator}
    response = post_request(['logout'], post_data)
    return HttpResponseRedirect(reverse('index'))
