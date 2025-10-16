from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from system.forms import LoginForm
from pages.models import Webpage, Slider

def login_view(request):
	form = LoginForm(request.POST or None)
	context = {'form': form}
	if request.method == 'POST' and form.is_valid():
		user = authenticate(
			request,
			username=form.cleaned_data["username"],
			password=form.cleaned_data["password"]
		)
		if user:
			login(request, user)
			return redirect(request.GET.get('next', '/'))
		context['error_message'] = 'Логін або пароль введений невірно'
	return render(request, "system/login_view.html", context)

@login_required
def logout_view(request):
	logout(request)
	return redirect('login_url')

########################################################################################

def home_view(request):
	template = 'system/home_view.html'
	context = {}
	context['sliders'] = Slider.objects.all()
	news = Webpage.objects.get(parent__slug='nuwm', slug='news')
	context['news'] = news.children.all().order_by('-id')[:3]
	return render(request, template, context)

def app_view(request):
	template = 'system/app_view.html'
	context = {}
	return render(request, template, context)

def privacy_policy_view(request):
	template = 'system/privacy_policy_view.html'
	context = {}
	return render(request, template, context)