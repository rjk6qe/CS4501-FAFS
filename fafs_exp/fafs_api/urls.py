from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^categories/$', views.getCategories, name='getCategories'),
    url(r'^products/$', views.getProducts, name='getProducts'),
    url(r'^products/latest/(?P<num>[0-9]*)/$', views.getLatestProducts, name='getLatestProducts'),
    url(r'^products/latest/$', views.getLatestProducts, name='getLatestProducts_default'),
]
