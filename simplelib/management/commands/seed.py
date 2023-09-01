from django.core.management.base import BaseCommand
import faker
import random

from simplelib.models import User, Book


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

		print("Seeding complete.")
