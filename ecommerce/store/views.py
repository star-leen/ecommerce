from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import *
from .utils import cookieCart, cartData, guestOrder
from django.urls import reverse
# from paypal.standard.forms import PayPalPaymentsForm

# Create your views here.
def store(request):
    data = cartData(request)
    order = data['order']
    
    products = Product.objects.all()
    context = {'products': products, 'order':order}
    return render(request, 'store/store.html', context)

def cart(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    
    context = {'items':items, 'order':order,}
    return render(request, 'store/cart.html', context)

def checkout(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    
    context = {'items':items, 'order':order,}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = request.body
    data = data.decode('utf-8')
    data = json.loads(data)
    productId = data['productId']
    action = data['action']
    print('Action: ', action)
    print('ProductId: ', productId)
    
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = request.body
    data = data.decode('utf-8')
    data = json.loads(data)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        
    else:
        customer, order = guestOrder(request, data)
    
    total =float(data['form']['total'])
    order.transaction_id = transaction_id
        
    if total == order.get_cart_total:
        order.complete = True
    order.save()
    
    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],
        )
        
    return JsonResponse('Payment Complete', safe=False)