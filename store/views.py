from django.shortcuts import render
from .models import *  # 載入所有models


# Create your views here.
def store(request):
    products = Product.objects.all()  # 搜尋到所有產品資料
    context = {'products': products}
    return render(request, 'store/store.html', context)


def cart(request):
    context = {}
    return render(request, 'store/cart.html', context)


def checkout(request):
    context = {}
    return render(request, 'store/checkout.html', context)
