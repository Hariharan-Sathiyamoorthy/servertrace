
# Create your models here.
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User




class UserProfile(models.Model):
    user = models.OneToOneField(
        User, 
        verbose_name=_("user"), 
        on_delete=models.CASCADE
    )
    is_admin = models.BooleanField(default=False)
    is_techie = models.BooleanField(default=False)
    is_user = models.BooleanField(default=True)

    def delete(self, *args, **kwargs):
        self.user.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.user.username
    