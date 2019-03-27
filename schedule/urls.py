from django.conf.urls import url, include
from django.urls import path

from . import views

from .models import *

urlpatterns = [
    url(r'^today/$', views.today, name='today'),
    path('day/<int:year>/<int:month>/<int:day>/', views.day, name='day')
]
