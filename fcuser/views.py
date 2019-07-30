from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.hashers import make_password, check_password
from .models import Fcuser, FcuserValidation
from .forms import LoginForm
from libs.exporter import send_mail
import hashlib
import datetime
# Create your views here.


def home(request):
    return render(request, 'home.html')


def logout(request):
    if request.session.get('user'):
        del(request.session['user'])

    return redirect('/')

def validation(request):
    key = request.GET.get('k')

    try:
        validation = FcuserValidation.objects.get(hashkey=key)
        validation.fcuser.is_authenticated = True
        validation.fcuser.save()
    # if FcuserValidation.objects.filter('hashkey'=key):
    #     Fcuser.is_authenticated
        return redirect('/')
    except FcuserValidation.DoesNotExist:
        pass

    return HttpResponse('<script>alert("잘못된 접근");</script>')
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            request.session['user'] = form.user_id
            return redirect('/')
    else:
        # GET
        token = request.GET.get('token')
        if token:
            from google.oauth2 import id_token
            from google.auth.transport import requests # google-api-python-client #reqeusts
            from django.conf import settings

            try:
                info = id_token.verify_oauth2_token(token, requests.Request(), settings.GOOGLE_CLIENT_ID)
                fcuser = Fcuser.objects.get(useremail=info['email'])
                request.session['user'] = fcuser.id

                return redirect('/')
            except Fcuser.DoesNotExists:
                #회원가입 후 리다이렉트 or 회원가입페이지
                pass

        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        username = request.POST.get('username', None)
        useremail = request.POST.get('useremail', None)
        password = request.POST.get('password', None)
        re_password = request.POST.get('re-password', None)

        res_data = {}

        if not (username and useremail and password and re_password):
            res_data['error'] = '모든 값을 입력해야합니다.'
        elif password != re_password:
            res_data['error'] = '비밀번호가 다릅니다.'
        else:
            fcuser = Fcuser(
                username=username,
                useremail=useremail,
                password=make_password(password),
                level=1
            )

            fcuser.save()

            code = username + str(datetime.datetime.now())
            validation = FcuserValidation(
                fcuser=fcuser,
                hashkey=hashlib.sha256(code.encode()).hexdigest()
            )
            validation.save()

            title = '%s님 이메일 인증' % username
            contents = '''이메일 인증을 하시려면 아래 링크를 눌러주세요
            <a href="http://localhost:8000/fcuser/validation?k=%s">링크</a>'''% validation.hashkey

            send_mail(useremail, title, contents)

            return redirect('/')

        return render(request, 'register.html', res_data)


class PublisherList(ListView):
    model = Fcuser
