from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index_store'),
    path('categoria/<slug:slugcat>', CategoryDetailView.as_view(), name='category_detail'),
    path('buscar', SearchView.as_view(), name='search'),
    path('producto/<int:pk>', ProductView.as_view(), name='product'),

    path('tienda/<slug:slug>', IndexSlugView.as_view(), name='index_slug_store'),
    path('tienda/<slug:slug>/categoria/<slug:slugcat>', CategorySlugDetailView.as_view(), name='category_slug_detail'),
    path('tienda/<slug:slug>/producto/<int:pk>', ProductSlugView.as_view(), name='product_slug'),
    path('tienda/<slug:slug>/carrito', CartSlugDetailView.as_view(), name='cart_slug'),
    path('tienda/<slug:slug>/pagar', CheckoutSlugDetailView.as_view(), name='checkout_slug'),

]
