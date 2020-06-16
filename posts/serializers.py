from django.utils.timesince import timesince
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.reverse import reverse as api_reverse
from accounts.serializers import UserPublicSerializer
from comments.models import Comment
from comments.serializers import CommentSerializer, CommentListSerializer
from .models import Post, PostLike


class PostSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)
    uri             = serializers.SerializerMethodField(read_only=True)
    date_display = serializers.SerializerMethodField()
    timesince = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    did_like = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'parent_id',
            'uri',
            'id',
            'user',
            'content',
            'image',
            'date_display',
            'timesince',
            'parent',
            'likes',
            'did_like'
        ]
        
    def get_did_like(self, obj):
        request = self.context.get("request")
        try:
            user = request.user
            if user.is_authenticated:
                try:
                    post = get_object_or_404(PostLike, post=obj)
                    liked_users = post.liked.all()
                except:
                    pass
                if user in liked_users:
                    return True
        except:
            pass
        return False

    def get_uri(self, obj):
        request = self.context.get('request')
        return api_reverse('api-posts:detail', kwargs={"pk": obj.pk}, request=request)

    def get_likes(self, obj):
        likes = 0
        try:
            qs = get_object_or_404(PostLike, post=obj)
            likes = qs.liked.all().count()
        except:
            pass
        return likes

    def get_date_display(self, obj):
        return obj.timestamp.strftime("%b %d, %Y at %I:%M %p")

    def get_timesince(self, obj):
        return timesince(obj.timestamp) + " ago"


class ParentPostModelSerializer(PostSerializer):

    class Meta:
        model = Post
        fields = [
            'uri',
            'id',
            'user',
            'content',
            'image',
            'date_display',
            'timesince',
            'likes',
            'did_like',
        ]


class PostInlineSerializer(PostSerializer):
    parent_id = serializers.CharField(write_only=True, required=False)
    parent = ParentPostModelSerializer(read_only=True)
    comments = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'parent_id',
            'uri',
            'id',
            'user',
            'content',
            'image',
            'date_display',
            'timesince',
            'parent',
            'likes',
            'did_like',
            'comments'
        ]

    def validate(self, data):
        content = data.get("content")
        if content == "":
            content = None
        image = data.get("image", None)
        if content is None:
            raise serializers.ValidationError("Content is required.")
        return data

    def get_comments(self, obj):
        request = self.context.get('request')
        limit = 10
        if request:
            limit_query = request.GET.get('comments_limit')
            try:
                limit = int(limit_query)
            except:
                pass
        c_qs = Comment.objects.filter_by_instance(obj)
        comments = CommentListSerializer(c_qs[:limit], many=True, context={'request': request}).data
        return comments
