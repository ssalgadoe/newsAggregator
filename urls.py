from django.conf.urls import url
from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns



urlpatterns = [
    path('', views.index, name='index'),
    url(r'details/(?P<news_id>.+)/$', views.news_data, name='news_data'),
    ]