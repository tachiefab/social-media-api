from django.conf import settings
from django.db import models
from django.db.models.signals import post_save


def upload_profile_image(instance, filename):
    return "profile/{username}/{filename}".format(username=instance.user.username, filename=filename)

class Profile(models.Model):
    user        = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile') # user.profile
    profile_image       = models.ImageField(upload_to=upload_profile_image, null=True, blank=True)
    location = models.CharField(max_length=220, null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
    	return self.user.username

    @property
    def owner(self):
        return self.user

    def get_profile_image_url(self):
        try:
            image = self.profile_image.url
        except:
            image = None
        return image

def user_did_save(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

post_save.connect(user_did_save, sender=settings.AUTH_USER_MODEL)


class FriendsManager(models.Manager):

    def friend_toggle(self, authenticated_user, user_to_friend):
        user_friends, created = Friends.objects.get_or_create(user=user_to_friend)
        if authenticated_user in user_friends.friends.all():
            user_friends.friends.remove(authenticated_user)
            added = False
        else:
            user_friends.friends.add(authenticated_user)
            added = True
        return added

class Friends(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_friends')
    friends       = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='friends')
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = FriendsManager()

    def __str__(self):
        return str(self.friends.all().count()) + ' friends'


class FollowersManager(models.Manager):
    use_for_related_fields = True

    def toggle_follow(self, authenticated_user, user_to_follow):
        user_followers, created = Followers.objects.get_or_create(user=user_to_follow)
        if authenticated_user in user_followers.followers.all():
            user_followers.followers.remove(authenticated_user)
            added = False
        else:
            user_followers.followers.add(authenticated_user)
            added = True
        return added

    def is_following(self, user, followed_by_user):
        user_followers, created = Followers.objects.get_or_create(user=user)
        if created:
            return False
        if followed_by_user in user_followers.following.all():
            return True
        return False

class Followers(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_follower')
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followings', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = FollowersManager()

    def __str__(self):
        return self.user.username

    def get_following(self):
        users  = self.followings.all()
        return users.exclude(username=self.user.username)



