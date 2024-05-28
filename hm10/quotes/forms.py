from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from quotes.models import Author, Quote, Tag



class RegisterForm(UserCreationForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']


class AuthorForm(forms.ModelForm):
	class Meta:
		model = Author
		fields = ['fullname', 'born_date', 'born_location', 'description']


class QuoteForm(forms.ModelForm):
	author = forms.ModelChoiceField(queryset=Author.objects.all().order_by('fullname'), required=True)
	tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all().order_by('name'), required=True,
	                                      widget=forms.SelectMultiple)

	class Meta:
		model = Quote
		fields = ['text', 'author', 'tags']



