from django.conf.urls import url

from fafs_api import views

urlpatterns = [
	url(r'^auth/$', views.AuthView.as_view(), name='auth'),
	url(r'^auth/(?P<token>\w+)/$', views.AuthView.as_view(), name='auth'),
	url(r'^auth_check/$', views.auth_check, name='auth_check'),


	url(r'^login/$', views.LoginView.as_view(), name='login'),
	url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
	url(r'^users/$', views.UserView.as_view(), name='users'),
	url(r'^users/(?P<pk>[0-9]+)/$', views.UserView.as_view(), name='users'),
	url(r'^users/check_pass/$', views.users_check_pass, name='users_check_pass'),
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
