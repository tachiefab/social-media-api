import datetime
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.serializers import SerializerMethodField, ModelSerializer
from rest_framework.reverse import reverse as api_reverse
from posts.serializers import PostInlineSerializer
from profiles.models import Followers, Friends
from posts.models import Post
from profiles.serializers import (
                                PublicProfileSerializer, 
                                FollowersSerializer, 
                                FollowingsSerializer, 
                                FriendsSerializer
                                )

User = get_user_model()


class UserDetailSerializer(ModelSerializer):
    profile = PublicProfileSerializer(read_only=True)
    uri             = SerializerMethodField(read_only=True)
    posts          = SerializerMethodField(read_only=True)
    followers          = SerializerMethodField(read_only=True)
    followings          = SerializerMethodField(read_only=True)
    friends          = SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'uri',
            'profile',
            'posts',
            'followers',
            'followings',
            'friends',
        ]

    def get_uri(self, obj):
        request = self.context.get('request')
        return api_reverse("api-user:detail", kwargs={"username": obj.username}, request=request)

    def get_posts(self, obj):
        request = self.context.get('request')
        limit = 10
        if request:
            limit_query = request.GET.get('posts_limit')
            try:
                limit = int(limit_query)
            except:
                pass
        qs1 = obj.post_set.all().order_by("-timestamp")
        user_following = obj.followings.all()
        followings = user_following.exclude(user=obj)
        users = []
        for following in followings:
            user = get_object_or_404(User, username=following.user.username)
            users.append(user)
        qs2 = Post.objects.filter(user__in=users)
        qs = (qs1 | qs2).distinct().order_by("-timestamp")
        data = {
            'total': obj.post_set.all().count(),
            'uri': self.get_uri(obj) + "posts/",
            'last': PostInlineSerializer(qs.first(), context={'request': request}).data,
            'recent': PostInlineSerializer(qs[:limit], many=True, context={'request': request}).data
        }
        return data

    def get_followers(self, obj):
        request = self.context.get('request')
        limit = 10
        if request:
            limit_query = request.GET.get('followers_limit')
            try:
                limit = int(limit_query)
            except:
                pass
        try:
            follower_obj = get_object_or_404(Followers, user=obj)
            # Have to exclude the user from his or her followers
            followers = follower_obj.followers.all()#.exclude(user=obj)
        except:
            pass
        try:
            data = {
                'total': followers.count(),
                'uri': self.get_uri(obj) + "followers/",
                'last': FollowersSerializer(followers.first(), context={'request': request}).data,
                'recent': FollowersSerializer(followers[:limit], many=True, context={'request': request}).data
            }
        except:
            data = "No followers yet."
        return data

    def get_followings(self, obj):
        request = self.context.get('request')
        limit = 10
        if request:
            limit_query = request.GET.get('followings_limit')
            try:
                limit = int(limit_query)
            except:
                pass
        try:
            follower_obj = get_object_or_404(Followers, user=obj)
            followings = follower_obj.user.followings.all()
        except:
            pass
        try:
            data = {
                'total': followings.count(),
                'uri': self.get_uri(obj) + "followings/",
                'last': FollowingsSerializer(followings.first(), context={'request': request}).data,
                'recent': FollowingsSerializer(followings[:limit], many=True, context={'request': request}).data
            }
        except:
            data = "No followings yet."
        return data

    def get_friends(self, obj):
        request = self.context.get('request')
        limit = 10
        if request:
            limit_query = request.GET.get('friends_limit')
            try:
                limit = int(limit_query)
            except:
                pass
        try:
            friends_obj = get_object_or_404(Friends, user=obj)
            friends = friends_obj.friends.all()
        except:
            pass
        try:
            data = {
                'total': friends.count(),
                'uri': self.get_uri(obj) + "friends/",
                'last': FriendsSerializer(friends.first(), context={'request': request}).data,
                'recent': FriendsSerializer(friends[:limit], many=True, context={'request': request}).data
            }
        except:
            data = "No friends yet."
        return data





