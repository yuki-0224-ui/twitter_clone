from django.urls import path
from . import views

app_name = 'tweets'
urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/login/', views.login, name='account_login'),
    path('accounts/signup/', views.signup, name='account_signup'),
    path('accounts/logout/', views.logout, name='account_logout'),
]
