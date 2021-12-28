from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistForm, UserAuthenticationForm, StudentUpdateForm, ProfileUpdateForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import BorrowedBook, Student
from django.utils import timezone
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage, send_mail, BadHeaderError
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.db.models.query_utils import Q
import threading, datetime

class EmailThread(threading.Thread):
	def __init__(self, email):
		super(EmailThread, self).__init__()
		self.email = email
	def run(self):
		self.email.send()
		print("ssuccess")



def register_view(request):
	if request.method == 'POST':
		form = UserRegistForm(request.POST)
		if form.is_valid():
			to_email = form.cleaned_data.get('email')
			if to_email.find('@ksa') == -1:
				messages.warning(request, 'Improper email address!')
				return redirect('register')
			else:
				user = form.save(commit=False)
				user.is_active = False
				user.save()
				current_site = get_current_site(request)
				message = render_to_string('Users/acc_active_email.html', {
					'user': user,
					'domain':current_site,
					'uid': urlsafe_base64_encode(force_bytes(user.pk)),
					'token': account_activation_token.make_token(user),
				})
				mail_subject = 'Activate your KSA Library account.'
				email = EmailMessage(subject=mail_subject, body=message, from_email=settings.EMAIL_HOST_USER,to=[to_email])
				# EmailThread(email).start()
				email.send()
				return redirect('registration-confirm-message')
	else:
		form = UserRegistForm()
	return render(request, 'Users/register.html', {'form': form, 'title': "Sign up, KSA students!" })


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Student.objects.get(pk=uid)
    except Exception as e:
        user = None
    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')
    else:
        return HttpResponse('Activation link is invalid!')


def confirm_message(request):
	return render(request, 'Users/confirmation_request.html', {'title': "Registration confirmation!"})


def login_view(request):
	user = request.user
	if user.is_authenticated:
		return redirect('library-main')

	if request.POST:
		form = UserAuthenticationForm(request.POST)
		if form.is_valid():
			studentID = request.POST['student_ID']
			password = request.POST['password']
			student = authenticate(student_ID = studentID, password=password)
			if student:
				login(request, student)
				messages.success(request, f'Welcome back to our library!')
				return redirect('library-main')
	else:
		form = UserAuthenticationForm()

	return render(request, 'Users/login.html', {'form': form, 'title': "Sign in to your Account"})

def logout_view(request):
	logout(request)
	return render(request, 'Users/logout.html')

@login_required
def profile(request):
	if request.user.is_penalized:
		if datetime.date.today() > request.user.penalty_date:
			user = request.user
			user.is_penalized = False
			user.save()
	if request.method == "POST":
		u_form = StudentUpdateForm(request.POST)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		if p_form.is_valid() or u_form.is_valid():
			if u_form.is_valid():
				new_password = u_form.cleaned_data['password1']
				request.user.set_password(new_password)
				request.user.save()
				student = authenticate(student_ID = request.user.student_ID, password=request.user.password)
				login(request, student)
				messages.success(request, f'Your account has been updated')
				return redirect('profile')
			if p_form.is_valid():
				p_form.save()
				messages.success(request, f'Your account has been updated')
				return redirect('profile')
	else:
		u_form = StudentUpdateForm()
		p_form = ProfileUpdateForm(instance = request.user.profile)
		if 'book_id' in request.GET:
			book_id = request.GET['book_id']
			book = BorrowedBook.objects.get(id=book_id)
			if book.num_of_extensions == 0:
				book.deadline = book.deadline + timezone.timedelta(days=7)
				book.num_of_extensions += 1
				book.save()
				return redirect('profile')
			else:
				messages.warning(request, f'You have already extended once')
				return redirect('profile')

	content = {
		'p_form': p_form,
		'u_form': u_form,
		'title': str(request.user.first_name) + "'s Profile",
	}
	borrow_books = BorrowedBook.objects.filter(user=request.user)
	for book in borrow_books:
		if book.deadline < datetime.date.today():
			book.is_expired = True
			book.save()
			user = request.user
			user.is_penalized = True
			duration = datetime.date.today() - book.deadline
			print(duration)
			user.penalty_date = datetime.date.today() + duration
			user.save()
	content['borrowed_books'] = borrow_books
	return render(request, 'Users/profile.html', content)

def password_reset_view(request):
	if request.method == 'POST':
		password_form = PasswordResetForm(request.POST)
		if password_form.is_valid():
			data = password_form.cleaned_data['email']
			try:
				user = Student.objects.get(email=data)
				print("User:", user)
				subject = 'Password Reset'
				current_site = get_current_site(request)
				message = render_to_string('Users/password_reset_message.html', {
					'user': user,
					'domain':current_site,
					'uid': urlsafe_base64_encode(force_bytes(user.pk)),
					'token': default_token_generator.make_token(user),
				})
				try:
					send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=[data], fail_silently=False )
				except:
					return HttpResponse('Invalid Header')
				return redirect('password_reset_done')
			except:
				messages.warning(request, 'Improper email address!')
				return redirect('password_reset')
	else:
		password_form = PasswordResetForm()
	content={'form': password_form}
	return render(request, 'Users/password_reset.html', content)