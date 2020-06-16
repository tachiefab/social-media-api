from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import generics, mixins, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.permissions import IsOwnerOrReadOnly
from .models import Followers, Friends, Profile
from .serializers import FollowersSerializer, FriendsSerializer, PublicProfileSerializer

User = get_user_model()

class ProfileAPIDetailView(
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin, 
                    generics.RetrieveAPIView
                    ):

    permission_classes          = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class            = PublicProfileSerializer
    queryset                    = Profile.objects.all()

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class FollowersAPIView(generics.ListAPIView): 
    permission_classes          = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class            = FollowersSerializer

    queryset                    = Followers.objects.all()

class FriendsAPIView(generics.ListAPIView): 
    permission_classes          = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class            = FriendsSerializer

    queryset                    = Followers.objects.all()


class FollowToggleAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, username, format=None):
        message = ""
        user_qs = None
        try:
            user_qs = User.objects.get(username__iexact=username)
        except:
            message = "User does not exist"
        if user_qs is not None:
            if request.user.is_authenticated:
                is_following = Followers.objects.toggle_follow(request.user, user_qs)
                return Response({'following': is_following})
        return Response({"message": message}, status=400)


class FriendToggleAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, username, format=None):
        message = ""
        user_qs = None
        try:
            user_qs = User.objects.get(username__iexact=username)
        except:
            message = "User does not exist"
        if user_qs is not None:
            if request.user.is_authenticated:
                is_friending = Friends.objects.friend_toggle(request.user, user_qs)
                return Response({'friending': is_friending})
        return Response({"message": message}, status=400)

