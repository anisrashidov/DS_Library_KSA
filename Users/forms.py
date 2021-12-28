from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import Student, Profile
from django.contrib.auth import login, authenticate
from django.template.loader import render_to_string

class UserRegistForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text = "Required. KSA email address only! <i>e.g. **-***@ksa.hs.kr</i> ")
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    student_ID = forms.CharField(label="Student ID", max_length=7, required=True)
    policy_agreement = forms.BooleanField(label="I agree to the terms and conditions listed in the Library Policies!")

    class Meta:
    	model = Student
    	fields = ['email', 'first_name', 'last_name', 'student_ID', 'password1', 'password2', 'policy_agreement']

class UserAuthenticationForm(forms.ModelForm):
    student_ID = forms.CharField(label="Student ID")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = Student
        fields = ['student_ID', 'password']

    def clean(self):
        student_ID = self.cleaned_data['student_ID']
        password =self.cleaned_data['password']
        if not authenticate(student_ID = student_ID, password=password):
            raise forms.ValidationError("Invalid Student ID or Password")
        


class StudentUpdateForm(forms.Form):
    password1 = forms.CharField(label="New Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm New Password", widget=forms.PasswordInput)
    class Meta:
        model = Student
        fields = ['password1', 'password2']

    def clean_password(self):
        if self.data['password1'] != self.data['password2']:
            raise forms.ValidationError('Passwords are not the same')
        return self.data['password1']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']




