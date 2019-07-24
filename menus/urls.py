from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import LoginView
from menus.views import (ItemCreateView,ItemListView,ItemDetailUpdateView)


urlpatterns = [


    url(r'^(?P<pk>\d+)/$', ItemDetailUpdateView.as_view(),name='detail-update'),

    url(r'$', ItemListView.as_view(),name='list'),
    url(r'^create/$',ItemCreateView.as_view(),name='create'),
]
