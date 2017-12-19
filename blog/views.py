from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from blog.ejudge import EjudgeUser
from blog.forms import *
from blog.contests import EjudgeContests

# Create your views here.
from blog.models import News, Course, Lesson, Logins

def index (request):
	return render(request, 'blog/index.html')

#Аутентификация
def login(request):
	if ('user_id' in request.session):
		return redirect('/ejudgeservice/')
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			login = form.cleaned_data['login']
			password = form.cleaned_data['password']
			try:
				user = Logins.objects.get(login=login,password=password)
			except ObjectDoesNotExist:
				error_login = "Неверные логин или пароль!"
				return render(request, 'blog/ejudge_login.html',{'form':form,'error_login':error_login})
			request.session.set_expiry(3600)
			request.session['user_id'] = user.user_id
			request.session.modified = True
			return redirect('/ejudgeservice/')
		else:
			return render(request, 'blog/ejudge_login.html',{'form':form})
	else:
		form = LoginForm(auto_id='auth_%s')
		return render(request, 'blog/ejudge_login.html',{'form':form})

def register(request):
	if ('user_id' in request.session):
		return redirect('/ejudgeservice/')
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			login = form.cleaned_data['login']
			password = form.cleaned_data['password']
			email = form.cleaned_data['email']
			try:
				user = Logins.objects.get(login=login,email=email)
				error_registration = "Пользователь с таким Login и Email уже существует!"
				return render(request, 'blog/ejudge_register.html',{'form':form,'error_reg':error_registration})
			except ObjectDoesNotExist:
				try:
					new_user = Logins.objects.create(login=login,password=password,email=email,pwdmethod=2)
				except:
					error_registration = "Неопределённая ошибка регистрации!"
					return render(request, 'blog/ejudge_register.html',{'form':form,'error_reg':error_registration})
				request.session.set_expiry(3600)
				request.session['user_id'] = new_user.user_id
				request.session.modified = True
				return redirect('/ejudgeservice/')
		else:
			return render(request, 'blog/ejudge_register.html',{'form':form})
	else:
		form = RegisterForm(auto_id='reg_%s')
		return render(request, 'blog/ejudge_register.html',{'form':form})
#Конец аутентификации

def news(request):
	#Получаем все новости
	allNews = News.objects.all().order_by("-time")

	#Передаём их в шаблон
	context = {
		'news': allNews,
	}
	return render(request, 'blog/news.html', context)

def about(request):
	return render(request, 'blog/about.html')

def ejudgeusers(request):
	if not request.user.is_authenticated():
		return redirect('/')
	if request.method == 'POST':
		if 'delete_user' in request.POST:
			user_id = request.POST['user_id']
			if (EjudgeUser.delete_user(user_id)):
				return HttpResponse("ok", content_type='text/html')
	users = EjudgeUser.get_users()
	data = []
	if not users['error']:
		data = users['data']
	return render(request, 'blog/ejudge_users.html',{'user_data':data})

def ejudge(request):
	user_data = ''
	if ('user_id' not in request.session) and (str(request.user) != 'admin'):
		return redirect('/ejudgelogin/')
	else:
		if ('user_id' in request.session):
			user_id = request.session['user_id']
			user_data = EjudgeUser.get_user_by_id(user_id)
			if(user_data['error']):
				user_data = ''
			else:
				user_data = user_data['data']
	return render(request, 'blog/ejudge.html',{'user_data':user_data})

def test(request):
	users = Logins.objects.all()

	return render(request, 'blog/test.html',{'users':users})

def courses_list(request):
	if 'user_id' not in request.session and not request.user.is_authenticated():
		return redirect('/ejudgelogin/')
	courses = Course.objects.all()
	return render(request, 'blog/courses_list.html',{'courses':courses})

def courses_detail(request,slug):
	if 'user_id' not in request.session and not request.user.is_authenticated():
		return redirect('/ejudgelogin/')
	course = get_object_or_404(Course, slug=slug)
	lessons = Lesson.objects.filter(course=course)
	return render(request, 'blog/course_detail.html',{'course':course,'lessons':lessons})

def lesson_detail(request,**kwargs):
	if 'user_id' not in request.session and not request.user.is_authenticated():
		return redirect('/ejudgelogin/')
	course = get_object_or_404(Course, slug=kwargs.get('course'))
	lesson = get_object_or_404(Lesson, course=course, slug=kwargs.get('slug'))
	return render(request, 'blog/lesson_detail.html',{'course':course,'lesson':lesson})

def contests(request):
	if 'user_id' not in request.session:
		return redirect('/ejudgelogin/')
	user_id = request.session['user_id']
	#AJAX action
	if request.method == 'POST':
		if 'contest_id' in request.POST and 'delete_contest' not in request.POST:
			contest_id = request.POST['contest_id']
			if not EjudgeContests.register_exist(user_id,contest_id):
				error = EjudgeContests.register_to_contest(user_id,contest_id)['error']
				return HttpResponse(error, content_type='text/html')
		if 'delete_contest' in request.POST:
			contest_id = request.POST['contest_id']
			if(EjudgeContests.delete_contests(user_id,contest_id)):
				return HttpResponse("ok", content_type='text/html')
	user_contests_ids = EjudgeContests.get_user_contest(user_id)['data']
	avaliable_contests = EjudgeContests.get_contests_data(user_contests_ids,False)
	used_contests = EjudgeContests.get_contests_data(user_contests_ids,True)
	return render(request, 'blog/contests.html',{'avaliable':avaliable_contests,'used':used_contests})

def logout(request):
	if ('user_id' in request.session):
		del request.session['user_id']
		request.session.modified = True
		return redirect('/')
	else:
		return redirect('/')

def ejudgeaction(request):
	if request.method == 'POST':
		if 'action' in request.POST:
			answer = EjudgeUser.do_control_action(request.POST['action'])
			return HttpResponse(answer, content_type='text/html')
		else:
			return HttpResponse('Bad Data', content_type='text/html')
	else:
		return HttpResponse('Bad Data', content_type='text/html')