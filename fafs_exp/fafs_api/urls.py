from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^categories/$', views.getCategories, name='getCategories'),
    url(r'^products/$', views.getProducts, name='getProducts'),
]
