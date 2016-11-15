from django.conf.urls import patterns, url
from banjo import views 

urlpatterns = patterns("", url(r'^$', views.nextindex, name = 'nextindex'))
