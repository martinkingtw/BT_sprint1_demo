from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
	email=forms.EmailField()
	USER_CHOICE =(
		(1,("Product Owner")),
		(2,("Scrum Master")),
		(3,("Developer"))
)

	position = forms.ChoiceField(choices = USER_CHOICE,  label="Position", initial='', widget=forms.Select(), required=True)


	class Meta:
		model = User
		fields = ['username', 'email', 'position','password1', 'password2']
		