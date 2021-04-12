import json

from . models import *


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])  # 取得cookies
    except KeyError:  # 使用者剛登入cookies裡面沒有cart會報錯
        cart = {}

    print('Cart:', cart)
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cartItems = order['get_cart_items']

    for i in cart:
        try:
            cartItems += cart[i]["quantity"]

            product = Product.objects.get(id=i)  # 找到商品
            total = (product.price * cart[i]["quantity"])  # 商品乘以數量

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]["quantity"]

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL,
                },
                'quantity': cart[i]["quantity"],
                'get_total': total
            }

            items.append(item)

            if not product.digital:  # product.digital == False
                order['shipping'] = True
        except:
            pass
    return {'items': items, 'order': order, 'cartItems': cartItems}


def cartData(request):
    if request.user.is_authenticated:  # 如果使用者通過身分驗證
        customer = request.user.customer  # 取得使用者name
        # https://docs.djangoproject.com/en/3.1/ref/models/querysets/#get-or-create
        order, created = Order.objects.get_or_create(customer=customer, complete=False)  # 搜尋如果不存在則建立
        items = order.orderitem_set.all()  # 取得OrderItem物件
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        items = cookieData['items']
        order = cookieData['order']
    return {'items': items, 'order': order, 'cartItems': cartItems}