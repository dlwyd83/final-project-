from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import LoginForm, RegisterForm

User = get_user_model()


def index(request):
    if request.user.is_authenticated is False:
        request.user.username = "Anonymous User!"
    return render(request, "index.html")


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/login")
    else:
        logout(request)
        form = RegisterForm()
    return render(request, "register.html", {"form": form})



def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=raw_password)

            if user is not None:
                login(request, user)
            return HttpResponseRedirect("/")
        return render(request, "login.html", {"form": form})
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")


@login_required(login_url="/login")
def user_list_view(request):
    page = int(request.GET.get("page", 1))
    users = User.objects.all().order_by("-id")
    paginator = Paginator(users, 1)
    users = paginator.get_page(page)

    return render(request, "users.html", {"users": users})
