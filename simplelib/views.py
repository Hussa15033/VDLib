from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView, LogoutView
# Create your views here.
def home(request):
	return render(request, 'index.html')

def logout_view(request):
	# Logout the user and redirect them to login page
	logout(request)
	return redirect('login')
class VDLibLoginView(LoginView):
	redirect_authenticated_user = True

	template_name = 'login.html'

	# Page to redirect to on successful login, or if already logged in
	next_page = '/library'

def register(request):
	if request.method == 'GET':
		form = RegisterForm()
		return render(request, 'register.html', {'form': form})
	elif request.method == 'POST':
		print("WORKING")
		form = RegisterForm(request.POST)
		# print(form.errors)
		if form.is_valid():
			# If the form is valid, log the user in instantly and send them to the library
			user = form.save()
			login(request, user)
			return redirect('library')
		else:
			# Invalid form, reload it and show the errors
			return render(request, 'register.html', {'form': form})


def library(request):
	return render(request, 'library.html')

