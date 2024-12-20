import json
from . models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
        
    print('Cart: ', cart)
    items = []
    order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False,}
        
    for i in cart:
        try:
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']
            
            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageUrl': product.imageUrl,
                },
                'quantity': cart[i]['quantity'],
                'get_total': total,
            }
            print('item: ', item)
            items.append(item)
            
            if product.digital == False:
                order['shipping'] = True
        except:
            print('Didn\'t work for this item')
            pass
    return {'items':items, 'order':order,}

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        cookieData = cookieCart(request)
        items = cookieData['items']
        order = cookieData['order']
    return {'order':order, 'items':items,}

def guestOrder(request, data):
    print('User is not logged in')
        
    print('COOKIES: ', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']
    
    cookie_data = cookieCart(request)
    items = cookie_data['items']
    
    customer, create = Customer.objects.get_or_create(email=email)
    
    customer.name = name
    customer.save()
    
    order = Order.objects.create(
        customer=customer,
        complete=False,
        )
    for item in items:
        product=Product.objects.get(id=item['product']['id'])
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity'],
        )
    return customer, order