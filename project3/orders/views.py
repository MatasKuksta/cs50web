from django.http                    import HttpResponse, HttpResponseRedirect
from django.contrib.auth            import authenticate
from django.contrib.auth            import login as auth_login
from django.contrib.auth            import logout as auth_logout
from django.shortcuts               import render, redirect
from django.contrib.auth.models     import User
from django.urls                    import reverse
from django.template                import RequestContext

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")
    if not request.session:
        request.session["saved"] = []
        request.session["total"] = []
    return render(request, "index.html")

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {"message": "username already exists"})
        else:
            user = User.objects.create_user(username, email, password)
            user.first_name = firstname
            user.last_name = lastname
            user.save()
            return render(request, "login.html")
    else:
        return render(request, "register.html")

def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return redirect(request, "login.html", {"message": "username and password do not match"})
    else:
        return render(request, "login.html")

def logout(request):
    auth_logout(request)
    return render(request, "login.html", {"message": "logged out user"})


def pizza(request):
    kind = request.POST["pkind"]
    size = request.POST["psize"]
    name = request.POST["pname"]
    if name == "1 topping":
        topping1 = request.POST["topping1"]


def mhelp():
    context = {
        "size": Size.objects.all(),
        "kind": Kind.objects.all(),
        "toppings": Toppings.objects.all(),
        "Sub": Sub.objects.all(),
        "Pasta": Pasta.objects.all(),
        "Salads": Salads.objects.all(),
        "Dinner": Dinner.objects.all(),
    }
    return context
