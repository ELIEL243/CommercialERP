from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.


def Logout(request):
    logout(request)
    return redirect('login')


def LoginView(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username
                            , password=password)

        if user is not None:
            login(request, user)
            user = User.objects.get(username=username)
            if user.groups.filter(name="Approvisionnement"):
                return redirect('home-appro')
            elif user.groups.filter(name="Production"):
                return redirect('home-prod')
            elif user.groups.filter(name="Commercialisation"):
                return redirect('home-comm')
            elif user.userhasrole.role.name == "Facturation admin" and user.cashier is not None:
                return redirect('home-facturation')
            elif user.userhasrole.role.name == "Facturation" and user.cashier is not None:
                return redirect('home-facturation')
            elif user.groups.filter(name="Administration"):
                return redirect('main-stat')

        else:
            messages.error(request, "echec conn")
            return redirect('login')

    return render(request, 'auth_user/login.html', context={})