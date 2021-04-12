import json
import datetime

from django.shortcuts import render
from django.http import JsonResponse

from .models import *  # 載入所有models
from .utils import cookieCart, cartData, guestOrder


# Create your views here.
def store(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()  # 搜尋到所有產品資料
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    items = data['items']
    order = data['order']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    items = data['items']
    order = data['order']

    context = {'items': items, 'order': order, 'cartItems': cartItems, 'shipping': False}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']  # 產品ID
    action = data['action']  # add or remove

    # print('Action:', action, 'ProductId:', productId)

    customer = request.user.customer  # 取得用戶物件
    product = Product.objects.get(id=productId)  # 取得此ID產品物件
    order, created = Order.objects.get_or_create(customer=customer,
                                                 complete=False)  # 搜尋如果不存在則建立，return(返回搜尋物件, 是否建立bool值)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    # print('orderItem:', orderItem, 'created:', created)

    if action == 'add':  # 連結到前端，當使用者按下加入購物車
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)  # safe=False不偵錯


def processOrder(request):
    # print('Date:', request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,
                                                     complete=False)

    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):  # 前後端金額相同，防止從前端更改
        order.complete = True  # 訂單狀態改成完成
    order.save()

    if order.shipping:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zip_code=data['shipping']['zipcode'],
        )

    return JsonResponse("Payment submitted..", safe=False)
