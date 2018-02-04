# -*- coding: utf-8 -*-

from django.conf.urls import url

from async_include import views

app_name = 'async_include'

urlpatterns = [
    # Load
    url(r'^get/?$', views.get_template, name="get_template"),
]