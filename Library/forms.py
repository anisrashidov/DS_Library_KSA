from django import forms

class SearchFilterOptions(forms.Form):
	CHOICES = [
		['Title', 'Title'],
		['Author', 'Author']
	]
	Criteria = forms.CharField(widget=forms.RadioSelect(
		choices=CHOICES),initial=["Title", "Title"], required = True)


	GENRES = (
		('All Genres', 'All Genres'),
		('Fantasy', 'Fantasy'),
		('Adventure', 'Adventure'),
		('Romance', 'Romance'),
		('Contemporary', 'Contemporary'),
		('Dystopian', 'Dystopian'),
		('Mystery', 'Mystery'),
		('Horror', 'Horror'),
		('Thriller', 'Thriller'),
		('Paranormal', 'Paranormal'),
		('Historical fiction', 'Historical fiction'),
		('Science Fiction', 'Science Fiction'),
		('Children', 'Children'),
		('Memoir', 'Memoir'),
		('Cooking', 'Cooking'),
		('Art', 'Art'),
		('Self-help / Personal', 'Self-help / Personal'),
		('Development', 'Development'),
		('Motivational', 'Motivational'),
		('Health', 'Health'),
		('History', 'History'),
		('Travel', 'Travel'),
		('Guide', 'Guide'),
		('Family', 'Family'),
		('Humor', 'Humor'),
		('novel', "Novel"),
		('Economics', 'Economics'),
		('Standardized Tests', "Standardized Tests"),
		('Mathematics', 'Mathematics'),
		('Physics', 'Physics'),
		('Chemistry', 'Chemistry'),
		('Biology', 'Biology'),
	)
	Genre = forms.ChoiceField(choices=GENRES, required=True)


class BookCodeForm(forms.Form):
	code = forms.CharField(max_length=100)
