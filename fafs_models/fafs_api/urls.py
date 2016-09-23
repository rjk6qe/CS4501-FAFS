from django.conf.urls import url

from fafs_api import views

urlpatterns = [
	url(r'^users/$', views.UserView.as_view(), name='users'),
	url(r'^users/(?P<pk>[0-9]+)/$', views.UserView.as_view(), name='users'),
	url(r'^addresses/$', views.AddressView.as_view(), name='addresses'),
	url(r'^addresses/(?P<pk>[0-9]+)/$', views.AddressView.as_view(), name='addresses'),
	url(r'^schools/$', views.SchoolView.as_view(), name='schools'),
	url(r'^schools/(?P<pk>[0-9]+)/$', views.SchoolView.as_view(), name='schools'),
	url(r'^categories/$', views.CategoryView.as_view(), name='categories'),
	url(r'^categories/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='categories'),
	url(r'^products/$', views.ProductView.as_view(), name='products'),
	url(r'^products/(?P<pk>[0-9]+)/$', views.ProductView.as_view(), name='products'),
	url(r'^transactions/$', views.TransactionView.as_view(), name='transaction'),
	url(r'^transactions/(?P<pk>[0-9]+)/$', views.TransactionView.as_view(), name='transaction')
]