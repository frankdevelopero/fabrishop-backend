from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('inicio', IndexView.as_view(), name='index'),

]
