from django.urls import path
from .views import *

urlpatterns = [
    path('main-stat/', MainStatView, name='main-stat')
]