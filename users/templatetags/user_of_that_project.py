from django import template
from users.models import User
from project.models import Project



register = template.Library()

@register.simple_tag
def project_developer(request):
	if request.user.is_authenticated:
		return request.user.project.first()
	else:
		return False