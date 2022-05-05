from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
import uuid 

import random
from faker import Faker


# Create your views here.
# Helps to generate fake items on the database
def faker_data(request):
    fake = Faker()
    category = Category.objects.all()
    

    for i in range(3000):
        num = random.randint(1, 14)
        cat = random.randint(0, 2)
        price = random.randint(500, 10000)
        
        item = Item(title=fake.name(), image=f'background_pic/{num}.jpg',price=price,category=category[cat],quantity=100,description=fake.text())
        item.save()

    return redirect('core:home')

# Home page view
def home(request):
    items = Item.objects.all()
    if request.method == 'POST':
        print(request.POST.get('cat'),'hello')
        
        # Gets items base on search text and category.
        if request.POST.get('cat') == "":
            items = Item.objects.filter(title__contains=request.POST.get('search'))
            
        else:
            cat = get_object_or_404(Category, pk=int(request.POST.get('cat')))
            items = Item.objects.filter(title__contains=request.POST.get('search'),category=cat)
            
        


    items_count = items.count()


    # Pagination of items (Max of 100 per page)
    page = request.GET.get('page', 1)

    paginator = Paginator(items, 100)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    category = Category.objects.all()

    context = {"category": category,
            "items": items, "items_count": items_count,'store':'active'}

    return render(request, 'core/home.html', context)


# Retrieves details of a product or Item
def product_details(request, pk):
    item = get_object_or_404(Item, pk=pk)
    context = {}

    # check if user is authenticated and gets a list of thier current order items
    if request.user.is_authenticated:

        try:
            order = Order.objects.get(user=request.user, ordered=False)
            order_items = order.items.values_list('item__id', flat=True)
            

            context = {'item':item,'order_items':order_items}
        except ObjectDoesNotExist:

            context = {'item': item}

    else:
        context = {'item': item}

    return render(request, 'core/detail_page.html', context)


# Function handle the adding to cart(Existing or new order)
@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)

    order_item, created = OrderItem.objects.get_or_create(item=item, user = request.user,ordered=False)

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        #check if the order item is in the order so i just increases the quatity
        if order.items.filter(item__pk=item.pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, f'This item quantity was updated  to  cart. click cart to view')
            return redirect('core:product_details' ,pk=pk)
        else:
            messages.info(request, f'This item was added to cart. click cart to view')
            order.items.add(order_item)
            return redirect('core:product_details' ,pk=pk)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date )
        order.items.add(order_item)
        messages.info(request, f'This item was added to cart.')
    return redirect('core:product_details' ,pk=pk)

# Function handle change in quantity of an item in the cart(Existing order)
@login_required
def remove_single_item_from_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
                order_item.delete()

            messages.info(request, f'This item quantity was updated')
            return redirect('core:store')
        else:
            # add a add a message saying order does not contain the order time
            messages.info(request, f'This item was not in your cart.')
            return redirect('core:store')

    else:
        # add a add a message saying the user dosen't have an order
        messages.info(request, f'You do not have an active order.')
        return redirect('core:home')


# Function handles removing of an item in the cart (Existing order)
@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
       # check if the order item is in the order
        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False
                                    )[0]
            order.items.remove(order_item)
            order_item.delete()

            # messages.info(request, f'This item was removed from  cart.')
            return redirect('core:product_details', pk=pk)
        else:
            # add a add a message saying order does not contain the order time
            messages.info(request, f'This item was not in your cart.')
            return redirect('core:product_details', pk=pk)

    else:
        # add a add a message saying the user dosen't have an order
        messages.info(request, f'You do not have an active order.')
        return redirect('core:home')

# Handles cart checkout
@login_required
def checkout(request):
    try:
        order = Order.objects.get(user=request.user, ordered=False)
        order_items = order.items


        context = {"order_items": order_items,
                "order": order}
    except ObjectDoesNotExist:

        context = {}

    return render(request, 'core/checkout.html', context)

#Handle completing the order and clearing cart.
@login_required
def payment(request,pk):

    order = get_object_or_404(Order, pk=pk)

    order_items = order.items.all()
    
    if order_items.count() <= 0:
        
        return redirect('core:checkout')
    
    # Updates order item to ordered so it know the items that has been paid for
    order_items.update(ordered=True)
    for item in order_items:
        item.save()

    order.ordered = True

    order.ref_code = uuid.uuid4().hex[:6].upper()
    order.complete_date = timezone.now()
    order.save()

    all_orders = order.items.all()

    #Reduce item quantity 
    for order_item in all_orders:
        item = order_item.item
        item.quantity = item.quantity - order_item.quantity
        item.save()


    messages.info(request, f'Order completed')

        

    return redirect('core:home')
    
    

