from django.shortcuts import render,redirect,get_object_or_404
from core.models import *
from django.contrib.auth import get_user_model
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
from  django.contrib.auth.decorators import login_required,user_passes_test
# Create your views here.

User =get_user_model()

@login_required(login_url = 'showroom_admin:login')
@user_passes_test(lambda user: user.is_staff)
def dashboard(request):

    total_users = User.objects.count()
    total_order = Order.objects.filter(ordered=True).count()
    total_pending  = Order.objects.filter(status=False,ordered=True).count()
    total_delivered  = Order.objects.filter(status=True,ordered=True).count()
    total_item =Item.objects.count()


    pending  = Order.objects.filter(status=False,ordered=True).order_by('-id')
    delivered  = Order.objects.filter(status=True,ordered=True).order_by('-id')

    context = {

                "total_users":total_users,
                "total_order":total_order,
                "total_pending":total_pending,
                "total_delivered":total_delivered,
                "total_item":total_item,
                "pending":pending,
                "delivered":delivered,

                }

    return render(request,"home.html",context)

@login_required(login_url = 'showroom_admin:login')
@user_passes_test(lambda user: user.is_staff)
def orderdetail(request,pk):

    order = get_object_or_404(Order,pk=pk)
    

    context={"order":order}

    return render(request,'order_detail.html',context)

@login_required(login_url = 'showroom_admin:login')
@user_passes_test(lambda user: user.is_staff)
def send(request,pk):
    order = get_object_or_404(Order,pk=pk)
    order.status = True
    order.save()

    return redirect('showroom_admin:orderdetail',pk=pk)

@login_required(login_url = 'showroom_admin:login')
@user_passes_test(lambda user: user.is_staff)
def productList(request):
    items = Item.objects.all()

    context={'items':items}

    return render(request,'product_list.html',context)

@login_required(login_url = 'showroom_admin:login')
@user_passes_test(lambda user: user.is_staff)
def productItem(request,pk):

    item = get_object_or_404(Item,pk=pk)

    context={"item":item}

    return render(request,'product_item.html',context)

@login_required(login_url = 'showroom_admin:login')
@user_passes_test(lambda user: user.is_staff)
def add_product(request):

    form = ItemForm
    if request.method == 'POST':
        form = ItemForm(data=request.POST,files=request.FILES)
        if form.is_valid():
            instance  = form.save()

            files = request.FILES.getlist('images')

            for f in files:
                image = Image(item=instance,image=f)
                image.save()
            # messages.success(request,'Item Successfully added')
            return redirect('showroom_admin:product_item', pk=instance.id)
    else:
        form = ItemForm()

    context = {'form':form}

    return render(request,'add_product.html', context)

@login_required(login_url = 'showroom_admin:login')
@user_passes_test(lambda user: user.is_staff)
def edith_product(request,pk):

    item = Item.objects.get(pk=pk)


    form = ItemForm2(instance=item)
    if request.method == 'POST':
        form = ItemForm2(data=request.POST,files=request.FILES or None,instance=item)
        if form.is_valid():
            instance=form.save()

            if request.FILES.getlist('images'):
                files = request.FILES.getlist('images')

                for f in files:
                    image = Image(item=instance,image=f)
                    image.save()
            # messages.success(request,'Item Successfully added')
            return redirect('showroom_admin:product_item',pk=pk)
    else:
        form = ItemForm2(instance=item)

    context = {'form':form}

    return render(request,'add_product.html', context)

@login_required(login_url = 'showroom_admin:login')
@user_passes_test(lambda user: user.is_staff)
def delete_product(request,pk):

    item = get_object_or_404(Item,pk=pk)

    item.delete()
    # messages.success(request,'Item Successfully added')
    return redirect('showroom_admin:productlist')

@login_required(login_url = 'showroom_admin:login')
def category_list(request):

    category=Category.objects.all()

    context={"category":category}

    return render(request,'category_list.html',context)


@login_required(login_url = 'showroom_admin:login')
@user_passes_test(lambda user: user.is_staff)
def add_category(request):

    form = CategoryForm
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            # messages.success(request,'Item Successfully added')
            return redirect('showroom_admin:category_list')
    else:
        form = CategoryForm()

    context = {'form':form}

    return render(request,'add_product.html', context)


@login_required(login_url = 'showroom_admin:login')
@user_passes_test(lambda user: user.is_staff)
def delete_category(request,pk):

    category = get_object_or_404(Category,pk=pk)

    category.delete()
    messages.success(request,'Category Successfully Removed')
    return redirect('showroom_admin:category_list')


@login_required(login_url = 'showroom_admin:login')
@user_passes_test(lambda user: user.is_staff)
def pending_list(request):
    pending  = Order.objects.filter(status=False,ordered=True).order_by('-id')

    context = {
                "pending":pending,
                }
    return render(request,"pending_list.html",context)

@login_required(login_url = 'showroom_admin:login')
@user_passes_test(lambda user: user.is_staff)
def delivered_list(request):
    delivered  = Order.objects.filter(status=True,ordered=True).order_by('-id')

    context = {
                "delivered":delivered,
                }

    return render(request,"delivered_list.html",context)



def my_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)


        if user is not None:
            login(request, user)
            return redirect('showroom_admin:dashboard')
        else:

            messages.error(request,'username or password not correct')
            return redirect('showroom_admin:login')
    else:

        return render(request, 'login.html')
