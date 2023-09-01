from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from .models import User, Loan
from django import forms
from datetime import date

class LoginForm(forms.Form):
	username = forms.CharField(label='Username')
	password = forms.CharField(label='Password', widget = forms.PasswordInput())

class RegisterForm(UserCreationForm):
	class Meta:
		model=User
		fields=['username', 'first_name', 'last_name', 'email']

class DateInput(forms.DateInput):
    input_type = 'date'
class LoanForm(forms.Form):
	due_date = forms.DateField(widget=DateInput())

	def clean(self):
		super().clean()
		if (self.cleaned_data.get('due_date') <= date.today()):
			self.add_error('due_date', 'Return date must be in the future')
