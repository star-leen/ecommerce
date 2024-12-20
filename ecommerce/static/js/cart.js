var updateBtns = document.getElementsByClassName('update-cart')

for(var i = 0; i < updateBtns.length; i ++) {
    updateBtns[i].addEventListener('click', function() {
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId: ', productId, ' action: ', action)

        console.log('User: ', user)
        if (user === 'AnonymousUser') {
            addCookieItem(productId, action)
        } else {
            updateUserOrder(productId, action)
        }
    })
}

function addCookieItem(productId, action) {
    console.log('Not logged in')
    if(action=='add') {
        if (cart[productId] == undefined) {
            cart[productId] = {'quantity': 1}
        } else {
            cart[productId]['quantity'] += 1
        }
    } 
    if(action == 'remove') {
        if (cart[productId] == undefined) {
            console.log('Cannot remove from nothing...')
        } else {
            cart[productId]['quantity'] -= 1
            if(cart[productId]['quantity'] < 0) {
                delete cart[productId]
                console.log('Item deleted')
            }
        }
    }
    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/'
    location.reload()
    console.log('Cart: ', cart)
}

console.log(cart)

function updateUserOrder(productId, action) {
    console.log('User is logged in, sending data...')

    var url = '/update_item/'

    const myHeaders = new Headers();
    myHeaders.append('Content-Type', 'application/json');
    myHeaders.append('X-CSRFToken', csrftoken);

    fetch(url, {
        method: 'POST',
        headers:myHeaders,
        body: JSON.stringify({'productId':productId, 'action':action}),
    })

    .then((response) => {
        return response.json()
    })

    .then((data) => {
        console.log('data :', data)
        location.reload()
    })
}