from django.shortcuts import render, redirect

from .forms import LoginForm
from .models import BoardMember
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse

def register(request):
	if request.method == 'GET':
		return render(request, 'register.html')

	elif request.method == 'POST':
		username = request.POST.get('username', None)
		email = request.POST.get('email', None)
		password = request.POST.get('password', None)
		re_password = request.POST.get('re_password', None)

		res_data = {}
		if not (username and password and re_password and email):
			res_data['error'] = '모든 값을 입력하세요!'

		elif password != re_password:
			res_data['error'] = '비밀번호가 다릅니다'

		else:
			member = BoardMember(
				username=username,
				password=make_password(password),
				email=email,
			)
			member.save()
			res_data['error'] = '회원가입에 성공하였습니다.'


		return render(request, 'register.html', res_data)

def login(request):
	if request.method == "POST":
		form = LoginForm(request.POST)
		# 폼 객체, 폼 클래스를 만들 때 괄호에 POST 데이터를 담아준다.
		# POST 안에 있는 데이터가 form 변수에 들어간다.
		if form.is_valid():  # 장고 폼에서 제공하는 검증 함수 is_valid()
			request.session['user'] = form.user_id
			# session_code 검증
			return redirect('/')
	else:
		form = LoginForm()
	# 빈 클래스 변수를 만든다.
	return render(request, 'login.html', {'form': form})


def Home(request):
		return render(request, 'home.html')

def logout(request):
    if request.session.get('user'):
        del(request.session['user'])

    return redirect('/')