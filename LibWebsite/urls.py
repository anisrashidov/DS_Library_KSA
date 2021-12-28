"""LibWebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from Users.views import register_view as student_registration_view
from Users.views import login_view as student_login_view
from Users.views import logout_view as student_logout_view
from Users.views import profile as profile_view
from Users.views import confirm_message as confirm_message_view
from Users.views import activate as activate_view
from Users.views import password_reset_view
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('djadmin/', admin.site.urls),
    path('admin/', include('AdminPanel.urls')),
    path('', include('Library.urls')),
    path('register/', student_registration_view, name='register'),
    path('login/', student_login_view, name='login'),
    path('logout/', student_logout_view, name='logout' ),
    path('profile/', profile_view, name='profile' ),
    path('registration-confirm', confirm_message_view, name="registration-confirm-message" ),
    path('activate/<uidb64>/<token>', activate_view, name="account-activate" ),
    path('password_reset/', password_reset_view, name='password_reset' ),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='Users/password_reset_sent.html'), name='password_reset_done' ),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='Users/password_reset_confirm.html'), name='password_reset_confirm' ),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="Users/password_reset_complete.html"), name='password_reset_complete' ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)