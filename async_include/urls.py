try:
    from django.urls import re_path
except ImportError:
    from django.conf.urls import url as re_path

from async_include import views

app_name = 'async_include'

urlpatterns = [
    re_path(r'^get/?$', views.get_template, name="get_template"),
]
