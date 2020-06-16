from django.conf.urls import url
from .views import (
	LikeToggleAPIView,
    PostAPIView, 
    PostAPIDetailView,
    )

app_name= 'Posts'

urlpatterns = [
    url(r'^$', PostAPIView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', PostAPIDetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/like/$', LikeToggleAPIView.as_view(), name='like-toggle'),
]
