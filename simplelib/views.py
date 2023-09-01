from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm, LoanForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView, LogoutView

from .models import Book, Loan


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
	return render(request, 'library.html', {'books': Book.objects.all()})

def book_view(request, book_id):
	try:
		book = Book.objects.get(id=book_id)
	except ObjectDoesNotExist:
		raise Http404

	if request.method == 'GET':
		form = LoanForm()

	if request.method == 'POST':
		form = LoanForm(request.POST)
		if form.is_valid():
			# Check the book has not been loaned already, i.e prevent user from refreshing
			try:
				loan = Loan.objects.get(book=book)
			except ObjectDoesNotExist:
				loan = None
				
			if loan is None:

				# The user entered a correct date, create a new Loan for them
				Loan.objects.create(
					borrower=request.user,
					book=book,
					due_date=form.cleaned_data.get('due_date')
				)

	return render(request, 'book.html', {'book': book, 'form': form})