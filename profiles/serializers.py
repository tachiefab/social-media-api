from rest_framework.serializers import SerializerMethodField, ModelSerializer
from django.conf import settings
from rest_framework.reverse import reverse as api_reverse
from django.shortcuts import get_object_or_404
from .models import Profile, Followers, Friends
from accounts.serializers import UserPublicSerializer

HOST_SERVER = settings.HOST_SERVER

class PublicProfileSerializer(ModelSerializer):
    first_name = SerializerMethodField(read_only=True)
    last_name = SerializerMethodField(read_only=True)
    profile_image = SerializerMethodField()
    bio = SerializerMethodField()
    location = SerializerMethodField()
    class Meta:
        model = Profile
        fields = [
            "first_name",
            "last_name",
            "profile_image",
            "bio",
            "location",
        ]
    
    def get_first_name(self, obj):
        return obj.user.first_name
    
    def get_last_name(self, obj):
        return obj.user.last_name


    def get_profile_image(self, obj):
        try:
            img = obj.get_profile_image_url()
            image = HOST_SERVER + img
        except:
           image = None
        return image

    def get_bio(self, obj):
        return obj.bio

    def get_location(self, obj):
        return obj.location

class FollowersSerializer(ModelSerializer):
    username = SerializerMethodField(read_only=True)
    first_name = SerializerMethodField(read_only=True)
    last_name = SerializerMethodField(read_only=True)
    profile_image = SerializerMethodField()
    uri             = SerializerMethodField(read_only=True)
    class Meta:
        model = Followers
        fields = [
            "username",
            'first_name',
            'last_name',
            "profile_image",
            'uri',
        ]

    def get_username(self, obj):
        try:
            username = obj.username
        except:
            username = obj.user.username
        return username

    def get_first_name(self, obj):
        try:
            first_name = obj.first_name
        except:
            first_name = obj.user.first_name
        return first_name

    def get_last_name(self, obj):
        try:
            last_name = obj.last_name
        except:
            last_name = obj.user.last_name
        return last_name

    def get_profile_image(self, obj):
        try:
            try:
                profile_obj = get_object_or_404(Profile, user=obj)
                img = profile_obj.get_profile_image_url()
            except:
                follow_obj = get_object_or_404(Followers, user=obj.user)
                profile_obj = get_object_or_404(Profile, user=follow_obj.user)
                img = profile_obj.get_profile_image_url()
            image = HOST_SERVER + img
        except:
           image = None
        return image

    def get_uri(self, obj):
        request = self.context.get('request')
        try:
            username = obj.username
        except:
            username = obj.user.username
        return api_reverse("api-user:detail", kwargs={"username": username}, request=request)


class FollowingsSerializer(FollowersSerializer):
    is_following = SerializerMethodField(read_only=True)
    class Meta:
        model = Followers
        fields = [
             "username",
            'first_name',
            'last_name',
            "profile_image",
            'uri',
            "is_following",
        ]

    def get_is_following(self, obj):
        request = self.context.get("request")
        try:
            user = request.user
            if user.is_authenticated:
                try:
                    follower_obj = get_object_or_404(Followers, user=obj.user)
                    followed_users = follower_obj.followers.all()
                except:
                    pass
                if user in followed_users:
                    return True
        except:
            pass
        return False


class FriendsSerializer(FollowersSerializer):
    are_friends = SerializerMethodField(read_only=True)
    class Meta:
        model = Friends
        fields = [
            "username",
            'first_name',
            'last_name',
            "profile_image",
            'uri',
            'are_friends',
        ]

    def get_are_friends(self, obj):
        request = self.context.get("request")
        try:
            user = request.user
            if user.is_authenticated:
                try:
                    friend_obj = get_object_or_404(Friends, user=obj)
                    friends = friend_obj.friends.all()
                except:
                    pass
                if user in friends:
                    return True
        except:
            pass
        return False