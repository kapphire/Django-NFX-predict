from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^$', views.typeCurve, name = 'typeCurve'),
	url(r'^typeCurveAjax/$', views.typeCurveAjax, name = 'typeCurveAjax'),
	url(r'^ini_prod/change/$', views.changeInitProduct, name = 'changeInitProduct'),
]