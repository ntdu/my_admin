from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from user.forms import CreateUserForm
from user.forms import LoginForm


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

    return render(request, "user/investor/login.html", {"form": form, "msg" : msg})


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
    
    return render(request, 'user/investor/register.html', { 'form': form })


def logout_view(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)


@login_required
def change_password(request):
    if request.method == 'GET': return render(request, 'user/investor/change_password.html')
    
    old_password = request.POST.get('old_password')
    if not request.user.check_password(old_password): 
        return render(request, 'user/investor/change_password.html', {'error_old_password': 'Nhập sai mật khẩu!'})
    
    new_password = request.POST.get('new_password')
    confirm_new_password = request.POST.get('confirm_new_password')
    if new_password != confirm_new_password:
        return render(request, 'user/investor/change_password.html', {'error_confirm_new_password': 'Mật khẩu không khớp!', 'old_password': old_password})

    request.user.set_password(confirm_new_password)
    request.user.save()

    return login(request)

