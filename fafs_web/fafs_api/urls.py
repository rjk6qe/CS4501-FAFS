from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^products/(?P<pk>[0-9]+)/$', views.product_detail, name='product_detail'),
    url(r'^products/create/$', views.product_create, name='product_create'),
    url(r'^categories/(?P<pk>[0-9]+)/$', views.category_detail, name='category_detail'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
]
