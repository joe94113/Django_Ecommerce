from django.shortcuts import render
from .models import *  # 載入所有models


# Create your views here.
def store(request):
    products = Product.objects.all()  # 搜尋到所有產品資料
    context = {'products': products}
    return render(request, 'store/store.html', context)


def cart(request):
    if request.user.is_authenticated:  # 如果使用者通過身分驗證
        customer = request.user.customer  # 取得使用者name
        # https://docs.djangoproject.com/en/3.1/ref/models/querysets/#get-or-create
        order, created = Order.objects.get_or_create(customer=customer, complete=False)  # 搜尋如果不存在則建立
        items = order.orderitem_set.all()  # 取得OrderItem物件
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    context = {'items': items, 'order': order}
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:  # 如果使用者通過身分驗證
        customer = request.user.customer  # 取得使用者name
        # https://docs.djangoproject.com/en/3.1/ref/models/querysets/#get-or-create
        order, created = Order.objects.get_or_create(customer=customer, complete=False)  # 搜尋如果不存在則建立
        items = order.orderitem_set.all()  # 取得OrderItem物件
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    context = {'items': items, 'order': order}
    return render(request, 'store/checkout.html', context)
