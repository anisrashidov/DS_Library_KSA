from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from PIL import Image
from Library.models import BookCode
from django.utils import timezone

class StudentManager(BaseUserManager):
	def create_user(self, email, first_name, last_name, student_ID, password = None):
		if not email:
			raise ValueError('Users must have an email address')
		if not(first_name and last_name):
			raise ValueError('Users must enter their first and last names')
		if not student_ID:
			raise ValueError('Users must enter their student ID')
		user = self.model(
				email = self.normalize_email(email),
				first_name = first_name,
				last_name = last_name,
				student_ID = student_ID,
			)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, first_name, last_name, student_ID, password):
		if not email:
			raise ValueError("Users must have an email address")
		if not( first_name and last_name ):
			raise ValueError("Users must have a first name and a last name")
		if not student_ID:
			raise ValueError("Users must have a student ID")
		user = self.create_user(
				email = self.normalize_email(email),
				first_name = first_name,
				last_name = last_name,
				student_ID = student_ID,
				password=password
			)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user

def penalty_date(days=-1):
	return timezone.now() + timezone.timedelta(days=days)


class Student(AbstractBaseUser):
	email = models.EmailField(
		max_length=100,
		verbose_name='email',
		unique=True,
		)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	student_ID = models.CharField(max_length=7, unique=True)
	is_penalized = models.BooleanField(default=False)
	penalty_date = models.DateField(default=penalty_date)
	policy_agreement = models.BooleanField()
	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)

	USERNAME_FIELD = 'student_ID'
	REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

	objects = StudentManager()

	def __str__(self):
		return self.first_name + ' ' + self.last_name

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True


class Profile(models.Model):
	user = models.OneToOneField(Student, on_delete=models.CASCADE)
	image = models.ImageField(default='default.png', upload_to='profile_pics')

	def __str__(self):
		return f"{self.user}'s Profile"

	def save(self, *args, **kwargs):
		super(Profile, self).save(*args, **kwargs)

		img = Image.open(self.image.path)

		if img.width > 500:
			k = 500 / img.width
			output_size = (500, img.height * k)
			img.thumbnail(output_size)
			img.save(self.image.path)

def f():
	return timezone.now() + timezone.timedelta(days=7)

class BorrowedBook(models.Model):
	user = models.ForeignKey(Student, on_delete=models.CASCADE)
	book = models.OneToOneField(BookCode, on_delete=models.CASCADE)
	deadline = models.DateField(default=f)
	num_of_extensions = models.IntegerField(default=0)
	is_expired = models.BooleanField(default=False)

	def __str__(self):
		return str(self.user) + ' borrowed ' + str(self.book)
	