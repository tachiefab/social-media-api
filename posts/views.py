from rest_framework import generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.permissions import IsOwnerOrReadOnly
from .models import Post, PostLike
from .serializers import PostInlineSerializer


class PostAPIDetailView(
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin, 
                    generics.RetrieveAPIView
                    ):

    permission_classes          = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class            = PostInlineSerializer
    queryset                    = Post.objects.all()

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class PostAPIView(
                mixins.CreateModelMixin, 
                generics.ListAPIView
                ): 

    permission_classes          = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class            = PostInlineSerializer
    passed_id                   = None
    search_fields               = ('user__username', 'content', 'user__email')
    ordering_fields             = ('user__username', 'timestamp')

    queryset                    = Post.objects.all()
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LikeToggleAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, format=None):
        message = ""
        post_qs = None
        try:
            post_qs = Post.objects.get(pk=pk)
        except:
            message = "Post does not exist"
        if post_qs is not None:
            try:
                postlike_qs = PostLike.objects.get(post=post_qs)
            except:
                postlike_qs = PostLike.objects.create(post=post_qs)
            if request.user.is_authenticated:
                is_liked = PostLike.objects.like_toggle(request.user, postlike_qs)
                return Response({'liked': is_liked})
        return Response({"message": message}, status=400)