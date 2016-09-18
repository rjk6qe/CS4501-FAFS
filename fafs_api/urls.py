from django.conf.urls import url

from fafs_api import views

urlpatterns = [
	url(r'^users/$', views.UserView.as_view(), name='users'),
	url(r'^users/(?P<pk>[0-9]+)/$', views.UserView.as_view(), name='users'),
	url(r'^schools/$', views.SchoolView.as_view(), name='schools'),
	url(r'^schools/(?P<pk>[0-9]+)/$', views.SchoolView.as_view(), name='schools'),
]