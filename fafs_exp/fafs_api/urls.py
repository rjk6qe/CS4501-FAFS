from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^auth_check/$', views.auth_check, name="auth_check"),

    url(r'^categories/$', views.get_categories, name='getCategories'),
    url(r'^categories/(?P<pk>[0-9]+)/$', views.get_categories, name='getCategories'),
    url(r'^products/create/$', views.create_product, name='createProduct'),
    url(r'^products/$', views.get_products, name='getProducts'),
    url(r'^products/(?P<pk>[0-9]+)/$', views.get_products, name='getProduct'),
    url(r'^products/latest/$', views.get_latest_products, name='getLatestProducts_default'),
    url(r'^products/latest/(?P<num>[0-9]*)/$', views.get_latest_products, name='getLatestProducts'),
    url(r'^register/$', views.register_user, name='registerUser'),
    url(r'^search_products/$', views.search_products, name='searchProducts'),

    #Dummy method just for testing
    url(r'^school/$', views.create_school),
]
