from django.conf.urls import include
from django.urls import path
from django.shortcuts import render


def test_page_view(request):
    return render(request, 'test_e2e_page.html')


urlpatterns = [
    path('test-page/', test_page_view, name='test_page'),
    path(r'async_include/', include('async_include.urls', namespace="async_include")),
]
