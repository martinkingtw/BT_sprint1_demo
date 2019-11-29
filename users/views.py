from django.shortcuts import render, redirect

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm



from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib.auth.decorators import login_required

from django.views.generic import ListView
from users.models import User

def register(request):
	context = {}
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)


		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email')
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(email=email, password=raw_password)
			messages.success(request,f'Your account has been created! Now you can login!')
			return redirect('login')

		else:
			context['registeration_form'] = form



	else:
		form = UserRegisterForm()
	return render(request,'users/register.html',{'form':form})

@login_required
def profile(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST,instance=request.user)

		if u_form.is_valid():
			u_form.save()
			messages.success(request,f'Your account has been updated!')
			return redirect("profile")

	else:
		u_form = UserUpdateForm(instance=request.user)


	return render(request, 'users/profile.html',{'u_form':u_form})


def user_list(request):
	all_users = User.objects.order_by('username')

	context ={'users':all_users}

	return render(request, 'users/list.html', context)