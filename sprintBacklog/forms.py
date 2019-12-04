from django import forms
from sprintBacklog.models import Task
from project.models import Project
from users.models import User
from django.shortcuts import get_object_or_404

class TaskForm(forms.ModelForm):
	def __init__(self, project, *args, **kwargs):
		super(TaskForm,self).__init__(*args,**kwargs)
		self.fields['task_owner'] = forms.ModelChoiceField(queryset=User.objects.filter(project=project, position=3), required=False)

	# position = forms.ChoiceField(choices = USER_CHOICE,  label="Position", initial='', widget=forms.Select(), required=True)
	task_owner = forms.ModelChoiceField(queryset=User.objects.filter(position=3))

	class Meta:
		model = Task
		fields = [	'title',
					'task_owner',
					'status',
					'effort',
					'details' ]

class TaskCreateForm(forms.ModelForm):
	def __init__(self, project, *args, **kwargs):
		super(TaskCreateForm, self).__init__(*args, **kwargs)
		self.fields['task_owner'] = forms.ModelChoiceField(queryset=User.objects.filter(project=project, position=3),
														   required=False)

	# position = forms.ChoiceField(choices = USER_CHOICE,  label="Position", initial='', widget=forms.Select(), required=True)
	task_owner = forms.ModelChoiceField(queryset=User.objects.filter(position=3))

	class Meta:
		model = Task
		fields = ['title',
				  'task_owner',
				  'effort',
				  'details']
