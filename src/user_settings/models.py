from django.conf import settings
from django.db import models



class UserProfileManager(models.Manager):
    def get_user_profile(self, request):
        user_profile = super(UserProfileManager, self).filter(user=request.user)
        if user_profile:
            return user_profile[0]

    def get_user_profile_by_eventcode(self, request):
        pass



class UserProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    username = models.CharField(max_length=120, null=True, blank=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    objects = UserProfileManager()

    def __str__(self):
        return '{}: {}'.format(self.id, self.user)
