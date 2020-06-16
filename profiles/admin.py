from django.contrib import admin
from .models import Profile, Followers, Friends#, FollowerRelation

admin.site.register(Profile)
admin.site.register(Followers)
admin.site.register(Friends)
# admin.site.register(FollowerRelation)