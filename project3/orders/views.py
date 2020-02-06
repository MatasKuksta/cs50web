from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from django.shortcuts import render, redirect

# Create your views here.
def index(request):
    return render(request, "index.html")

def signup(request):
    if request.method == "POST":
        username == request.post("username")
        email == request.post("email")
        firstname == request.post("firstname")
        lastname == request.post("lastname")
        password == request.post("password")
