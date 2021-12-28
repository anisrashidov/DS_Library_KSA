from django.contrib import admin
from .models import Book, BookCode, Recommendation, Notice, CommentBook, CommentNotice

admin.site.register(Book)
admin.site.register(BookCode)
admin.site.register(Recommendation)
admin.site.register(Notice)
admin.site.register(CommentBook)
admin.site.register(CommentNotice)