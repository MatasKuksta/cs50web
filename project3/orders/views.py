from django.http import HttpResponse
from django.shortcuts import render
<<<<<<< HEAD
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from django.shortcuts import render, redirect
=======
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
>>>>>>> 5a3216f58f548afd0ea982d051736473fc63f63b

# Create your views here.
def index(request):
    return render(request, "index.html")

<<<<<<< HEAD
def signup(request):
    if request.method == "POST":
        username == request.post("username")
        email == request.post("email")
        firstname == request.post("firstname")
        lastname == request.post("lastname")
        password == request.post("password")
=======
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {"message": "Username already exists"})
        else:
            user = User.objects.create_user(username, email, password)
            user.first_name = firstname
            user.last_name = lastname
            user.save()
            return render(request, "orders/login.html")
>>>>>>> 5a3216f58f548afd0ea982d051736473fc63f63b
