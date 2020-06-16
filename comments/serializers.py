from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.reverse import reverse as api_reverse
from django.utils.timesince import timesince
from django.contrib.auth import get_user_model
from rest_framework import serializers
from accounts.serializers import UserPublicSerializer
from comments.models import Comment
from profiles.models import Profile

User = get_user_model()
HOST_SERVER = settings.HOST_SERVER

class CommentSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)
    uri             = serializers.SerializerMethodField(read_only=True)
    date_display = serializers.SerializerMethodField()
    timesince = serializers.SerializerMethodField()
    reply_count = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = [
            'id',
            'uri',
            'content_type',
            'object_id',
            'parent',
            'content',
            'reply_count',
            'timesince',
            'date_display',
            'user',
        ]

    def get_uri(self, obj):
        request = self.context.get('request')
        return api_reverse("comments-api:thread", kwargs={"pk": obj.pk}, request=request)

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0

    def get_date_display(self, obj):
        return obj.timestamp.strftime("%b %d, %Y at %I:%M %p")

    def get_timesince(self, obj):
        return timesince(obj.timestamp) + " ago"


class CommentCreateSerializer(CommentSerializer):
        user = UserPublicSerializer(read_only=True)
        type = serializers.CharField(required=False, write_only=True)
        obj_id = serializers.IntegerField(write_only=True)
        parent_id = serializers.IntegerField(required=False)

        class Meta:
            model = Comment
            fields = [
                'id',
                'user',
                'content',
                'type',
                'obj_id',
                'parent_id',
                'date_display',
                'timesince'
            ]


        def validate(self, data):
            model_type      = data.get("type", "post")
            model_qs        = ContentType.objects.filter(model=model_type)
            if not model_qs.exists() or model_qs.count() != 1:
                raise serializers.ValidationError("This is not a valid content type")
            SomeModel       = model_qs.first().model_class()
            obj_id            = data.get("obj_id")
            obj_qs          = SomeModel.objects.filter(id=obj_id)
            if not obj_qs.exists() or obj_qs.count() != 1:
                raise serializers.ValidationError("This is not a id for this content type")
            parent_id       = data.get("parent_id")
            if parent_id:
                parent_qs   = Comment.objects.filter(id=parent_id)
                if not parent_qs.exists() or parent_qs.count() !=1:
                    raise serializers.ValidationError("This is not a valid parent for this content")
            return data

        def create(self, validated_data):
            content         = validated_data.get("content")
            model_type      = validated_data.get("type", "post")
            obj_id            = validated_data.get("obj_id")
            parent_obj      = None
            parent_id       = validated_data.get("parent_id")
            if parent_id:
                parent_obj  = Comment.objects.filter(id=parent_id).first()
            user            = self.context['user']
            comment         = Comment.objects.create_by_model_type(
                                model_type, obj_id, content, user,
                                parent_obj=parent_obj,
                    )
            return comment


class CommentListSerializer(CommentSerializer):
    reply_count = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = [
            'uri',
            'id',
            'content',
            'reply_count',
            'timesince',
            'date_display',
            'user',
        ]

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0


class CommentChildSerializer(CommentSerializer):
    class Meta:
        model = Comment
        fields = [
            'id',
            'user',
            'content',
            'timesince',
            'date_display',
        ]
    read_only_fields = [
            'timesince',
            'date_display',
        ]

class CommentDetailSerializer(CommentSerializer):
    reply_count = serializers.SerializerMethodField()
    content_object_url = serializers.SerializerMethodField()
    replies =   serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = [
            'id',
            'content',
            'reply_count',
            'timesince',
            'date_display',
            'content_object_url',
            'user',
            'replies',
        ]
        read_only_fields = [
            'reply_count',
            'replies',
        ]

    def get_content_object_url(self, obj):
        try:
            uri = obj.content_object.get_absolute_url()
            return HOST_SERVER + uri
        except:
            return None

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True).data
        return None

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0
