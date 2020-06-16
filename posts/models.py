import re
from django.conf import settings
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from hashtags.signals import parsed_hashtags
from .validators import validate_content

def upload_post_image(instance, filename):
    return "post/{username}/{filename}".format(username=instance.user.username, filename=filename)

class Post(models.Model):
    parent      = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE)
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content     = models.CharField(max_length=140, validators=[validate_content])
    image       = models.ImageField(upload_to=upload_post_image, null=True, blank=True)
    updated     = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.content)

    @property
    def owner(self):
        return self.user

    def get_absolute_url(self):
        return reverse("api-posts:detail", kwargs={"pk":self.pk})

    class Meta:
        ordering = ['-timestamp']

    def get_parent(self):
        the_parent = self
        if self.parent:
            the_parent = self.parent
        return the_parent

    def get_children(self):
        parent = self.get_parent()
        qs = Post.objects.filter(parent=parent)
        qs_parent = Post.objects.filter(pk=parent.pk)
        return (qs | qs_parent)


class PostLikeManager(models.Manager):

    def like_toggle(self, user, post_obj):
        if user in post_obj.liked.all():
            is_liked = False
            post_obj.liked.remove(user)
        else:
            is_liked = True
            post_obj.liked.add(user)
        return is_liked

class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    liked       = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='likes')
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = PostLikeManager()

    def __str__(self):
        return str(self.liked.all().count()) + ' likes'








