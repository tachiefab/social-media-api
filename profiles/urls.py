from django.conf.urls import url
from .views import ProfileAPIDetailView

app_name= 'profiles'

urlpatterns = [
    url(r'^(?P<pk>\d+)/profile/$', ProfileAPIDetailView.as_view(), name='profile'),
]