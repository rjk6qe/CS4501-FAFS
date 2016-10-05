from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^products/(?P<pk>[0-9]+)/$', views.product_detail, name='product_detail'),
]
