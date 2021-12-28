from django.urls import path
from . import views

urlpatterns = [
    path('', views.mainPage, name="library-main"),
    path('archive/', views.archive, name='library-archive'),
    path('book/<book_id>/', views.book_view, name='library-book'),
    path('book-borrow/', views.book_borrow_view, name="library-book-borrow"),
    path('notice/<notice_id>/', views.notice_view, name='library-notice'),
    path('library-policies/', views.policies_view, name="library-policies" ),
]
