from django.urls import path

from .views import *

app_name = "articles"

urlpatterns = [
    path('store-test/', StoreView.as_view()),
    path('store-test/<int:pk>', StoreDetailView.as_view()),
    path('store/<int:pk>', StoreHomeView.as_view()),
    path('home/<int:pk>', HomeView.as_view()),
    path('store-data/<int:pk>', StoreDataView.as_view()),
    path('register', RegisterAPIView.as_view()),
    path('login', UserLoginAPIView.as_view(), name='login_api'),
    path('product', ProductAPIView.as_view()),
    path('product/add', ProductAddView.as_view()),
    path('category/add', CategoryAddView.as_view()),
    path('category', CategoryAPIView.as_view()),
    path('verifyslug/<str:slug>', VerifySlugAPIView.as_view()),
]
