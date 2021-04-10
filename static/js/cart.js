var updateBtns = document.getElementsByClassName('update-cart') //取得class="update-cart"的元素

for(var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener("click", function(){
        var productId = this.dataset.product  // 讀取到data-product="{{ product.id }}"資料
        var action = this.dataset.action  // 讀取到data-action="add" or "remove"資料
        console.log("productId:", productId, "action", action)

        console.log('USER:', user)
        if(user === 'AnonymousUser'){
            addCookieItem(productId, action)
        }else{
            updateUserOrder(productId, action)
        }
    })
}


function addCookieItem(productId, action){
    console.log("USER is not authenticated")

    if(action == 'add'){
        if(cart[productId] == undefined){  // main.html裡的var cart
            cart[productId] = {'quantity': 1}
        }else{
            cart[productId]['quantity'] + 1
        }

    if(action == 'remove'){
        cart[productId]['quantity'] -= 1
        
        if(cart[productId]['quantity'] <= 0){
                console.log("Remove Item")
                delete cart[productId]
            }
        }
    }
    console.log("Cart:", cart)
    document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}


function updateUserOrder(productId, action){  // 更新用戶訂單
    console.log('User is logged in, sending data...')

    var url = '/update_item/'

    fetch(url, {  // 使用 fetch() (en-US) 來 POST JSON 格式的資料。
        method: 'POST', // or 'PUT'
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'productId': productId, 'action': action})
    })

    .then((response) => {
        return response.json
    })

    .then((data) => {
        console.log('data:', data)
        location.reload()  // 畫面重新載入

    })
}