
from django.contrib import admin
from django.urls import path
from .views import Index, SignUpView
from django.contrib.auth import views as authViews

urlpatterns = [
  path('', Index.as_view(), name='index'),
	path('signup/', SignUpView.as_view(), name='signup'),
	path('login/', authViews.LoginView.as_view(template_name='inventory/login.html'), name='login'),
	path('logout/', authViews.LogoutView.as_view(template_name='inventory/logout.html'), name='logout'),
]
