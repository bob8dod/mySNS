from django.shortcuts import render, redirect
from .models import UserModel
from django.http import HttpResponse
from django.contrib.auth import get_user_model  # 사용자가 데이터베이스 안에 있는지 검사하는 함수
from django.contrib import auth  # 인증기능 모듈
from django.contrib.auth.decorators import login_required


# Create your views here.
def sign_up_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/signup.html')
    elif request.method == 'POST':
        username = request.POST.get('username', '') # 값이 없다면 None으로 보내고 있음
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        bio = request.POST.get('bio', '')

        if password != password2:
            return render(request, 'user/signup.html', {'error': 'Check your password'})
        else:
            if username == '' or password == '':
                return render(request, 'user/signup.html', {'error': 'ID and Password is required'})

            exist_user = get_user_model().objects.filter(username=username)
            if exist_user:
                return render(request, 'user/signup.html', {'error': 'ID is already existed'})
            else:
                UserModel.objects.create_user(username=username, password=password, bio=bio)
                # new_user = UserModel()
                # new_user.username = username
                # new_user.password = password
                # new_user.bio = bio
                # new_user.save()
        return redirect('/sign-in')


def sign_in_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        #  me = UserModel.objects.get(username=username)
        me = auth.authenticate(request, username=username,
                               password=password)  # username과 password가 일치하는 지를 한번에 판단 후 가져옴
        if me is not None:
            auth.login(request, me)  # 로그인 시켜줌 # request.session['user'] = me.username
            return redirect('/')
        else:
            return render(request, 'user/signin.html', {'error': 'Check your ID or Password'})
    elif request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/signin.html')


@login_required  # 사용자가 로그인이 되어있어야만 접근 가능한 함수라고 선언
def logout(request):
    auth.logout(request)
    return redirect('/')

# user/views.py

@login_required
def user_view(request):
    if request.method == 'GET':
        # 사용자를 불러오기, exclude와 request.user.username 를 사용해서 '로그인 한 사용자'를 제외하기
        user_list = UserModel.objects.all().exclude(username=request.user.username)
        return render(request, 'user/user_list.html', {'user_list': user_list})


@login_required
def user_follow(request, id):
    me = request.user
    click_user = UserModel.objects.get(id=id)
    if me in click_user.followee.all():
        click_user.followee.remove(request.user)
    else:
        click_user.followee.add(request.user)
    return redirect('/user')
