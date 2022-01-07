from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.views.generic.base import View

from store.models import Store, Category, Product


class IndexView(View):
    def get(self, request):
        host = request.get_host()
        slug = host.split('.')[0]
        store = get_object_or_404(Store, slug=slug)
        categories = store.category_set.all()
        context = {
            'categories': categories,
            'store': store
        }
        return render(request, 'store/index.html', context)


class IndexSlugView(View):
    def get(self, request, slug):
        store = get_object_or_404(Store, slug=slug)
        categories = store.category_set.all()
        for cat in categories:
            print(cat.name)
            for prod in cat.products.all():
                print(prod.name)

        context = {
            'categories': categories,
            'store': store
        }
        return render(request, 'store/index.html', context)


class CategoryDetailView(View):
    def get(self, request, slugcat):
        host = request.get_host()
        slug = host.split('.')[0]
        store = get_object_or_404(Store, slug=slug)
        categories = store.category_set.all()
        category = Category.objects.filter(store=store, slug=slugcat).first()
        products = Product.objects.filter(category=category)
        context = {
            'category': category,
            'categories': categories,
            'store': store,
            'products': products,
        }
        return render(request, 'store/category.html', context)


class CategorySlugDetailView(View):
    def get(self, request, slug, slugcat):
        store = get_object_or_404(Store, slug=slug)
        categories = store.category_set.all()
        category = Category.objects.filter(store=store, slug=slugcat).first()
        products = Product.objects.filter(category=category)
        context = {
            'category': category,
            'categories': categories,
            'store': store,
            'products': products,
        }
        return render(request, 'store/category.html', context)


class CartSlugDetailView(View):
    def get(self, request, slug):
        store = get_object_or_404(Store, slug=slug)
        categories = store.category_set.all()
        products = Product.objects.filter(store=store).all()
        context = {
            'categories': categories,
            'store': store,
            'products': products
        }
        return render(request, 'store/cart.html', context)


class CheckoutSlugDetailView(View):
    def get(self, request, slug):
        store = get_object_or_404(Store, slug=slug)
        categories = store.category_set.all()
        products = Product.objects.filter(store=store).all()
        context = {
            'categories': categories,
            'store': store,
            'products': products
        }
        return render(request, 'store/checkout.html', context)


class SearchView(View):
    def get(self, request):
        host = request.get_host()
        slug = host.split('.')[0]
        query = request.GET['query']
        store = get_object_or_404(Store, slug=slug)
        categories = store.category_set.all()
        products = Product.objects.filter(store=store, name__contains=query)
        context = {
            'categories': categories,
            'store': store,
            'products': products,
            'query': query
        }
        return render(request, 'store/search.html', context)


class ProductView(View):
    def get(self, request, pk):
        host = request.get_host()
        slug = host.split('.')[0]
        store = get_object_or_404(Store, slug=slug)
        product = get_object_or_404(Product, pk=pk)
        categories = store.category_set.all()
        context = {
            'categories': categories,
            'store': store,
            'product': product
        }
        return render(request, 'store/product.html', context)


class ProductSlugView(View):
    def get(self, request, slug, pk):
        store = get_object_or_404(Store, slug=slug)
        product = get_object_or_404(Product, pk=pk)
        categories = store.category_set.all()
        products = Product.objects.filter(category=product.category).all()
        context = {
            'categories': categories,
            'store': store,
            'product': product,
            'products': products,
        }
        return render(request, 'store/product.html', context)
