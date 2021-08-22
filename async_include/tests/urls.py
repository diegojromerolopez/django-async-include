# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf.urls import include
from django.urls import path

urlpatterns = [
    path(
        r'async_include/',
        include('async_include.urls', namespace="async_include")
    ),
]
