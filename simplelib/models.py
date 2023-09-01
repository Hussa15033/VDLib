from datetime import date

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

''' 
	We create a custom user model as it is more flexible,
	and we can use custom validators
'''


class User(AbstractUser):
	username = models.CharField(
		max_length=30,
		unique=True
	)

	first_name = models.CharField(max_length=30, blank=False)
	last_name = models.CharField(max_length=30, blank=False)
	email = models.EmailField(unique=True, blank=False)


class Book(models.Model):
	image_url = models.URLField(max_length=150)
	title = models.CharField(max_length=80, unique=False)
	description = models.CharField(max_length=200)

	def _get_loan(self):
		if Loan.objects.filter(book=self).count() == 0:
			return None
		return Loan.objects.get(book=self)

	def is_available(self):
		# Returns a boolean of if this book is available or not
		return self._get_loan() is None

	def due_date(self):
		loan = self._get_loan()
		if loan is None:
			return None

		return loan.due_date

	def due_today(self):
		due_date = self.due_date()
		if due_date is None:
			return

		return due_date == date.today()

	def borrower(self):
		loan = self._get_loan()
		if loan is None:
			return None

		return loan.borrower



# This class models an active loan
class Loan(models.Model):
	# Set on delete to models.PROTECT, incase trying to delete a book/user
	# while it is currently in an active loan
	borrower = models.ForeignKey(User, on_delete=models.PROTECT)
	book = models.ForeignKey(Book, on_delete=models.PROTECT)

	# The date/time the book was taken out
	taken = models.DateTimeField(auto_now=False, auto_now_add=True)

	due_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)

	class Meta:
		ordering = ['due_date']

		# The following constraint means a user cannot take the same book out more than once
		# as django does not allow multiple primary keys
		constraints = [
			models.UniqueConstraint(
				fields = ['borrower', 'book'],
				name='unique_book_borrower_loan'
			)
		]
