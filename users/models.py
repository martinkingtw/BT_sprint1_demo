from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from project.models import Project

# Create your models here.


class MyAccountManager(BaseUserManager):
	def create_user(self,email,username,password=None):
		if not email:
			raise ValueError("Users must have an email address")

		if not username:
			raise ValueError("Users must have username")

		user = self.model(
				email=self.normalize_email(email),
				username=username,

			)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user=self.create_user(
				email=self.normalize_email(email),
				password=password,
				username=username,

			)

		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class User(AbstractBaseUser):



	email				=	models.EmailField(verbose_name="email",max_length=60, unique=True)
	position			=	models.CharField(
								max_length=32,

							)
	first_name			=	models.CharField(max_length=30, unique=False, default=False)
	last_name			= 	models.CharField(max_length=20, unique=False, default = False)
	username			=	models.CharField(max_length=10,unique=True)
	date_joined			=	models.DateTimeField(verbose_name='date joined', auto_now_add = True)
	last_login			=	models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin			=	models.BooleanField(default=False)
	is_active			=	models.BooleanField(default=True)
	is_staff			=	models.BooleanField(default=False)
	is_superuser		=	models.BooleanField(default=False)
	project 			= 	models.ForeignKey(Project, models.SET_NULL, null=True, blank=True)


	USERNAME_FIELD	=	'email'
	REQUIRED_FIELDS	=	['username',]


	objects = MyAccountManager()

	def __str__(self):
		return self.username

	def has_perm(self,perm,obj=None):
		return self.is_admin

	def has_module_perms(self,app_label):
		return True




class Profile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	#image = models.ImageField(default='default.jpg', upload_to='profile_pics')


	def __str__(self):
		return f'{self.user.username} Profile'


