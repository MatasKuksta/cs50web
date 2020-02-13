from django.http                    import HttpResponse, HttpResponseRedirect
from django.contrib.auth            import authenticate
from django.contrib.auth            import login as auth_login
from django.contrib.auth            import logout as auth_logout
from django.shortcuts               import render, redirect
from django.contrib.auth.models     import User
from django.urls                    import reverse
from django.template                import RequestContext
from .models                        import Toppings, Subs, Pasta, Salads, Platters, Size, Kind, Pizza

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")
    if not request.session:
        request.session["saved"] = []
        request.session["total"] = []
    content = mhelp()
    return render(request, "index.html", content)

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
            return redirect(request, "error.html")
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
        topping2 = '0'
        topping3 = '0'
    elif name == "2 toppings":
        topping1 = request.POST["topping1"]
        topping2 = request.POST["topping2"]
        topping3 = '0'
    elif name == "3 toppings":
        topping1 = request.POST["topping1"]
        topping2 = request.POST["topping2"]
        topping3 = request.POST["topping3"]
    else:
        topping1 = '0'
        topping2 = '0'
        topping3 = '0'
    content = mhelp()
    price = Pizza.objects.all().filter(name=name, kind_kind=kind, size_size=size)
    price = price.values_list("price", flat=True)[0]
    saved_list = request.session.get("saved", [])
    saved_list.append([kind, size, name, topping1, topping2, topping3, str(price)])
    request.session["saved"] = saved_list
    totals = request.session.get("total", [])
    if len(totals) == 0:
        totals.append(price)
        request.session["total"] = totals
    else:
        totals[0] = totals[0] + price
    content["total"] = request.session.get("total", [])
    content["ordered"] = request.session.get("saved", [])
    return render(request, "index.html", content)

def mhelp():
    content = {
        "size": Size.objects.all(),
        "kind": Kind.objects.all(),
        "toppings": Toppings.objects.all(),
        "Sub": Subs.objects.all(),
        "Pasta": Pasta.objects.all(),
        "Salads": Salads.objects.all(),
        "Dinner": Platters.objects.all(),
    }
    return content
