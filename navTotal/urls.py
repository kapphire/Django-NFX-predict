from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^$', views.navTotal, name = 'navTotal'),
	url(r'^navTotalInitVariables/$', views.navTotalInitVariables, name = 'navTotalInitVariables'),
	url(r'^navTotalEquityOffering/$', views.navTotalEquityOffering, name = 'navTotalEquityOffering'),
	url(r'^navTotalAssetAcquisition/$', views.navTotalAssetAcquisition, name = 'navTotalAssetAcquisition'),
	url(r'^navTotalAssetSale/$', views.navTotalAssetSale, name = 'navTotalAssetSale'),
	url(r'^navTotalNetLanding/$', views.navTotalNetLanding, name = 'navTotalNetLanding'),
	url(r'^navTotalLandingResults/$', views.navTotalLandingResults, name = 'navTotalLandingResults'),
	url(r'^navTotalUnconventional/$', views.navTotalUnconventional, name = 'navTotalUnconventional'),
	url(r'^navTotalConventional/$', views.navTotalConventional, name = 'navTotalConventional'),
]