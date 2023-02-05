from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
# 首页登录
def sign_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            # 保存登录会话
            login(request, user)
            return redirect("/dashboard")
        else:
            return render(request, 'login.html', {'error': '用户名或密码错误！'})

    return render(request, 'login.html')


@login_required
def logout(request):
    logout(request)
    return redirect("login/")


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')
