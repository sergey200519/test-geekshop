from django.shortcuts import render
from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from django.contrib import auth, messages
# from django.contrib import auth, messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from basket.models import Basket
from django.contrib.auth.decorators import login_required
# from django.contrib.messages import middleware

# Create your views here.

def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = auth.authenticate(username=username, password=password)
            if user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()

    context = {
        "title": "Geekshop |  Авиоризация",
        "form": form
    }
    return render(request, "authapp/login.html", context)





def register(request):
    if request.method == "POST":
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Вы успешно зарегистрировалилсь")
            return HttpResponseRedirect(reverse('authapp:login'))
        else:
            print(form.errors)
    else:
        form = UserRegisterForm()
    context = {
        "title": "Geekshop |  Регистрация",
        "form": form
    }
    return render(request, "authapp/register.html", context)




@login_required
def profile(request):
    if request.method == "POST":
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
    user_select = request.user
    context = {
        "title": "Geekshop |  Профайл",
        "form": UserProfileForm(instance=request.user),
        "baskets": Basket.objects.filter(user=user_select)
    }
    return render(request, "authapp/profile.html", context)




def logout(request):
    auth.logout(request)
    return render(request, "mainapp/index.html")
