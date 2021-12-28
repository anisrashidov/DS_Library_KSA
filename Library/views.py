from django.shortcuts import render, redirect
from .models import *
from .forms import SearchFilterOptions
from django.contrib.auth.decorators import login_required
from Users.models import BorrowedBook
from django.contrib import messages

def mainPage(request):
	recommendations = Recommendation.objects.all()
	content = {
		"title": "Welcome to KSA Library!",
		'recommendations': recommendations,
		'notices': Notice.objects.all(),
	}
	return render(request, 'Library/main.html', content)

def archive(request):
	content = {
		'title': 'Welcome to Library archive',
		'archive': True,
		'books': Book.objects.all(),
	}
	filters = SearchFilterOptions()
	content['filters'] = filters
	if request.method == "POST":
		search = request.POST['searched']
		content['search'] = search
		content['books'] = Book.objects.filter(title__contains=search)
	elif request.method == "GET":
		if 'search-main' in request.GET:
			search = request.GET.get('search-main')
			criteria = request.GET.get('Criteria')
			genre = request.GET.get('Genre')
			if genre == 'All Genres':
					genre = ''
			if criteria == 'Title':
				content['books'] = Book.objects.filter(title__contains=search, genre__contains=genre)
			elif criteria == 'Author':
				content['books'] = Book.objects.filter(authors__contains=search, genre__contains=genre)

	return render( request, 'Library/archive.html', content )

@login_required
def book_view(request, book_id=0):
	content = dict()
	book = Book.objects.get(id=book_id)
	content['title']=book.title
	content['book'] = book
	content['book_count'] = book.bookcode_set.filter(borrowed=False).count()
	if request.method == "POST":
		comment_student_ID = request.user.student_ID
		comment_body = request.POST['comment-textarea']
		CommentBook(book=book, student_ID=comment_student_ID, body=comment_body).save()
		return redirect('library-book', book_id=book_id)


	return render(request, 'Library/book.html', content)

@login_required
def notice_view(request, notice_id=0):
	content = dict()
	notice = Notice.objects.get(id=notice_id)
	content['title']=notice.title
	content['notice'] = notice
	if request.method == "POST":
		comment_student_ID = request.user.student_ID
		comment_body = request.POST['comment-textarea']
		CommentNotices(notice=notice, student_ID=comment_student_ID, body=comment_body).save()
		return redirect('library-notice', notice_id=notice_id)
	return render(request, 'Library/notice.html', content)

@login_required
def book_borrow_view(request):
	content = {'title': 'Borrow a Book!'}

	if request.method == 'POST':
		book_code = request.POST['code_field']
		book = BookCode.objects.get(code=book_code)
		if not book:
			messages.warning(request, 'Wrong book code! No books with such a code found!!!')
		elif book.borrowed:
			messages.error(request, 'Wrong book code! The book with this code is already borrowed!!!')
		else:
			book.borrowed = True
			book.save(update_fields=['borrowed'])
			borrow_book = BorrowedBook(user=request.user, book=book)
			borrow_book.save()
			messages.success(request, f"{book.book.title} has been added to your borrow-list!")
		return redirect('library-book-borrow')


	return render( request, 'Library/book_borrow.html', content)

def policies_view(request):
	return render(request, 'Library/policies.html', {'title': 'Library Policies', 'archive': True} )