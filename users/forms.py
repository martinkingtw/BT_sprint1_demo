from django import forms
from users.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
	email=forms.EmailField(max_length=60, help_text='Required. Add a valid email address')
	USER_CHOICE =(
	
		(2,("Manager")),
		(3,("Developer"))
)

	position = forms.ChoiceField(choices = USER_CHOICE,  label="Position", initial='', widget=forms.Select(), required=True)


	class Meta:
		model = User
		fields = ['username', 'email', 'position','password1', 'password2']
		