from django.conf.urls import url, include
from django.contrib import admin
from profiles.views import FollowToggleAPIView, FriendToggleAPIView, ProfileAPIDetailView
from .views import (
				UserDetailAPIView, 
				UserPostAPIView, 
				UserFollowersAPIView, 
				UserFollowingsAPIView, 
				UserFriendsAPIView
				)

app_name= 'accounts'

urlpatterns = [
    url(r'^(?P<username>\w+)/$', UserDetailAPIView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/profile/$', ProfileAPIDetailView.as_view(), name='profile'),
    url(r'^(?P<username>\w+)/posts/$', UserPostAPIView.as_view(), name='post-list'),
    url(r'^(?P<username>\w+)/follow/$', FollowToggleAPIView.as_view(), name='follow-toggle'),
    url(r'^(?P<username>\w+)/friend/$', FriendToggleAPIView.as_view(), name='friend-toggle'),
    url(r'^(?P<username>\w+)/followers/$', UserFollowersAPIView.as_view(), name='followers-list'),
    url(r'^(?P<username>\w+)/followings/$', UserFollowingsAPIView.as_view(), name='followings-list'),
    url(r'^(?P<username>\w+)/friends/$', UserFriendsAPIView.as_view(), name='friends-list'),
]

