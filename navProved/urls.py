from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^$', views.navProved, name = 'navProved'),
	url(r'^navProvedAjax/$', views.navProvedAjax, name = 'navProvedAjax'),	
]