from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^$', views.navTotal, name = 'navTotal'),
	url(r'^navTotalAjax/$', views.navTotalAjax, name = 'navTotalAjax'),
	url(r'^navTotalInitVariables/$', views.navTotalInitVariables, name = 'navTotalInitVariables'),
	url(r'^navTotalEquityOffering/$', views.navTotalEquityOffering, name = 'navTotalEquityOffering'),
	url(r'^navTotalAssetAcquisition/$', views.navTotalAssetAcquisition, name = 'navTotalAssetAcquisition'),
	url(r'^navTotalAssetSale/$', views.navTotalAssetSale, name = 'navTotalAssetSale'),
]