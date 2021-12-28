from django.contrib import admin
from .models import Student, Profile, BorrowedBook

admin.site.register(Student)
admin.site.register(Profile)
admin.site.register(BorrowedBook)

