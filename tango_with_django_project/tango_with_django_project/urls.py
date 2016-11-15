#from registration.backends.simple.views import RegistrationView

"""tango_with_django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls import patterns
from django.conf import settings

#class MyRegistrationView(RegistrationView):
#    def getrighturl(self,request,user):
#        return "/rango/"

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^rango/', include('rango.urls')), # ADD THIS NEW TUPLE!
    url(r'^banjo/', include('banjo.urls')),
#    url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
#    url(r'^accounts/', include('registration.backends.simple.urls')), # refers to registration package
#    url(r'^rango/about', include("rango.urls"))
]
if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'^media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )
