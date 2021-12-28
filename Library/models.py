from django.db import models
from PIL import Image

class Book(models.Model):
	image = models.ImageField(default='default_book.jpg', upload_to='book_pics')
	title = models.CharField(max_length=200)
	authors = models.CharField(max_length=100)
	genre = models.CharField(max_length=100, default="novel")
	description = models.TextField()

	def __str__(self):
		return f"{self.title} written by {self.authors}"

class BookCode(models.Model):
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	code = models.CharField(max_length=30)
	borrowed = models.BooleanField(default=False)

	def __str__(self):
		return self.book.title + ": " + self.code

class Recommendation(models.Model):
	book = models.OneToOneField(Book, related_name='recommendations', on_delete=models.CASCADE, unique=True)

	def __str__(self):
		return str(self.book)

class Notice(models.Model):
	image = models.ImageField(default="notice_default.png", upload_to='notice_pics')
	title = models.CharField(max_length=200)
	description = models.TextField()

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		super(Notice, self).save(*args, **kwargs)

		img = Image.open(self.image.path)

		if img.width > 500:
			k = 500 / img.width
			output_size = (500, img.height * k)
			img.thumbnail(output_size)
			img.save(self.image.path)

class CommentBook(models.Model):
	book = models.ForeignKey(Book, related_name='comments', on_delete=models.CASCADE)
	student_ID = models.CharField(max_length=60)
	body = models.TextField()

	def __str__(self):
		return f'Comment by {self.student_ID}'

class CommentNotice(models.Model):
	notice = models.ForeignKey(Notice, related_name='comments', on_delete=models.CASCADE)
	student_ID = models.CharField(max_length=60)
	body = models.TextField()

	def __str__(self):
		return f'Comment by {self.student_ID}'