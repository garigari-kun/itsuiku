from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    username = models.CharField(max_length=120, null=True, blank=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return '{}: {}'.format(self.id, self.user)
