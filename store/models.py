from django.db import models
from django.contrib.auth.models import User  # 內置Django用戶模型，為註冊的每個客戶創建實例


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True,  # blank是針對表單，null是針對資料庫
                                on_delete=models.CASCADE)  # 對應到別人的資料要怎麼被處理，而 CASCADE 就是一倂刪除
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):  # 產品模型代表我們在商店中擁有的產品類型
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=False)  # 判斷是物理還是數位商品
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property  # 讀取的屬性
    def imageURL(self):  # 捕捉如果沒有照片產生的錯誤
        try:
            url = self.image.url
        except:
            url = ""
        return url


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True,
                                 null=True)  # on_delete=models.SET_NULL用於表示該字段的所有者，如果不存在所有者，則應將其設置為NULL。
    date_orderd = models.DateTimeField(auto_now_add=True)  # 每次 object 被儲存時會自動更新為現在的時間
    complete = models.BooleanField(default=False, null=True, blank=False)  # 完成訂單狀態
    transaction_id = models.CharField(max_length=200, null=True)  # 交易ID

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if not i.product.digital:  # 如果產品不是實體
                shipping = True
        return shipping


    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        count = sum([item.quantity for item in orderitems])  # 查看每個OrderItem.quantity相加
        return count


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)  # 數量
    data_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):  # 取得個別總價
        total = self.product.price * self.quantity  # 產品價格*數量
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zip_code = models.CharField(max_length=200, null=True)  # 郵政編碼
    data_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
