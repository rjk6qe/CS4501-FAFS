from django.conf import settings
from django.contrib.auth.hashers import check_password
from fafs_api.models import User


def authenticate(username=None, password=None):
    try:
        user_obj = User.objects.get(email=username)
        pwd_valid = check_password(password, user_obj.password)
        if pwd_valid:
            return user_obj
    except User.DoesNotExist:
        pass
    return None