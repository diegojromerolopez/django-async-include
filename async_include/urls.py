# -*- coding: utf-8 -*-

from django.urls import path

from async_include import views

app_name = 'async_include'

urlpatterns = [
    path(r'get/?', views.get_template, name="get_template"),
]
