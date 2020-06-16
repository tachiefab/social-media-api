from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView
    )
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
    )
from accounts.permissions import IsOwnerOrReadOnly
from comments.models import Comment
from .serializers import (
    CommentListSerializer,
    CommentDetailSerializer,
    CommentCreateSerializer
    )

User = get_user_model()

class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer

    def get_serializer_context(self):
        context = super(CommentCreateAPIView, self).get_serializer_context()
        context['user'] = self.request.user
        return context


class CommentDetailAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
    queryset = Comment.objects.filter(id__gte=0)
    serializer_class = CommentDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CommentListAPIView(ListAPIView):
    serializer_class = CommentListSerializer
    permission_classes = [AllowAny]
    search_fields = ['content', 'user__first_name']

    def get_queryset(self, *args, **kwargs):
        queryset_list = []
        query = self.request.GET.get("q")
        obj_id = self.request.GET.get("obj_id")
        type = self.request.GET.get("type", "post")
        if obj_id:
            model_type      = type
            model_qs        = ContentType.objects.filter(model=model_type)
            if model_qs.exists():  
                SomeModel       = model_qs.first().model_class()
                obj_qs          = SomeModel.objects.filter(id=obj_id)
                if obj_qs.exists():
                    content_obj     = obj_qs.first()
                    queryset_list   = Comment.objects.filter_by_instance(content_obj)
        else:
            queryset_list = Comment.objects.filter(id__gte=0)

        if query:
            queryset_list = queryset_list.filter(
                    Q(content__icontains=query)|
                    Q(user__first_name__icontains=query) |
                    Q(user__last_name__icontains=query)
                    ).distinct()
        return queryset_list

