from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^$', views.navTotal, name = 'navTotal'),
	# url(r'^navTotalAjax/$', views.navTotalAjax, name = 'navTotalAjax'),
	# url(r'^ini_prod/change/$', views.changeInitProduct, name = 'changeInitProduct'),
]