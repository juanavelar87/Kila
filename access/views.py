from django.db import IntegrityError
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect, render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

def loginv(request):
    if request.method=="POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("home:index"))
        else:
            return render(request, "access/login.html", {
                "message": "Nombre de usuario o contraseña incorrecta"
            })
    else:
        return render(request, "access/login.html")

def logoutv(request):
    logout(request)
    return HttpResponseRedirect(reverse("access:login"))
