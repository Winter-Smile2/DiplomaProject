#-*-coding:utf-8-*-
from django.conf.urls import url
from . import views

urlpatterns = [
    #http://127.0.0.1:8000/tple/index/title
    url(r'^/title$', views.get_title),
    # http://127.0.0.1:8000/tple/index/image
    url(r'^/image$',views.get_image),
    # http://127.0.0.1:8000/tple/index/href
    url(r'/href$',views.get_href),
    # http://127.0.0.1:8000/tple/index/eititle
    url(r'^/eititle$',views.get_eititle),
    # http://127.0.0.1:8000/tple/index/eiimage
    url(r'^/eiimage$',views.get_eiimage),
    # http://127.0.0.1:8000/tple/index/eihref
    url(r'^/eihref$',views.get_eihref),
    # http://127.0.0.1:8000/tple/index/eihref
    url(r'^/eitimer$',views.get_eitimer),
    # http://127.0.0.1:8000/tple/index/eiviews
    url(r'^/eiviews$',views.get_eivisits),
    # http://127.0.0.1:8000/tple/index/eitally
    url(r'^/eitally$',views.get_eitally),
    # http://127.0.0.1:8000/tple/index/lastimages
    url(r'^/lastimages$',views.get_last_image),
    # http://127.0.0.1:8000/tple/index/lasttitles
    url(r'^/lasttitles$',views.get_last_title),
    # http://127.0.0.1:8000/tple/index/lasthrefs
    url(r'^/lasthrefs$',views.get_last_href),

]