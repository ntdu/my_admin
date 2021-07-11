from django.shortcuts import render, redirect
from user.forms import CreateUserForm
from user.forms import LoginForm
from django.contrib.auth import authenticate, login


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:    
                msg = 'Tài khoản hoặc mật khẩu không đúng!'    
        else:
            msg = 'Thông tin nhập không đúng định dạng'    

    return render(request, "user/login.html", {"form": form, "msg" : msg})


# Create your views here.
def register(request):
    form = None

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/login/")

    else:
        form = CreateUserForm(initial={})
    
    return render(request, 'user/register.html', { 'form': form })