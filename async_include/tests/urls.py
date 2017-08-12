# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve as serve_static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    url(r'^async_include/', include('async_include.urls', namespace="async_include")),
]
