import datetime

from django.core.management.base import BaseCommand
import faker
import random

from simplelib.models import User, Book, Loan
import random
from datetime import date

class Command(BaseCommand):
	def __init__(self):
		super().__init__()
		self.faker = faker.Faker('en_GB')

	def handle(self, *args, **options):
		# Create 30 random users
		print("Seeding users...")
		for i in range(30):
			user = User.objects.create_user(
				username=self.faker.user_name(),
				first_name=self.faker.first_name(),
				last_name=self.faker.last_name(),
				email=self.faker.email(),
				password=self.faker.password()
			)

			user.full_clean()
			user.save()

		# Create 40 random books
		print("Seeding books..")
		for i in range(40):
			book = Book.objects.create(
				image_url=self.faker.image_url(height=480, width=300),
				title=" ".join(self.faker.words(nb=random.randint(1, 6))),
				description=self.faker.text()
			)


		# Create loans at random
		print("Seeding loans..")
		for i in range(20):
			# Select a book that is not being loaned, at random
			book = Book.objects.filter(loan__isnull=True).order_by('?').first()

			# Select a user at random that is not borrowing a book
			user = User.objects.filter(loan__isnull=True).order_by('?').first()

			# Create due date some time in the near future, with a 20% probability of it being today
			if random.random() < 0.2:
				due_date = date.today()
			else:
				due_date = date.today() + datetime.timedelta(days=random.randint(1, 30))

			Loan.objects.create(
				borrower=user,
				book=book,
				due_date=due_date
			)

		print("Seeding complete.")
