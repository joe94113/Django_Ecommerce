var updateBtns = document.getElementsByClassName('update-cart') //取得class="update-cart"的元素

for(var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener("click", function(){
        var productId = this.dataset.product  // 讀取到data-product="{{ product.id }}"資料
        var action = this.dataset.action  // 讀取到data-action="add"資料
        console.log("productId:", productId, "action", action)

        console.log('USER:', user)
        if(user === 'AnonymousUser'){
            console.log('Not logged in')
        }else{
            updateUserOrder(productId, action)
        }
    })
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
    })
}