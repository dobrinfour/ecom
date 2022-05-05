# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from django.contrib.auth import authenticate, login
from .models import *

# Create your views here.

def register(request):
   if request.method == 'POST':
      form = UserRegisterForm(request.POST)

      if form.is_valid():
          form.save()
          username = form.cleaned_data.get('username')
          password = form.cleaned_data.get('password1')

          user = authenticate(request, username=username, password=password)

          login(request, user)
          messages.success(request, f'Account creation for {username} was successfully!')

          return redirect('core:home')
      else:
          messages.error(request, f'Invalid, please complete form details.')

   else:
      form = UserRegisterForm()

   return render(request, 'core/register.html', {"form": form})


# Create your views here.
def my_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        print(user)
        if user is not None:
            login(request, user)

            messages.success(request, f'you have logged in')
            return redirect('core:home')

        else:
            messages.error(request,'username or password not correct')
            return redirect('login')
    else:

        return render(request, 'core/login.html')
