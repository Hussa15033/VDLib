from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login, authenticate, logout
# Create your views here.
def home(request):
	return render(request, 'index.html')

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

