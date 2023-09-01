from datetime import date

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm, LoanForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.utils.timezone import make_aware

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

@login_required
def library(request):
	filters = {
		'': 'All',
		'available': 'Available',
		'onloan': 'On loan',
		'duetoday': 'Due today'
	}

	showing_books = Book.objects.all()
	if request.method == 'GET':
		filter = request.GET.get('filter')
		if filter is not None:
			if filter == 'available':
				showing_books = Book.objects.filter(loan__isnull=True)
			elif filter == 'onloan':
				showing_books = Book.objects.filter(loan__isnull=False)
			elif filter == 'duetoday':
				showing_books = Book.objects.filter(loan__due_date__exact=date.today())

	return render(request, 'library.html', {'books': showing_books, 'filters': filters})

@login_required
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
			# Check the book has not been loaned already, i.e prevent user from refreshing, or attempting
			# to get a loaned book
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

@login_required
def profile(request):
	if request.method == 'POST':
		# Id of the book to return
		return_id = request.POST.get('book_return_id')

		if return_id.isdigit():
			try:
				loan_to_cancel = Loan.objects.get(borrower=request.user, book=return_id)
				loan_to_cancel.delete()
			except ObjectDoesNotExist:
				# If object does not exist, usually a refresh occurred or malicious input, ignore
				pass

	# Must come after the book has been returned, to not include it in the borrowed books
	borrowed_books = Book.objects.filter(loan__borrower=request.user)
	return render(request, 'profile.html', {'borrowed_books': borrowed_books})