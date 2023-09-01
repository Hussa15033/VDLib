from django.core.exceptions import ValidationError
from django.test import TestCase
from simplelib.models import User
from django.db.utils import IntegrityError

class UserModelTestCase(TestCase):
	def setUp(self) -> None:
		self.user = User.objects.create_user(
			username='john_smith',
			email='johnsmith@example.com',
			first_name='John',
			last_name='Smith',
			password='Password123'
		)

	# Username tests
	def test_username_must_be_unique(self):
		with self.assertRaises(IntegrityError):
			User.objects.create_user(username='john_smith', email='notjohn@example.com', password='Password123')

	def test_username_cannot_be_more_than_30_chars(self):
		self.user.username = 'a' * 31
		self._assert_user_is_invalid()

	def test_username_cannot_be_blank(self):
		self.user.username = ''
		self._assert_user_is_invalid()

	# First name tests
	def test_first_name_cannot_be_blank(self):
		self.user.first_name = ''
		self._assert_user_is_invalid()

	def test_first_name_cannot_be_more_than_30_chars(self):
		self.user.first_name = 'a' * 31
		self._assert_user_is_invalid()

	def test_first_name_can_be_30_chars(self):
		self.user.first_name = 'a' * 30
		self._assert_user_is_valid()
	# Last name tests
	def test_last_name_cannot_be_blank(self):
		self.user.last_name = ''
		self._assert_user_is_invalid()

	def test_last_name_cannot_be_more_than_30_chars(self):
		self.user.last_name = 'a' * 31
		self._assert_user_is_invalid()

	def test_last_name_can_be_30_chars(self):
		self.user.last_name = 'a' * 30
		self._assert_user_is_valid()
	# Email tests
	def test_email_cannot_be_blank(self):
		self.user.email = ''
		self._assert_user_is_invalid()

	def test_email_must_be_unique(self):
		with self.assertRaises(IntegrityError):
			User.objects.create_user(username='new_john', email='johnsmith@example.com', password='Password123')
	# Password tests
	# Helper functions
	def _assert_user_is_invalid(self):
		with self.assertRaises(ValidationError):
			self.user.full_clean()

	def _assert_user_is_valid(self):
		try:
			self.user.full_clean()
		except ValidationError:
			self.fail('The test user should be invalid')