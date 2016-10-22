import requests

API_URL = 'http://exp-api:8000/fafs/'

def append_to_url(path_list):
    url = API_URL
    if path_list is not None:
        for path in path_list:
            if path is not None:
                url = url + str(path) + '/'
    return url

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

class UserMiddleware(object):
    def process_request(self, request):
        request.user = get_user_if_logged_in(request)
