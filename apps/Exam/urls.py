
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index),
	url(r'^register$', views.register),
	url(r'^login$', views.login),
	url(r'^travels$', views.travels),
	url(r'^logout$', views.logout),
	url(r'^travels/add$', views.add),
	url(r'^insert$', views.insert),
	url(r'^travels/destination/(?P<number>\S+)$', views.tripdetail),
	url(r'^join/(?P<number>\S+)$', views.join),

]
