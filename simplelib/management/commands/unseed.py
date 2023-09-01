from django.core.management.base import BaseCommand
import faker
import random

from simplelib.models import User, Book, Loan


class Command(BaseCommand):
	def __init__(self):
		super().__init__()
		self.faker = faker.Faker('en_GB')

	def handle(self, *args, **options):
		print("Deleting loans..")
		Loan.objects.all().delete()

		print("Deleting users..")
		User.objects.all().delete()

		print("Deleting books..")
		Book.objects.all().delete()

		print("Unseeding complete.")
