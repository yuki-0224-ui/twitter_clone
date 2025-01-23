from django.urls import path
from . import views

app_name = 'tweets'
urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/login/', views.login, name='account_login'),
    path('accounts/signup/', views.signup, name='account_signup'),
    path('accounts/logout/', views.logout, name='account_logout'),
    path('@<str:username>/', views.profile, name='profile'),
    path('settings/profile/', views.profile_edit, name='profile_edit'),
    path('tweet/<int:pk>/', views.tweet_detail, name='tweet_detail'),
    path('tweet/<int:pk>/like/', views.like_tweet, name='like_tweet'),
    path('tweet/<int:pk>/retweet/', views.retweet_tweet, name='retweet'),
    path('tweet/<int:pk>/bookmark/', views.bookmark_tweet, name='bookmark'),
    path('@<str:username>/follow/', views.follow_user, name='follow'),
    path('bookmarks/', views.bookmark_list, name='bookmarks'),
    path('messages/', views.message_room_list, name='messages'),
    path('messages/new/<str:username>/',
         views.create_message_room, name='create_message_room'),
    path('notifications/', views.notification_list, name='notifications'),
]
