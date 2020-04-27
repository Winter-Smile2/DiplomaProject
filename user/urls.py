from django.conf.urls import url
from . import views

urlpatterns = [
    #http://127.0.0.1:8000/tple/users
    url(r'^$', views.users),
    #http://127.0.0.1:8000/tple/users/<username>
    url(r'^/(?P<username>\w{1,11})$', views.users),
]